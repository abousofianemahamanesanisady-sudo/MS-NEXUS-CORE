from pydantic import BaseModel, Field

class KeyRequest(BaseModel):
    owner: str = Field(min_length=2, max_length=100)

class ImageRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=2000)
    width: int = Field(default=1024, ge=256, le=1536)
    height: int = Field(default=1024, ge=256, le=1536)
    steps: int = Field(default=25, ge=1, le=60)

class VideoRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=3000)
    duration_seconds: int = Field(default=5, ge=1, le=600)

class SpeechRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    voice: str = "default"
