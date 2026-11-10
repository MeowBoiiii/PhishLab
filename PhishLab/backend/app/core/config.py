from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "PhishLab API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "temporary_dev_secret_key_change_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "phishlab_user"
    POSTGRES_PASSWORD: str = "phishlab_password"
    POSTGRES_DB: str = "phishlab"
    POSTGRES_PORT: int = 5432

    # URL bazy danych budowany dynamicznie lub nadpisywany ze zmiennych środowiskowych
    DATABASE_URL: str | None = None

    @property
    def sync_database_url(self) -> str:
        if self.DATABASE_URL:
            # Upewnij się, że używamy sterownika psycopg2
            url = self.DATABASE_URL
            if url.startswith("postgresql://") and not url.startswith("postgresql+psycopg2://"):
                url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
            return url
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # URL frontendowy do przekierowań edukacyjnych
    FRONTEND_URL: str = "http://localhost:5173"

    # Dozwolone domeny dla CORS (Frontend Maćka)
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

