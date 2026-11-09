# MS NEXUS AI Core — starter source

Base source for an independent AI platform with a public API, API-key authentication,
a model registry, and separate inference workers.

## Important reality check
This repository is the **starting source**, not a trained foundation model. It does not
bundle model weights. SDXL, Wan 2.1, Kokoro and Qwen are candidate open-weight starting
points; review each model's current license and usage conditions before deployment.
Running image/video/audio models requires suitable GPU compute and storage. A Cloudflare
Worker can expose/protect the API, but it cannot itself run large GPU models.

## Architecture
- `gateway/`: Cloudflare Worker API gateway (optional edge front door).
- `server/`: FastAPI service, API-key authentication, generation endpoints and model registry.
- `server/providers/`: local model adapters. Image adapter is a real Diffusers loading path;
  video/audio/text adapters are explicit integration points, not fake generation.
- `models.yaml`: model registry/configuration.
- `docker-compose.yml`: local API development only; it does not provide GPU/model weights.

## Run the API (development)
1. Install Python 3.11+ and dependencies in `server/requirements.txt`.
2. Set `NEXUS_ADMIN_KEY` and `NEXUS_DB_PATH`.
3. Run `uvicorn app.main:app --host 0.0.0.0 --port 8000` from `server/`.
4. Open `/docs`. Create a user/API key through the admin endpoint.
5. Set `NEXUS_IMAGE_MODEL_ID` to a locally downloaded SDXL model path or permitted model ID,
   install the GPU-compatible PyTorch/Diffusers build, and test image generation.

## API key management
For the first prototype, the admin endpoint creates user keys. Never expose the admin key
in an Android app or public client. In production, replace the bootstrap admin endpoint with
a verified account system, hashed key storage, quotas, abuse prevention, billing controls,
audit logs and key revocation.

## Endpoints
- `GET /health`
- `GET /v1/models`
- `POST /admin/keys` (admin only; bootstrap)
- `POST /v1/images/generations`
- `POST /v1/videos/generations` (returns 501 until a video worker is installed)
- `POST /v1/audio/speech` (returns 501 until a TTS worker is installed)
- `GET /v1/jobs/{job_id}`

## Public API rollout
Do not publish an unrestricted endpoint. Add HTTPS, authentication, per-key quotas,
request-size limits, moderation/safety checks, GPU queue limits, monitoring and a clear
acceptable-use policy before inviting the public.
