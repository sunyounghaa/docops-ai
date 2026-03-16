# services/indexing_service.py
from __future__ import annotations

from sqlalchemy.orm import Session

from models.chunk_embedding import ChunkEmbedding
from repositories.document_repo import DocumentRepository
from repositories.document_chunk_repo import DocumentChunkRepository
from repositories.chunk_embedding_repo import ChunkEmbeddingRepository
from services.embedding_service import EmbeddingService


class IndexingService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.document_repo = DocumentRepository(db)
        self.chunk_repo = DocumentChunkRepository(db)
        self.embedding_repo = ChunkEmbeddingRepository(db)
        self.embedding_service = EmbeddingService()

    def index_document(self, document_id: int) -> dict:
        document = self.document_repo.get_by_id(document_id)
        if document is None:
            raise ValueError(f"Document not found: {document_id}")

        chunks = self.chunk_repo.get_by_document_id(document_id)
        if not chunks:
            raise ValueError(f"No chunks found for document: {document_id}")

        created_count = 0
        skipped_count = 0

        for chunk in chunks:
            existing = self.embedding_repo.get_by_chunk_id(chunk.id)
            if existing is not None:
                skipped_count += 1
                continue

            vector = self.embedding_service.generate_embedding(chunk.content)

            embedding = ChunkEmbedding(
                document_chunk_id=chunk.id,
                embedding_model=self.embedding_service.model,
                embedding_dimension=len(vector),
                vector=vector,
                status="completed",
            )

            self.embedding_repo.create_embedding(embedding)
            created_count += 1

        document.status = "indexed"
        self.db.commit()
        self.db.refresh(document)

        return {
            "document_id": document.id,
            "status": document.status,
            "created_embeddings": created_count,
            "skipped_embeddings": skipped_count,
        }