import secrets
from fastapi import Header, HTTPException
from .config import get_settings
async def require_api_key(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.lower().startswith("bearer "): raise HTTPException(401, "Bearer API key required")
    key = authorization.split(" ", 1)[1].strip()
    if not any(secrets.compare_digest(key, valid) for valid in get_settings().api_keys): raise HTTPException(401, "Invalid API key")
    return key
async def require_admin_key(x_admin_key: str | None = Header(default=None)):
    expected = get_settings().admin_api_key
    if not x_admin_key or not secrets.compare_digest(x_admin_key, expected): raise HTTPException(403, "Admin access denied")
