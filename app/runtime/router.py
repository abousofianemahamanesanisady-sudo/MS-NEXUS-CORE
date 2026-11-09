from __future__ import annotations

import httpx
from fastapi import HTTPException

from .local import local_chat


async def hybrid_chat(payload: dict, settings) -> dict:
    """Prefer edge Ollama; optionally fail over to a self-hosted cloud OpenAI-compatible node."""
    try:
        result = await local_chat(payload, settings)
        result["runtime"] = "edge"
        return result
    except HTTPException as edge_error:
        if not settings.cloud_text_base_url:
            raise edge_error
        headers = {"Authorization": f"Bearer {settings.cloud_text_api_key}"} if settings.cloud_text_api_key else {}
        body = dict(payload)
        if body.get("model") in (None, "", "default"):
            body["model"] = settings.cloud_text_model
        try:
            async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
                response = await client.post(
                    settings.cloud_text_base_url.rstrip("/") + "/chat/completions",
                    headers=headers,
                    json=body,
                )
                response.raise_for_status()
                data = response.json()
                data["runtime"] = "self-hosted-cloud"
                return data
        except httpx.HTTPStatusError as exc:
            raise HTTPException(502, f"Nœud cloud autonome en erreur ({exc.response.status_code}).") from exc
        except httpx.RequestError as exc:
            raise HTTPException(503, "Nœud cloud autonome inaccessible; le nœud edge a également échoué.") from exc
