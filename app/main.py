import json, uuid
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.orm import Session
from .config import get_settings
from .db import Base, engine, get_db
from .models import Job
from .schemas import ChatRequest, ImageRequest, SpeechRequest, VideoRequest
from .security import require_api_key, require_admin_key
from .providers import compatible, video
s = get_settings(); Base.metadata.create_all(bind=engine)
app = FastAPI(title=s.app_name, version="2.0.0", description="API centrale MS NEXUS AI")
app.add_middleware(CORSMiddleware, allow_origins=s.allowed_origins, allow_credentials=False, allow_methods=["GET","POST"], allow_headers=["Authorization","Content-Type","X-Admin-Key"])
@app.get("/")
async def root(): return {"name":s.app_name,"version":"2.0.0","docs":"/docs"}
@app.get("/health")
async def health(): return {"status":"ok","service":"ms-nexus-api","version":"2.0.0"}
@app.get("/v1/models", dependencies=[Depends(require_api_key)])
async def models(): return {"object":"list","data":[{"id":s.ai_text_model},{"id":s.ai_image_model},{"id":s.ai_audio_model},{"id":"video-default","available":bool(s.video_api_url and s.video_api_key)}]}
@app.post("/v1/chat/completions", dependencies=[Depends(require_api_key)])
async def chat(req:ChatRequest): return await compatible.chat(req.model_dump(exclude_none=True))
@app.post("/v1/images/generations", dependencies=[Depends(require_api_key)])
async def images(req:ImageRequest): return await compatible.image(req.model_dump())
@app.post("/v1/audio/speech", dependencies=[Depends(require_api_key)])
async def speech(req:SpeechRequest):
    data,mime = await compatible.speech(req.model_dump()); return Response(data,media_type=mime,headers={"Content-Disposition":"inline; filename=speech.mp3"})
@app.post("/v1/videos/generations", dependencies=[Depends(require_api_key)])
async def videos(req:VideoRequest, db:Session=Depends(get_db)):
    result=await video.submit(req.model_dump()); jid=str(uuid.uuid4())
    job=Job(id=jid,kind="video",status=str(result.get("status","submitted")),prompt=req.prompt,provider_job_id=str(result.get("id") or result.get("job_id")),result_json=json.dumps(result))
    db.add(job); db.commit(); return {"id":jid,"object":"video.job","status":job.status,"provider_job_id":job.provider_job_id}
@app.get("/v1/jobs/{job_id}", dependencies=[Depends(require_api_key)])
async def job_status(job_id:str, db:Session=Depends(get_db)):
    job=db.get(Job,job_id)
    if not job: raise HTTPException(404,"Job not found")
    return {"id":job.id,"type":job.kind,"status":job.status,"prompt":job.prompt,"provider_job_id":job.provider_job_id,"result":json.loads(job.result_json) if job.result_json else None}
@app.get("/admin/health", dependencies=[Depends(require_admin_key)])
async def admin_health(db:Session=Depends(get_db)): return {"status":"ok","jobs":db.query(Job).count(),"environment":s.environment}
