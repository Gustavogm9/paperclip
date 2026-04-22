/**
 * Bootstrap admin script for Paperclip running in containers.
 *
 * Located at server/scripts/ so Node/tsx can resolve drizzle-orm from
 * server/node_modules/ (the pnpm workspace does not hoist it to /app/node_modules).
 *
 * Runs on every container start. If no instance_admin exists, creates
 * a bootstrap_ceo invite and prints the URL to stdout (captured in container logs).
 *
 * Uses env vars directly — no config file required:
 *   - DATABASE_URL (required)
 *   - PAPERCLIP_AUTH_PUBLIC_BASE_URL or PAPERCLIP_PUBLIC_URL (required)
 */

import { createHash, randomBytes } from "node:crypto";
import { and, eq, gt, isNull } from "drizzle-orm";
import { createDb } from "../../packages/db/src/client.js";
import { instanceUserRoles, invites } from "../../packages/db/src/schema/index.js";

function hashToken(token: string) {
  return createHash("sha256").update(token).digest("hex");
}

function createInviteToken() {
  return `pcp_bootstrap_${randomBytes(24).toString("hex")}`;
}

function resolveBaseUrl(): string | null {
  const candidates = [
    process.env.PAPERCLIP_AUTH_PUBLIC_BASE_URL,
    process.env.PAPERCLIP_PUBLIC_URL,
    process.env.BETTER_AUTH_URL,
    process.env.BETTER_AUTH_BASE_URL,
  ];
  for (const candidate of candidates) {
    if (candidate && candidate.trim()) {
      return candidate.trim().replace(/\/+$/, "");
    }
  }
  return null;
}

async function main() {
  const dbUrl = process.env.DATABASE_URL;
  if (!dbUrl) {
    process.stderr.write("[bootstrap-admin] DATABASE_URL not set, skipping\n");
    return;
  }

  const baseUrl = resolveBaseUrl();
  if (!baseUrl) {
    process.stderr.write(
      "[bootstrap-admin] PAPERCLIP_AUTH_PUBLIC_BASE_URL not set, skipping\n",
    );
    return;
  }

  const db = createDb(dbUrl);
  const closableDb = db as typeof db & {
    $client?: {
      end?: (options?: { timeout?: number }) => Promise<void>;
    };
  };

  try {
    const adminRows = await db
      .select()
      .from(instanceUserRoles)
      .where(eq(instanceUserRoles.role, "instance_admin"))
      .limit(1);

    if (adminRows.length > 0) {
      process.stdout.write(
        "[bootstrap-admin] Instance admin already exists — skipping invite creation.\n",
      );
      return;
    }

    const now = new Date();
    const existingInvites = await db
      .select()
      .from(invites)
      .where(
        and(
          eq(invites.inviteType, "bootstrap_ceo"),
          isNull(invites.revokedAt),
          isNull(invites.acceptedAt),
          gt(invites.expiresAt, now),
        ),
      )
      .limit(1);

    if (existingInvites.length > 0) {
      process.stdout.write(
        "[bootstrap-admin] Active bootstrap invite already exists. " +
          "Re-generate via `pnpm paperclipai auth bootstrap-ceo --force` if needed.\n",
      );
      return;
    }

    const token = createInviteToken();
    const expiresAt = new Date(Date.now() + 72 * 60 * 60 * 1000); // 72h
    await db.insert(invites).values({
      inviteType: "bootstrap_ceo",
      tokenHash: hashToken(token),
      allowedJoinTypes: "human",
      expiresAt,
      invitedByUserId: "system",
    });

    const inviteUrl = `${baseUrl}/invite/${token}`;
    process.stdout.write("\n");
    process.stdout.write("====================================================\n");
    process.stdout.write("  PAPERCLIP BOOTSTRAP CEO INVITE (first admin)\n");
    process.stdout.write("====================================================\n");
    process.stdout.write(`  URL:     ${inviteUrl}\n`);
    process.stdout.write(`  Expires: ${expiresAt.toISOString()}\n`);
    process.stdout.write("====================================================\n");
    process.stdout.write("\n");
  } catch (error) {
    process.stderr.write(
      `[bootstrap-admin] ERROR: ${error instanceof Error ? error.stack ?? error.message : String(error)}\n`,
    );
  } finally {
    await closableDb.$client?.end?.({ timeout: 5 }).catch(() => undefined);
  }
}

main().catch((error) => {
  process.stderr.write(
    `[bootstrap-admin] FATAL: ${error instanceof Error ? error.stack ?? error.message : String(error)}\n`,
  );
});
