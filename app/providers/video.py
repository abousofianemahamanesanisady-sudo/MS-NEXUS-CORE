import httpx
from fastapi import HTTPException
from ..config import get_settings

async def submit(payload):
    s = get_settings()
    if not s.video_api_url:
        raise HTTPException(503, "Vidéo non configurée : renseignez VIDEO_API_URL vers votre worker auto-hébergé.")
    headers = {"Authorization": f"Bearer {s.video_api_key}"} if s.video_api_key else {}
    try:
        async with httpx.AsyncClient(timeout=s.video_timeout_seconds) as client:
            response = await client.post(s.video_api_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if not (data.get("id") or data.get("job_id")):
                raise HTTPException(502, "Réponse vidéo invalide : id/job_id manquant.")
            return data
    except httpx.HTTPStatusError as exc:
        raise HTTPException(502, f"Worker vidéo en erreur ({exc.response.status_code}).") from exc
    except httpx.RequestError as exc:
        raise HTTPException(502, "Worker vidéo auto-hébergé inaccessible.") from exc
