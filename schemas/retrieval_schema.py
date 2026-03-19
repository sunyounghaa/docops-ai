# schemas/retrieval_schema.py
from pydantic import BaseModel


class RetrievalResultSchema(BaseModel):
    chunk_id: int
    document_id: int
    content: str
    page_number: int
    chunk_index: int
    similarity_score: float


class RetrievalResponseSchema(BaseModel):
    query: str
    top_k: int
    results: list[RetrievalResultSchema]