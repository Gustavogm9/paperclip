#!/bin/sh
set -e

# Capture runtime UID/GID from environment variables, defaulting to 1000
PUID=${USER_UID:-1000}
PGID=${USER_GID:-1000}

# Adjust the node user's UID/GID if they differ from the runtime request
# and fix volume ownership only when a remap is needed
changed=0

if [ "$(id -u node)" -ne "$PUID" ]; then
    echo "Updating node UID to $PUID"
    usermod -o -u "$PUID" node
    changed=1
fi

if [ "$(id -g node)" -ne "$PGID" ]; then
    echo "Updating node GID to $PGID"
    groupmod -o -g "$PGID" node
    usermod -g "$PGID" node
    changed=1
fi

if [ "1" = "1" ]; then
    chown -R node:node /paperclip
fi

# On first boot in authenticated mode, generate a bootstrap CEO invite URL
# if no admin exists yet. URL is printed to stdout (Railway logs) so the
# operator can redeem it via web.
if [ "${PAPERCLIP_DEPLOYMENT_MODE}" = "authenticated" ] && [ -n "${DATABASE_URL}" ]; then
    echo "[entrypoint] Checking bootstrap admin state..."
    if [ -f /app/server/scripts/bootstrap-admin-if-needed.ts ]; then
        gosu node sh -c "cd /app/server && node --import ./node_modules/tsx/dist/loader.mjs scripts/bootstrap-admin-if-needed.ts" || \
            echo "[entrypoint] bootstrap-admin script failed (non-fatal, continuing)"
    fi
fi

exec gosu node "$@"
