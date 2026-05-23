from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./stratege.db"  # fallback to SQLite if no PostgreSQL
    openai_api_key: str = ""
    pagespeed_api_key: str = ""
    secret_key: str = "changeme-set-in-env"
    environment: str = "development"
    # Comma-separated allowed origins — set via ALLOWED_ORIGINS env var in prod
    cors_origins: List[str] = ["http://localhost:3000"]
    allowed_origins: str = ""

    def get_cors_origins(self) -> List[str]:
        if self.allowed_origins:
            return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]
        return self.cors_origins

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
