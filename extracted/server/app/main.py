import uuid
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from .db import init_db, connect
from .config import ADMIN_KEY, OUTPUT_DIR
from .security import require_admin, require_api_key, new_api_key, digest
from .schemas import KeyRequest, ImageRequest, VideoRequest, SpeechRequest
from .providers.image_sdxl import generate as generate_image
from .providers.not_ready import not_installed

app = FastAPI(
    title="MS NEXUS AI API",
    version="0.1.0",
    description="Independent model-serving API. Model weights run on infrastructure you control."
)

@app.on_event("startup")
def startup():
    init_db()
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

@app.get("/health")
def health():
    return {"service": "MS NEXUS AI", "status": "online", "version": "0.1.0"}

@app.get("/v1/models")
def models(owner: str = Depends(require_api_key)):
    return {"data": [
        {"id": "nexus-image-sdxl", "type": "image", "status": "adapter_available"},
        {"id": "nexus-video-wan", "type": "video", "status": "integration_required"},
        {"id": "nexus-audio-kokoro", "type": "audio", "status": "integration_required"},
        {"id": "nexus-text-qwen", "type": "text", "status": "integration_required"}
    ]}

@app.post("/admin/keys", dependencies=[Depends(require_admin)])
def create_key(body: KeyRequest):
    raw = new_api_key()
    with connect() as db:
        db.execute("INSERT INTO api_keys(key_hash, owner) VALUES(?,?)",
                   (digest(raw), body.owner))
    return {"owner": body.owner, "api_key": raw,
            "warning": "Copy this key now. It is stored as a hash and cannot be displayed again."}

@app.post("/v1/images/generations")
def image_generation(body: ImageRequest, owner: str = Depends(require_api_key)):
    try:
        path = generate_image(body.prompt, body.width, body.height, body.steps)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    return {"owner": owner, "model": "nexus-image-sdxl",
            "status": "completed", "file": f"/outputs/{Path(path).name}"}

@app.post("/v1/videos/generations", status_code=501)
def video_generation(body: VideoRequest, owner: str = Depends(require_api_key)):
    not_installed("Video")

@app.post("/v1/audio/speech", status_code=501)
def speech_generation(body: SpeechRequest, owner: str = Depends(require_api_key)):
    not_installed("Audio/TTS")

@app.get("/v1/jobs/{job_id}")
def get_job(job_id: str, owner: str = Depends(require_api_key)):
    with connect() as db:
        row = db.execute("SELECT * FROM jobs WHERE id=? AND owner=?",
                         (job_id, owner)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Job not found")
    return dict(row)
