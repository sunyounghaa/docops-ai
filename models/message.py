# models/message.py
import uuid
import json
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import String, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id: Mapped[str] = mapped_column(String(36), ForeignKey("conversations.id"), index=True, nullable=False)

    role: Mapped[str] = mapped_column(String(16), index=True, nullable=False)  # user | assistant | system | tool
    content: Mapped[str] = mapped_column(Text, nullable=False)

    request_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    model: Mapped[str | None] = mapped_column(String(64), nullable=True)

    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # JSON 컬럼을 SQLite에서 깔끔히 쓰려면 JSON1/버전 이슈가 있어서 일단 Text로 둠 (확장용)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")

    # 편의 메서드(선택)
    def set_metadata(self, data: dict[str, Any]) -> None:
        self.metadata_json = json.dumps(data, ensure_ascii=False)

    def get_metadata(self) -> dict[str, Any]:
        if not self.metadata_json:
            return {}
        return json.loads(self.metadata_json)
