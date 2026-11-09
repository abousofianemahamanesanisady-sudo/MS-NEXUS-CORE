import json
import uuid
import httpx
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from .config import get_settings
from .db import initialize_database, get_db
from .models import Job
from .schemas import ChatRequest, ImageRequest, SpeechRequest, VideoRequest
from .security import require_api_key, require_admin_key
from .runtime.registry import list_models
from .runtime.router import hybrid_chat
from .runtime.local import local_generation
from .connectors.ms_digital_network import send_event

s = get_settings()
initialize_database()
app = FastAPI(title=s.app_name, version="2.2.0", description="Runtime hybride autonome edge/cloud auto-hébergé")
app.add_middleware(CORSMiddleware, allow_origins=s.allowed_origins, allow_credentials=False,
                   allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type", "X-Admin-Key"])

@app.get("/")
async def root():
    return {"name": s.app_name, "version": "2.2.0", "runtime": "hybrid", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ms-nexus-api", "version": "2.2.0", "runtime": s.runtime_mode}

@app.get("/v1/models", dependencies=[Depends(require_api_key)])
async def models():
    return {"object": "list", "data": list_models(s), "runtime": "edge-first-hybrid"}

@app.post("/v1/chat/completions", dependencies=[Depends(require_api_key)])
async def chat(req: ChatRequest):
    return await hybrid_chat(req.model_dump(exclude_none=True), s)

@app.post("/v1/images/generations", dependencies=[Depends(require_api_key)])
async def images(req: ImageRequest):
    result = await local_generation(s.local_image_base_url, s.local_image_api_key,
                                    "/v1/images/generations", req.model_dump(), s.ai_timeout_seconds)
    return JSONResponse(content=result) if isinstance(result, dict) else Response(result[0], media_type=result[1])

@app.post("/v1/audio/speech", dependencies=[Depends(require_api_key)])
async def speech(req: SpeechRequest):
    result = await local_generation(s.local_audio_base_url, s.local_audio_api_key,
                                    "/v1/audio/speech", req.model_dump(), s.ai_timeout_seconds)
    if isinstance(result, dict):
        return JSONResponse(content=result)
    return Response(result[0], media_type=result[1], headers={"Content-Disposition": "inline; filename=speech.mp3"})

@app.post("/v1/videos/generations", status_code=202, dependencies=[Depends(require_api_key)])
async def videos(req: VideoRequest, db: Session = Depends(get_db)):
    job_id = str(uuid.uuid4())
    job = Job(id=job_id, kind="video", status="queued", prompt=req.prompt,
              result_json=json.dumps({"model": req.model, "duration": req.duration}))
    db.add(job)
    db.commit()
    return {"id": job_id, "object": "video.job", "status": "queued",
            "message": "Demande mise en file. Consultez GET /v1/jobs/{id}."}

@app.get("/v1/jobs/{job_id}", dependencies=[Depends(require_api_key)])
async def job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return {"id": job.id, "type": job.kind, "status": job.status, "prompt": job.prompt,
            "provider_job_id": job.provider_job_id,
            "result": json.loads(job.result_json) if job.result_json else None,
            "error": job.error, "created_at": job.created_at.isoformat() if job.created_at else None}

@app.post("/v1/connectors/ms-digital-network/events", dependencies=[Depends(require_api_key)])
async def ms_digital_network_event(payload: dict = Body(...)):
    event = payload.get("event")
    data = payload.get("data", {})
    if not isinstance(event, str) or not event.strip() or not isinstance(data, dict):
        raise HTTPException(422, "Fournissez un événement texte et un objet data.")
    return await send_event(s.ms_dn_base_url, s.ms_dn_webhook_secret, event, data)

@app.get("/admin/runtime", dependencies=[Depends(require_admin_key)])
async def admin_runtime():
    """Probe configured self-hosted inference nodes without exposing their URLs or secrets."""
    result = {
        "mode": s.runtime_mode,
        "text": {"edge_configured": bool(s.local_text_base_url), "edge_reachable": False,
                 "edge_model": s.local_text_model, "cloud_configured": bool(s.cloud_text_base_url),
                 "cloud_reachable": False, "cloud_model": s.cloud_text_model},
        "media": {"image_configured": bool(s.local_image_base_url),
                  "audio_configured": bool(s.local_audio_base_url),
                  "video_configured": bool(s.video_api_url)},
    }
    timeout = httpx.Timeout(5.0)
    if s.local_text_base_url:
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(s.local_text_base_url.rstrip("/") + "/api/tags",
                    headers={"Authorization": f"Bearer {s.local_text_api_key}"} if s.local_text_api_key else {})
                result["text"]["edge_reachable"] = response.is_success
                if response.is_success:
                    names = [m.get("name") for m in response.json().get("models", [])]
                    result["text"]["edge_model_available"] = s.local_text_model in names or any(
                        name and name.split(":")[0] == s.local_text_model.split(":")[0] for name in names)
        except (httpx.HTTPError, ValueError):
            pass
    if s.cloud_text_base_url:
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(s.cloud_text_base_url.rstrip("/") + "/models",
                    headers={"Authorization": f"Bearer {s.cloud_text_api_key}"} if s.cloud_text_api_key else {})
                result["text"]["cloud_reachable"] = response.is_success
        except httpx.HTTPError:
            pass
    return result

@app.get("/admin/health", dependencies=[Depends(require_admin_key)])
async def admin_health(db: Session = Depends(get_db)):
    return {"status": "ok", "jobs": db.query(Job).count(),
            "queued": db.query(Job).filter(Job.status == "queued").count(),
            "environment": s.environment, "runtime": s.runtime_mode}
