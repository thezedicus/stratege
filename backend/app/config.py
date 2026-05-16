from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url: str = "postgresql://stratege:stratege_pass@localhost:5432/stratege"
    openai_api_key: str = ""
    pagespeed_api_key: str = ""
    secret_key: str = "changeme"
    environment: str = "development"
    cors_origins: List[str] = ["http://localhost:3000", "https://stratege.vercel.app"]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
