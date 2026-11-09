from pydantic import BaseModel, Field
from typing import Literal
class Message(BaseModel):
    role: Literal["system","user","assistant"]
    content: str = Field(min_length=1)
class ChatRequest(BaseModel):
    model: str = "default"
    messages: list[Message] = Field(min_length=1)
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int | None = Field(default=None, ge=1, le=32000)
class ImageRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    model: str = "default"
    size: str = "1024x1024"
    n: int = Field(default=1, ge=1, le=4)
class SpeechRequest(BaseModel):
    model: str = "default"
    input: str = Field(min_length=1, max_length=10000)
    voice: str = "alloy"
    response_format: str = "mp3"
class VideoRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    model: str = "default"
    duration: int = Field(default=5, ge=1, le=60)
