# schemas/chat_schema.py
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    session_id: str | None = None

class Usage(BaseModel):
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None

class ChatResponse(BaseModel):
    reply: str
    request_id: str
    session_id: str
    usage: Usage | None = None