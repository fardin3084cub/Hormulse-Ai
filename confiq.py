"""
app/config.py — Centralized configuration via pydantic-settings
"""
 
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
 
 
class Settings(BaseSettings):
    # App
    env: str = "development"
    secret_key: str = "change-me-in-production"
    port: int = 8000
    app_name: str = "Hormulse AI"
 
    # Database
    database_url: str = "sqlite+aiosqlite:///./hormulse.db"
 
    # JWT
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
 
    # AI Provider Keys (all optional — fallback chain used)
    groq_api_key: Optional[str] = None
    google_gemini_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None
 
    # Redis (optional)
    redis_url: Optional[str] = None
 
    # Email (optional)
    sendgrid_api_key: Optional[str] = None
 
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
 
    @property
    def is_production(self) -> bool:
        return self.env == "production"
 
    def available_providers(self) -> list[str]:
        """Return list of configured AI providers."""
        providers = []
        if self.groq_api_key:         providers.append("groq")
        if self.google_gemini_api_key: providers.append("gemini")
        if self.openrouter_api_key:   providers.append("openrouter")
        if self.huggingface_api_key:  providers.append("huggingface")
        return providers
 
 
@lru_cache()
def get_settings() -> Settings:
    return Settings()
