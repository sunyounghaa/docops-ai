# main.py
from pathlib import Path

from fastapi import FastAPI
from routers.chat import router as chat_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(chat_router)