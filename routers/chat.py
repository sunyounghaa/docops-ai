# routers/chat.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies.db import get_db
from schemas.chat_schema import ChatRequest, ChatResponse, Usage
from services.chat_service import ChatService
from services.llm_service import OpenAIKeyMissingError, OpenAIUpstreamError

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    svc = ChatService(db)

    try:
        result = svc.chat(message=request.message, session_id=request.session_id)
    except OpenAIKeyMissingError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except OpenAIUpstreamError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    usage = result.get("usage") or {}
    return ChatResponse(
        reply=result["reply"],
        request_id=result["request_id"],
        session_id=result["session_id"],
        usage=Usage(**usage),
    )