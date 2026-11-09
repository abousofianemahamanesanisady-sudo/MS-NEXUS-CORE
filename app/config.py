from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "MS NEXUS AI"
    environment: str = "development"
    database_url: str = "sqlite:///./data/ms_nexus.db"
    msnexus_api_keys: str = "change-this-key"
    admin_api_key: str = "change-admin-key"
    ai_base_url: str = "https://api.openai.com/v1"
    ai_api_key: str = ""
    ai_text_model: str = "gpt-4o-mini"
    ai_image_model: str = "gpt-image-1"
    ai_audio_model: str = "gpt-4o-mini-tts"
    ai_audio_voice: str = "alloy"
    ai_timeout_seconds: int = 120
    video_api_url: str = ""
    video_api_key: str = ""
    video_timeout_seconds: int = 300
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    @property
    def api_keys(self): return {v.strip() for v in self.msnexus_api_keys.split(",") if v.strip()}
    @property
    def allowed_origins(self): return [v.strip() for v in self.cors_origins.split(",") if v.strip()]

@lru_cache
def get_settings(): return Settings()
