# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.init_db import init_db
from routers.chat import router as chat_router
from routers.documents import router as documents_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_db()
    yield
    # shutdown (필요하면 여기에 정리 로직)

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(chat_router)
app.include_router(documents_router)