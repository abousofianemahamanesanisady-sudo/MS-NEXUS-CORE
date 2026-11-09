from pathlib import Path
from PIL import Image
from ..config import IMAGE_MODEL_ID, OUTPUT_DIR

_pipeline = None

def generate(prompt: str, width: int, height: int, steps: int) -> str:
    global _pipeline
    if not IMAGE_MODEL_ID:
        raise RuntimeError("Image model is not configured. Set NEXUS_IMAGE_MODEL_ID.")
    try:
        import torch
        from diffusers import StableDiffusionXLPipeline
    except Exception as exc:
        raise RuntimeError(f"Image runtime unavailable: {exc}") from exc

    if _pipeline is None:
        _pipeline = StableDiffusionXLPipeline.from_pretrained(
            IMAGE_MODEL_ID,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            use_safetensors=True
        )
        if torch.cuda.is_available():
            _pipeline = _pipeline.to("cuda")
        else:
            _pipeline = _pipeline.to("cpu")

    image = _pipeline(
        prompt=prompt, width=width, height=height, num_inference_steps=steps
    ).images[0]
    out = Path(OUTPUT_DIR)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"nexus-image-{__import__('secrets').token_hex(8)}.png"
    image.save(path)
    return str(path)
