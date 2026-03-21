# schemas/qa.py
from pydantic import BaseModel, Field
from typing import List


class QARequestSchema(BaseModel):
    document_id: int = Field(..., description="Target document ID")
    question: str = Field(..., min_length=1, description="Question for the document")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of chunks to retrieve")


class QASourceSchema(BaseModel):
    chunk_id: int
    page_number: int | None = None
    chunk_index: int
    score: float
    content: str


class QAResponseSchema(BaseModel):
    document_id: int
    question: str
    answer: str
    sources: List[QASourceSchema]