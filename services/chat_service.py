# services/chat_service.py
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from core.settings import settings
from repositories.conversation_repo import ConversationRepository
from repositories.message_repo import MessageRepository

from services.llm_service import generate_reply

from prompts.prompt_builder import build_chat_messages


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.conv_repo = ConversationRepository(db)
        self.msg_repo = MessageRepository(db)

    def chat(self, message: str, session_id: str | None) -> dict:
        request_id = str(uuid4())
        session_id = session_id or str(uuid4())

        # 1) conversation 가져오거나 생성
        conv = self.conv_repo.get_by_session_id(session_id)
        if not conv:
            conv = self.conv_repo.create(
                session_id=session_id,
                model=settings.MODEL_NAME,
            )

        # 2) user message 저장
        self.msg_repo.create_message(
            conversation_id=conv.id,
            role="user",
            content=message,
        )

        # history 조회
        history = self.msg_repo.list_recent_by_conversation(
            conversation_id=conv.id,
            limit=100,
        )

        # prompt 생성
        llm_messages = build_chat_messages(history)

        # LLM 호출
        reply, usage = generate_reply(llm_messages)
        usage = usage or {}

        # 4) assistant message 저장 (usage 포함)
        self.msg_repo.create_message(
            conversation_id=conv.id,
            role="assistant",
            content=reply,
            request_id=request_id,
            model=settings.MODEL_NAME,
            prompt_tokens=int(usage.get("prompt_tokens", 0) or 0),
            completion_tokens=int(usage.get("completion_tokens", 0) or 0),
            total_tokens=int(usage.get("total_tokens", 0) or 0),
        )

        # 5) updated_at 갱신
        conv.updated_at = datetime.now(timezone.utc)
        self.db.commit()

        return {
            "reply": reply,
            "request_id": request_id,
            "session_id": session_id,
            "usage": usage,
        }