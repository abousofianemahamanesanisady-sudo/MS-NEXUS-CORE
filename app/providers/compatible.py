import httpx
from fastapi import HTTPException
from ..config import get_settings
def _config():
    s = get_settings()
    if not s.ai_api_key: raise HTTPException(503, "Configurez AI_API_KEY dans .env")
    return s, {"Authorization": f"Bearer {s.ai_api_key}"}
async def _json(path, payload, model_field):
    s, headers = _config(); body = dict(payload)
    if body.get("model") == "default": body["model"] = getattr(s, model_field)
    try:
        async with httpx.AsyncClient(timeout=s.ai_timeout_seconds) as client:
            r = await client.post(s.ai_base_url.rstrip("/") + path, headers=headers, json=body); r.raise_for_status(); return r.json()
    except httpx.HTTPStatusError as e: raise HTTPException(502, f"Provider error {e.response.status_code}: {e.response.text[:400]}")
    except httpx.RequestError as e: raise HTTPException(502, f"Provider unavailable: {e}")
async def chat(p): return await _json("/chat/completions", p, "ai_text_model")
async def image(p): return await _json("/images/generations", p, "ai_image_model")
async def speech(p):
    s, headers = _config(); body = dict(p)
    if body.get("model") == "default": body["model"] = s.ai_audio_model
    try:
        async with httpx.AsyncClient(timeout=s.ai_timeout_seconds) as client:
            r = await client.post(s.ai_base_url.rstrip("/") + "/audio/speech", headers=headers, json=body); r.raise_for_status()
            return r.content, r.headers.get("content-type", "audio/mpeg")
    except httpx.HTTPStatusError as e: raise HTTPException(502, f"Audio provider error {e.response.status_code}: {e.response.text[:400]}")
    except httpx.RequestError as e: raise HTTPException(502, f"Audio provider unavailable: {e}")
