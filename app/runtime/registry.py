from __future__ import annotations
from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class ModelCard:
    id: str
    modality: str
    runtime: str
    description: str
    configured: bool

def list_models(settings) -> list[dict]:
    """Describe runtime routes; unconfigured modalities are never advertised as ready."""
    cards = [
        ModelCard(settings.local_text_model, "text", "ollama-edge", "Modèle open source exécuté sur un nœud contrôlé par MS NEXUS AI.", bool(settings.local_text_base_url)),
        ModelCard("nexus-image-local", "image", "self-hosted-image-node", "Génération via un nœud de diffusion auto-hébergé.", bool(settings.local_image_base_url)),
        ModelCard("nexus-audio-local", "audio", "self-hosted-audio-node", "Synthèse audio via un nœud auto-hébergé.", bool(settings.local_audio_base_url)),
        ModelCard("nexus-video-local", "video", "self-hosted-video-node", "Génération vidéo via un worker auto-hébergé.", bool(settings.video_api_url)),
    ]
    return [asdict(card) for card in cards]
