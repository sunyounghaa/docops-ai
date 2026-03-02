# routers/chat.py
from fastapi import APIRouter, HTTPException
from uuid import uuid4

from schemas.chat_schema import ChatRequest, ChatResponse, Usage
from services.llm_service import generate_reply, OpenAIKeyMissingError, OpenAIUpstreamError

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    request_id = str(uuid4())
    session_id = request.session_id or str(uuid4())

    try:
        reply, usage = generate_reply(request.message)
    except OpenAIKeyMissingError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except OpenAIUpstreamError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    return ChatResponse(
        reply=reply,
        request_id=request_id,
        session_id=session_id,
        usage=Usage(**usage) if usage else None,
    )