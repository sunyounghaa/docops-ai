# repositories/chunk_embedding_repo.py
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.chunk_embedding import ChunkEmbedding


class ChunkEmbeddingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_chunk_id(self, document_chunk_id: int) -> ChunkEmbedding | None:
        stmt = select(ChunkEmbedding).where(
            ChunkEmbedding.document_chunk_id == document_chunk_id
        )
        return self.db.scalar(stmt)

    def create_embedding(self, embedding: ChunkEmbedding) -> None:
        self.db.add(embedding)
        self.db.flush()