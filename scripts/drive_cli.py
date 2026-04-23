#!/usr/bin/env python3
"""
drive_cli.py — CLI para agentes Paperclip lerem/escreverem no Google Drive.

Usa a Service Account configurada em GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON (env var).
Root folder: GOOGLE_DRIVE_ROOT_FOLDER_ID (env var, default = Shared Drive
"Guilds Ops Agents").

Comandos:
    list <folder-path>              listar arquivos/pastas em path relativo à root
    find <folder-path> <query>      buscar por nome (substring) em path
    read <file-path>                ler conteúdo de arquivo texto
    write <file-path>               escrever/sobrescrever (conteúdo via stdin)
    move <file-path> <new-folder-path>  mover arquivo
    mkdir <folder-path>             criar pasta (idempotente)
    path-to-id <path>               resolver path para file/folder id

Exemplos:
    python drive_cli.py list 01-clients/guilds/outputs/drafts
    echo "conteudo" | python drive_cli.py write 01-clients/guilds/outputs/drafts/teste.md
    python drive_cli.py read 00-agency-shared/metodologia-g-forge/README.md
    python drive_cli.py move 01-clients/guilds/outputs/drafts/teste.md 01-clients/guilds/outputs/in-review

Sem dependências externas — usa apenas stdlib (urllib, json, base64, hmac, hashlib).
Compatível com Python 3.8+.
"""

import os
import sys
import json
import time
import base64
import hmac
import hashlib
import urllib.request
import urllib.parse
import urllib.error


GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
DRIVE_API = "https://www.googleapis.com/drive/v3"
DRIVE_UPLOAD_API = "https://www.googleapis.com/upload/drive/v3"
SCOPES = "https://www.googleapis.com/auth/drive"

# =====================================================================
# JWT e autenticação
# =====================================================================

def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _rsa_sign(msg: bytes, private_key_pem: str) -> bytes:
    """Assina uma mensagem com RSA-SHA256 usando chave privada PEM.

    Implementação minimalista que usa o módulo hashlib + estruturas básicas.
    Se a libcrypto estiver disponível via cryptography/pycryptodome, preferir
    por segurança e robustez.
    """
    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
        key = serialization.load_pem_private_key(
            private_key_pem.encode(), password=None
        )
        return key.sign(msg, padding.PKCS1v15(), hashes.SHA256())
    except ImportError:
        pass

    try:
        from Crypto.PublicKey import RSA
        from Crypto.Hash import SHA256
        from Crypto.Signature import pkcs1_15
        key = RSA.import_key(private_key_pem)
        h = SHA256.new(msg)
        return pkcs1_15.new(key).sign(h)
    except ImportError:
        pass

    raise RuntimeError(
        "Nenhuma lib de criptografia disponível. Instale 'cryptography' ou "
        "'pycryptodome': pip install cryptography"
    )


def _get_access_token() -> str:
    """Obtém access_token via JWT assinado com a Service Account.

    Cache simples em /tmp para evitar regerar a cada chamada.
    """
    cache_path = "/tmp/.drive_cli_token_cache.json"
    try:
        with open(cache_path) as f:
            cache = json.load(f)
        if cache.get("expires_at", 0) > time.time() + 60:
            return cache["access_token"]
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    sa_json = os.environ.get("GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON")
    if not sa_json:
        raise RuntimeError(
            "GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON não definida no ambiente"
        )

    sa = json.loads(sa_json)

    now = int(time.time())
    claim = {
        "iss": sa["client_email"],
        "scope": SCOPES,
        "aud": GOOGLE_TOKEN_URL,
        "exp": now + 3600,
        "iat": now,
    }
    header = {"alg": "RS256", "typ": "JWT"}

    header_b64 = _b64url(json.dumps(header, separators=(",", ":")).encode())
    claim_b64 = _b64url(json.dumps(claim, separators=(",", ":")).encode())
    msg = f"{header_b64}.{claim_b64}".encode()
    signature = _rsa_sign(msg, sa["private_key"])
    jwt_token = f"{header_b64}.{claim_b64}.{_b64url(signature)}"

    data = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_token,
    }).encode()

    req = urllib.request.Request(
        GOOGLE_TOKEN_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read())

    cache = {
        "access_token": body["access_token"],
        "expires_at": time.time() + body.get("expires_in", 3600),
    }
    try:
        with open(cache_path, "w") as f:
            json.dump(cache, f)
    except OSError:
        pass
    return cache["access_token"]


# =====================================================================
# Helpers Drive API
# =====================================================================

def _drive_request(method, path, params=None, data=None, headers=None, upload=False):
    base = DRIVE_UPLOAD_API if upload else DRIVE_API
    url = base + path
    query_params = {"supportsAllDrives": "true"}
    if params:
        query_params.update(params)
    if query_params:
        url += "?" + urllib.parse.urlencode(query_params)

    req_headers = {
        "Authorization": f"Bearer {_get_access_token()}",
    }
    if headers:
        req_headers.update(headers)

    if data is not None and not isinstance(data, bytes):
        data = data.encode() if isinstance(data, str) else json.dumps(data).encode()
        if "Content-Type" not in req_headers:
            req_headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        raise RuntimeError(f"Drive API {e.code} em {method} {path}: {err_body}")


def _list_children(parent_id, name=None):
    q = f"'{parent_id}' in parents and trashed=false"
    if name:
        escaped = name.replace("'", "\\'")
        q += f" and name='{escaped}'"
    result = _drive_request(
        "GET",
        "/files",
        params={
            "q": q,
            "fields": "files(id,name,mimeType,modifiedTime,size)",
            "includeItemsFromAllDrives": "true",
            "corpora": "allDrives",
            "pageSize": "1000",
        },
    )
    return result.get("files", [])


def _resolve_path(path):
    """Resolve path relativo à root folder para file/folder id."""
    root = os.environ.get("GOOGLE_DRIVE_ROOT_FOLDER_ID")
    if not root:
        raise RuntimeError("GOOGLE_DRIVE_ROOT_FOLDER_ID não definida")
    current = root
    current_mime = "application/vnd.google-apps.folder"
    parts = [p for p in path.strip("/").split("/") if p]
    for i, part in enumerate(parts):
        children = _list_children(current, name=part)
        if not children:
            raise RuntimeError(f"Path não encontrado: {'/'.join(parts[:i+1])}")
        child = children[0]
        current = child["id"]
        current_mime = child.get("mimeType", "")
    return {"id": current, "mimeType": current_mime}


# =====================================================================
# Comandos
# =====================================================================

def cmd_list(path):
    folder = _resolve_path(path) if path else {"id": os.environ["GOOGLE_DRIVE_ROOT_FOLDER_ID"]}
    items = _list_children(folder["id"])
    for item in sorted(items, key=lambda x: (x.get("mimeType", "") != "application/vnd.google-apps.folder", x["name"])):
        kind = "DIR " if item.get("mimeType") == "application/vnd.google-apps.folder" else "FILE"
        size = item.get("size", "-")
        modified = item.get("modifiedTime", "")[:10]
        print(f"{kind}  {modified}  {size:>10}  {item['name']}  ({item['id']})")


def cmd_find(path, query):
    folder = _resolve_path(path) if path else {"id": os.environ["GOOGLE_DRIVE_ROOT_FOLDER_ID"]}
    items = _list_children(folder["id"])
    matches = [i for i in items if query.lower() in i["name"].lower()]
    for item in matches:
        print(f"{item['id']}  {item['name']}")


def cmd_read(path):
    resolved = _resolve_path(path)
    if resolved["mimeType"] == "application/vnd.google-apps.folder":
        raise RuntimeError(f"{path} é uma pasta, não arquivo")
    url = f"{DRIVE_API}/files/{resolved['id']}?alt=media&supportsAllDrives=true"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {_get_access_token()}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        sys.stdout.buffer.write(resp.read())


def cmd_write(path):
    """Escreve conteúdo lido do stdin no path dado. Cria ou sobrescreve."""
    content = sys.stdin.buffer.read()
    parts = path.strip("/").split("/")
    parent_parts = parts[:-1]
    filename = parts[-1]

    parent_id = os.environ["GOOGLE_DRIVE_ROOT_FOLDER_ID"]
    if parent_parts:
        parent_id = _resolve_path("/".join(parent_parts))["id"]

    # Verifica se arquivo existe
    existing = _list_children(parent_id, name=filename)
    existing_file = existing[0] if existing else None

    mime_type = _guess_mime(filename)

    boundary = "----paperclipboundary" + str(int(time.time()))
    metadata = {"name": filename, "parents": [parent_id]}
    if existing_file:
        metadata = {}  # on update, não repetir parents

    body = (
        f"--{boundary}\r\n"
        f"Content-Type: application/json; charset=UTF-8\r\n\r\n"
        f"{json.dumps(metadata)}\r\n"
        f"--{boundary}\r\n"
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode() + content + f"\r\n--{boundary}--".encode()

    if existing_file:
        path_api = f"/files/{existing_file['id']}"
        method = "PATCH"
    else:
        path_api = "/files"
        method = "POST"

    result = _drive_request(
        method,
        path_api,
        params={"uploadType": "multipart"},
        data=body,
        headers={"Content-Type": f"multipart/related; boundary={boundary}"},
        upload=True,
    )
    print(f"{'atualizado' if existing_file else 'criado'}: {result.get('id')}  {filename}")


def cmd_move(path, new_folder_path):
    resolved = _resolve_path(path)
    new_folder = _resolve_path(new_folder_path)
    if new_folder["mimeType"] != "application/vnd.google-apps.folder":
        raise RuntimeError(f"{new_folder_path} não é pasta")

    # Pega os parents atuais
    meta = _drive_request("GET", f"/files/{resolved['id']}", params={"fields": "parents"})
    prev_parents = ",".join(meta.get("parents", []))

    _drive_request(
        "PATCH",
        f"/files/{resolved['id']}",
        params={
            "addParents": new_folder["id"],
            "removeParents": prev_parents,
            "fields": "id,parents",
        },
    )
    print(f"movido: {path} → {new_folder_path}/")


def cmd_mkdir(path):
    """Idempotente: cria path (pasta) relativo à root se não existir."""
    parts = [p for p in path.strip("/").split("/") if p]
    root = os.environ["GOOGLE_DRIVE_ROOT_FOLDER_ID"]
    current = root
    for part in parts:
        existing = _list_children(current, name=part)
        if existing and existing[0].get("mimeType") == "application/vnd.google-apps.folder":
            current = existing[0]["id"]
            continue
        result = _drive_request(
            "POST",
            "/files",
            params={"fields": "id"},
            data={
                "name": part,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [current],
            },
        )
        current = result["id"]
    print(current)


def cmd_path_to_id(path):
    resolved = _resolve_path(path)
    print(resolved["id"])


def _guess_mime(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return {
        "md": "text/markdown",
        "txt": "text/plain",
        "json": "application/json",
        "yaml": "text/yaml",
        "yml": "text/yaml",
        "html": "text/html",
        "csv": "text/csv",
        "pdf": "application/pdf",
    }.get(ext, "application/octet-stream")


# =====================================================================
# Main
# =====================================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    try:
        if cmd == "list":
            cmd_list(args[0] if args else "")
        elif cmd == "find":
            cmd_find(args[0], args[1])
        elif cmd == "read":
            cmd_read(args[0])
        elif cmd == "write":
            cmd_write(args[0])
        elif cmd == "move":
            cmd_move(args[0], args[1])
        elif cmd == "mkdir":
            cmd_mkdir(args[0])
        elif cmd == "path-to-id":
            cmd_path_to_id(args[0])
        else:
            print(f"Comando desconhecido: {cmd}", file=sys.stderr)
            print(__doc__, file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"ERRO: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
