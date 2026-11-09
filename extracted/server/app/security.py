import hashlib, secrets
from fastapi import Header, HTTPException
from .config import ADMIN_KEY
from .db import connect

def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def require_admin(x_nexus_admin: str = Header(default="")):
    if not ADMIN_KEY or not secrets.compare_digest(x_nexus_admin, ADMIN_KEY):
        raise HTTPException(status_code=403, detail="Admin access denied")

def require_api_key(authorization: str = Header(default="")) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Use Authorization: Bearer YOUR_API_KEY")
    raw = authorization[7:].strip()
    if not raw:
        raise HTTPException(status_code=401, detail="Missing API key")
    with connect() as db:
        row = db.execute(
            "SELECT owner FROM api_keys WHERE key_hash=? AND active=1", (digest(raw),)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=401, detail="Invalid or revoked API key")
    return row["owner"]

def new_api_key() -> str:
    return "msnx_" + secrets.token_urlsafe(32)
