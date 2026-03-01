from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

from fastapi import FastAPI
from routers.chat import router as chat_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(chat_router)