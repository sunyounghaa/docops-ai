# repositories/chunk_embedding_repo.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.chunk_embedding import ChunkEmbedding


class ChunkEmbeddingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        document_chunk_id: int,
        embedding_model: str,
        embedding_dimension: int,
        status: str = "pending",
    ) -> ChunkEmbedding:
        chunk_embedding = ChunkEmbedding(
            document_chunk_id=document_chunk_id,
            embedding_model=embedding_model,
            embedding_dimension=embedding_dimension,
            status=status,
        )
        self.db.add(chunk_embedding)
        self.db.commit()
        self.db.refresh(chunk_embedding)
        return chunk_embedding

    def get_by_chunk_id(self, document_chunk_id: int) -> ChunkEmbedding | None:
        stmt = select(ChunkEmbedding).where(
            ChunkEmbedding.document_chunk_id == document_chunk_id
        )
        return self.db.scalar(stmt)
    def create_embedding(self, embedding):
        self.db.add(embedding)