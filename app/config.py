from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "MS NEXUS AI"
    environment: str = "development"
    runtime_mode: str = "hybrid"
    database_url: str = "sqlite:///./data/ms_nexus.db"
    msnexus_api_keys: str = "change-this-key"
    admin_api_key: str = "change-admin-key"
    local_text_base_url: str = "http://ollama:11434"
    local_text_model: str = "llama3.2:3b"
    local_text_api_key: str = ""
    cloud_text_base_url: str = ""
    cloud_text_model: str = "Qwen/Qwen2.5-7B-Instruct"
    cloud_text_api_key: str = ""
    local_image_base_url: str = ""
    local_image_api_key: str = ""
    local_audio_base_url: str = ""
    local_audio_api_key: str = ""
    ai_timeout_seconds: int = 120
    video_api_url: str = ""
    video_api_key: str = ""
    video_timeout_seconds: int = 300
    video_worker_poll_seconds: int = 3
    ms_dn_base_url: str = ""
    ms_dn_webhook_secret: str = ""
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    @property
    def api_keys(self): return {v.strip() for v in self.msnexus_api_keys.split(",") if v.strip()}
    @property
    def allowed_origins(self): return [v.strip() for v in self.cors_origins.split(",") if v.strip()]

@lru_cache
def get_settings(): return Settings()
