# core/settings.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1] # docops-ai 기준(필요 시 조정)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    OPENAI_API_KEY: str | None = None
    MODEL_NAME: str = "gpt-4o-mini"
    OPENAI_TIMEOUT_SEC: int = 30
    APP_ENV: str = "local"

    DATABASE_URL: str = f"sqlite:///{(BASE_DIR / 'app.db').as_posix()}"

    DOCUMENT_STORAGE_DIR: str(BASE_DIR / "storage" / "documents")

    MAX_HISTORY_MESSAGES: int = 20
    SYSTEM_PROMPT: str = "You are a helpful assistant."

settings = Settings()