# repositories/retrieval_repo.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.document import Document
from models.document_chunk import DocumentChunk
from models.chunk_embedding import ChunkEmbedding

class RetrievalRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_indexed_chunks_with_embeddings(
        self,
        document_id: int | None = None,
    ) -> list[dict]:
        stmt = (
            select(
                DocumentChunk.id.label("chunk_id"),
                DocumentChunk.document_id,
                DocumentChunk.content,
                DocumentChunk.page_number,
                DocumentChunk.chunk_index,
                ChunkEmbedding.vector,
                ChunkEmbedding.embedding_model,
                ChunkEmbedding.embedding_dimension,
                ChunkEmbedding.status.label("embedding_status"),
            )
            .join(
                ChunkEmbedding,
                ChunkEmbedding.document_chunk_id == DocumentChunk.id,
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .where(Document.status == "indexed")
            .where(ChunkEmbedding.status == "completed")
        )

        if document_id is not None:
            stmt = stmt.where(DocumentChunk.document_id == document_id)

        rows = self.db.execute(stmt).all()

        results = []
        for row in rows:
            results.append(
                {
                    "chunk_id": row.chunk_id,
                    "document_id": row.document_id,
                    "content": row.content,
                    "page_number": row.page_number,
                    "chunk_index": row.chunk_index,
                    "vector": row.vector,
                    "embedding_model": row.embedding_model,
                    "embedding_dimension": row.embedding_dimension,
                    "embedding_status": row.embedding_status,
                }
            )

        return results