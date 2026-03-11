# repositories/document_chunk_repo.py
from sqlalchemy.orm import Session

from models.document_chunk import DocumentChunk

class DocumentChunkRepository:
    def create_many(
            self,
            db: Session,
            *,
            document_id: int,
            chunks: list[dict],
    ) -> list[DocumentChunk]:
        chunk_objects = [
            DocumentChunk(
            document_id=document_id,
                chunk_index=chunk["chunk_index"],
                page_number=chunk.get("page_number"),
                content=chunk["content"],
            )
            for chunk in chunks
        ]

        db.add_all(chunk_objects)
        db.commit()

        for chunk_obj in chunk_objects:
            db.refresh(chunk_obj)

        return chunk_objects

    def list_by_document_id(self, db: Session, document_id: int) -> list[DocumentChunk]:
        return (
            db.query(DocumentChunk)
            .filter(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index.asc())
            .all()
        )

    def delete_by_document_id(self, db: Session, document_id: int) -> None:
        db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete()
        db.commit()