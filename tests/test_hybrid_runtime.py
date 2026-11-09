import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from types import SimpleNamespace

from app.runtime.registry import list_models
from app.connectors.ms_digital_network import sign_payload


def test_model_registry_marks_unconfigured_media_nodes():
    settings = SimpleNamespace(
        local_text_model="llama3.2:3b", local_text_base_url="http://ollama:11434",
        local_image_base_url="", local_audio_base_url="", video_api_url="",
    )
    models = list_models(settings)
    by_modality = {item["modality"]: item for item in models}
    assert by_modality["text"]["configured"] is True
    assert by_modality["image"]["configured"] is False
    assert by_modality["audio"]["configured"] is False
    assert by_modality["video"]["configured"] is False


def test_ms_digital_network_signature_is_deterministic():
    payload = {"event": "profile.created", "data": {"user_id": "demo"}}
    headers, body = sign_payload(payload, "test-secret", timestamp=1700000000)
    assert headers["X-MS-Timestamp"] == "1700000000"
    assert headers["X-MS-Signature"].startswith("sha256=")
    assert b"profile.created" in body
