# schemas/retrieval.py
from pydantic import BaseModel


class RetrievedChunkSchema(BaseModel):
    chunk_id: int
    document_id: int
    page_number: int | None = None
    chunk_index: int
    content: str
    score: float | None = None