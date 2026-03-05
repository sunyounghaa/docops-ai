# repositories/message_repo.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.message import Message

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        request_id: str | None = None,
        model: str | None = None,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        total_tokens: int = 0,
        metadata_json: str | None = None,
    ) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            request_id=request_id,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            metadata_json=metadata_json,
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def list_by_conversation(
            self,
            conversation_id: str,
            limit: int = 50,
            offset: int = 0,
            order: str = "asc",
    ) -> list[Message]:
        stmt = select(Message).where(Message.conversation_id == conversation_id)
        if order == "desc":
            stmt = stmt.order_by(Message.created_at.desc())
        else:
            stmt = stmt.order_by(Message.created_at.asc())

        stmt = stmt.limit(limit).offset(offset)
        return list(self.db.execute(stmt).scalars().all())
    
    def list_recent_by_conversation(
    self,
    conversation_id: str,
    limit: int = 20
    ) -> list[Message]:

        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )

        messages = list(self.db.execute(stmt).scalars().all())

        # 시간순 reverse
        messages.reverse()

        return messages