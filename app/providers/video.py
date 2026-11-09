import httpx
from fastapi import HTTPException
from ..config import get_settings
async def submit(payload):
    s = get_settings()
    if not s.video_api_url or not s.video_api_key: raise HTTPException(503, "Vidéo non configurée : renseignez VIDEO_API_URL et VIDEO_API_KEY.")
    try:
        async with httpx.AsyncClient(timeout=s.video_timeout_seconds) as client:
            r = await client.post(s.video_api_url, headers={"Authorization": f"Bearer {s.video_api_key}"}, json=payload); r.raise_for_status(); data = r.json()
            if not (data.get("id") or data.get("job_id")): raise HTTPException(502, "Réponse vidéo invalide : id/job_id manquant.")
            return data
    except httpx.HTTPStatusError as e: raise HTTPException(502, f"Video provider error {e.response.status_code}: {e.response.text[:400]}")
    except httpx.RequestError as e: raise HTTPException(502, f"Video provider unavailable: {e}")
