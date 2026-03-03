# schemas/session_schema.py
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    role: str
    content: str

    request_id: str | None = None
    model: str | None = None

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    metadata_json: str | None = None
    created_at: datetime


class ConversationSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: str
    title: str | None = None
    model: str | None = None
    updated_at: datetime
    created_at: datetime


class ConversationDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: str
    title: str | None = None
    model: str | None = None
    system_prompt: str | None = None

    created_at: datetime
    updated_at: datetime

    messages: list[MessageOut]