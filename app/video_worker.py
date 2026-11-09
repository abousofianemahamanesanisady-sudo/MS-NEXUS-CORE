import asyncio, json, logging
from sqlalchemy import select
from .config import get_settings
from .db import Base, engine, SessionLocal
from .models import Job
from .providers.video import submit

logging.basicConfig(level=logging.INFO)
log=logging.getLogger("ms-nexus-video-worker")
settings=get_settings()
Base.metadata.create_all(bind=engine)

async def process_one():
    with SessionLocal() as db:
        job=db.scalar(select(Job).where(Job.kind=="video",Job.status=="queued").order_by(Job.created_at).limit(1))
        if job is None: return False
        job.status="processing"
        db.commit()
        job_id=job.id
        prompt=job.prompt
        payload=json.loads(job.result_json or "{}")
        payload["prompt"]=prompt
    try:
        result=await submit(payload)
        with SessionLocal() as db:
            job=db.get(Job,job_id)
            if job:
                job.provider_job_id=str(result.get("id") or result.get("job_id"))
                job.status="submitted"
                job.result_json=json.dumps(result)
                db.commit()
        log.info("Video job %s submitted to provider",job_id)
    except Exception as exc:
        log.exception("Video job %s failed",job_id)
        with SessionLocal() as db:
            job=db.get(Job,job_id)
            if job:
                job.status="failed"
                job.error=str(exc)[:2000]
                db.commit()
    return True

async def main():
    delay=max(1,int(settings.model_fields.get("video_worker_poll_seconds").default or 3)) if "video_worker_poll_seconds" in settings.model_fields else 3
    log.info("MS NEXUS video worker started; polling every %s seconds",delay)
    while True:
        found=await process_one()
        if not found: await asyncio.sleep(delay)

if __name__=="__main__":
    asyncio.run(main())
