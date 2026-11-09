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
    """Describe built-in runtime routes; never advertise an unconfigured model as ready."""
    cards = [
        ModelCard(
            id=settings.local_text_model,
            modality="text",
            runtime="ollama-local",
            description="Modèle de langage exécuté sur une machine contrôlée par MS NEXUS AI.",
            configured=bool(settings.local_text_base_url),
        ),
        ModelCard(
            id="nexus-image-local",
            modality="image",
            runtime="self-hosted-image-node",
            description="Génération d'images via un nœud de diffusion auto-hébergé.",
            configured=bool(settings.local_image_base_url),
        ),
        ModelCard(
            id="nexus-audio-local",
            modality="audio",
            runtime="self-hosted-audio-node",
            description="Synthèse audio via un nœud audio auto-hébergé.",
            configured=bool(settings.local_audio_base_url),
        ),
        ModelCard(
            id="nexus-video-local",
            modality="video",
            runtime="self-hosted-video-node",
            description="Génération vidéo via un worker vidéo auto-hébergé.",
            configured=bool(settings.local_video_api_url),
        ),
    ]
    return [asdict(card) for card in cards]
