# core/config.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

APP_ENV = os.getenv("APP_ENV", "local")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "app.db"))

DOCUMENT_STORAGE_DIR = os.getenv(
    "DOCUMENT_STORAGE_DIR",
    str(BASE_DIR / "storage" / "documents")
)