import json, uuid
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.orm import Session
from .config import get_settings
from .db import initialize_database, get_db
from .models import Job
from .schemas import ChatRequest, ImageRequest, SpeechRequest, VideoRequest
from .security import require_api_key, require_admin_key
from .providers import compatible

s = get_settings()
initialize_database()
app = FastAPI(title=s.app_name, version="2.1.1", description="API MS NEXUS AI avec file vidéo sans quota applicatif")
app.add_middleware(CORSMiddleware, allow_origins=s.allowed_origins, allow_credentials=False,
                   allow_methods=["GET","POST"], allow_headers=["Authorization","Content-Type","X-Admin-Key"])

@app.get("/")
async def root():
    return {"name":s.app_name,"version":"2.1.1","docs":"/docs"}

@app.get("/health")
async def health():
    return {"status":"ok","service":"ms-nexus-api","version":"2.1.1"}

@app.get("/v1/models", dependencies=[Depends(require_api_key)])
async def models():
    return {"object":"list","data":[{"id":s.ai_text_model},{"id":s.ai_image_model},{"id":s.ai_audio_model},
            {"id":"video-default","available":bool(s.video_api_url and s.video_api_key),"queue":"unlimited-app-queue"}]}

@app.post("/v1/chat/completions", dependencies=[Depends(require_api_key)])
async def chat(req:ChatRequest):
    return await compatible.chat(req.model_dump(exclude_none=True))

@app.post("/v1/images/generations", dependencies=[Depends(require_api_key)])
async def images(req:ImageRequest):
    return await compatible.image(req.model_dump())

@app.post("/v1/audio/speech", dependencies=[Depends(require_api_key)])
async def speech(req:SpeechRequest):
    data,mime=await compatible.speech(req.model_dump())
    return Response(data,media_type=mime,headers={"Content-Disposition":"inline; filename=speech.mp3"})

@app.post("/v1/videos/generations", status_code=202, dependencies=[Depends(require_api_key)])
async def videos(req:VideoRequest, db:Session=Depends(get_db)):
    # No lifetime quota in the application: accepted requests are durably queued.
    job_id=str(uuid.uuid4())
    job=Job(id=job_id,kind="video",status="queued",prompt=req.prompt,
            result_json=json.dumps({"model":req.model,"duration":req.duration}))
    db.add(job); db.commit()
    return {"id":job_id,"object":"video.job","status":"queued",
            "message":"Demande mise en file. Consultez GET /v1/jobs/{id}."}

@app.get("/v1/jobs/{job_id}", dependencies=[Depends(require_api_key)])
async def job_status(job_id:str, db:Session=Depends(get_db)):
    job=db.get(Job,job_id)
    if not job: raise HTTPException(404,"Job not found")
    return {"id":job.id,"type":job.kind,"status":job.status,"prompt":job.prompt,
            "provider_job_id":job.provider_job_id,
            "result":json.loads(job.result_json) if job.result_json else None,
            "error":job.error,"created_at":job.created_at.isoformat() if job.created_at else None}

@app.get("/admin/health", dependencies=[Depends(require_admin_key)])
async def admin_health(db:Session=Depends(get_db)):
    return {"status":"ok","jobs":db.query(Job).count(),
            "queued":db.query(Job).filter(Job.status=="queued").count(),"environment":s.environment}
