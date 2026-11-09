from __future__ import annotations

import httpx
from fastapi import HTTPException


def _headers(api_key: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {api_key}"} if api_key else {}


async def local_chat(payload: dict, settings) -> dict:
    """Call an Ollama-compatible local node. No commercial AI API is used."""
    if not settings.local_text_base_url:
        raise HTTPException(503, "Aucun moteur texte local n'est configuré. Déployez Ollama ou un nœud compatible.")
    body = dict(payload)
    body["model"] = settings.local_text_model if body.get("model") in (None, "", "default") else body["model"]
    body.pop("max_tokens", None) if body.get("max_tokens") is None else None
    if "max_tokens" in body:
        body["options"] = {"num_predict": body.pop("max_tokens")}
    try:
        async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
            response = await client.post(
                settings.local_text_base_url.rstrip("/") + "/api/chat",
                headers=_headers(settings.local_text_api_key),
                json={**body, "stream": False},
            )
            response.raise_for_status()
            result = response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(502, f"Nœud IA local en erreur ({exc.response.status_code}).") from exc
    except httpx.RequestError as exc:
        raise HTTPException(503, "Nœud IA local inaccessible. Vérifiez le réseau et le service Ollama.") from exc

    message = result.get("message", {})
    return {
        "id": result.get("id", "ms-nexus-local"),
        "object": "chat.completion",
        "model": result.get("model", body["model"]),
        "choices": [{"index": 0, "message": message, "finish_reason": "stop"}],
        "usage": {
            "prompt_tokens": result.get("prompt_eval_count", 0),
            "completion_tokens": result.get("eval_count", 0),
            "total_tokens": result.get("prompt_eval_count", 0) + result.get("eval_count", 0),
        },
        "runtime": "local",
    }


async def local_generation(base_url: str, api_key: str, path: str, payload: dict, timeout: int):
    if not base_url:
        raise HTTPException(503, f"Le moteur local demandé n'est pas encore configuré ({path}).")
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                base_url.rstrip("/") + path,
                headers=_headers(api_key),
                json=payload,
            )
            response.raise_for_status()
            content_type = response.headers.get("content-type", "application/json")
            if "application/json" in content_type:
                return response.json()
            return response.content, content_type
    except httpx.HTTPStatusError as exc:
        raise HTTPException(502, f"Nœud de génération local en erreur ({exc.response.status_code}).") from exc
    except httpx.RequestError as exc:
        raise HTTPException(503, "Nœud de génération local inaccessible.") from exc
