# repositories/conversation_repo.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.conversation import Conversation

class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_session_id(self, session_id: str) -> Conversation | None:
        stmt = select(Conversation).where(Conversation.session_id == session_id)
        return self.db.execute(stmt).scalar_one_or_none()
    
    def create(
            self,
            session_id: str,
            model: str | None = None,
            system_prompt: str | None = None,
            title: str | None = None,
    ) -> Conversation:
        conv = Conversation(
            session_id=session_id,
            model=model,
            system_prompt=system_prompt,
            title=title,
        )
        self.db.add(conv)
        self.db.commit()
        self.db.refresh(conv)
        return conv
    
    def touch(self, conversation: Conversation) -> None:
        # updated_at은 onupdate로 바뀌지만, SQLite/세션 상태에 따라 즉시 반영이 애매할 수 있어 커밋으로 확정
        self.db.add(conversation)
        self.db.commit()

    def list_recent(self, limit: int = 20, offset: int = 0) -> list[Conversation]:
        stmt = (
            select(Conversation)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.execute(stmt).scalars().all)