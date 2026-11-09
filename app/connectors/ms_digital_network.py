from __future__ import annotations

import hashlib
import hmac
import json
import time

import httpx
from fastapi import HTTPException


def sign_payload(payload: dict, secret: str, timestamp: int | None = None) -> tuple[dict, bytes]:
    timestamp = timestamp or int(time.time())
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), str(timestamp).encode() + b"." + body, hashlib.sha256).hexdigest()
    return {
        "Content-Type": "application/json",
        "X-MS-Timestamp": str(timestamp),
        "X-MS-Signature": f"sha256={signature}",
    }, body


async def send_event(base_url: str, secret: str, event: str, data: dict) -> dict:
    if not base_url or not secret:
        raise HTTPException(503, "Configurez MS_DN_BASE_URL et MS_DN_WEBHOOK_SECRET côté serveur.")
    headers, body = sign_payload({"event": event, "data": data}, secret)
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(base_url.rstrip("/") + "/api/integrations/ms-nexus/events", content=body, headers=headers)
            response.raise_for_status()
            return {"connected": True, "status_code": response.status_code, "response": response.json() if response.content else {}}
    except httpx.HTTPStatusError as exc:
        raise HTTPException(502, f"MS DIGITAL NETWORK a répondu HTTP {exc.response.status_code}.") from exc
    except httpx.RequestError as exc:
        raise HTTPException(503, "MS DIGITAL NETWORK est inaccessible depuis ce serveur.") from exc
