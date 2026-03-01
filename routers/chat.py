from fastapi import APIRouter
from schemas.chat_schema import ChatRequest, ChatResponse
from services.llm_service import generate_reply

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = generate_reply(request.message)
    return {"reply": reply}