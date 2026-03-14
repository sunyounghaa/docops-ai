# repositories/document_chunk_repo.py
from sqlalchemy.orm import Session

from models.document_chunk import DocumentChunk


class DocumentChunkRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_many(
        self,
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

        self.db.add_all(chunk_objects)
        self.db.commit()

        for chunk_obj in chunk_objects:
            self.db.refresh(chunk_obj)

        return chunk_objects

    def list_by_document_id(self, document_id: int) -> list[DocumentChunk]:
        return (
            self.db.query(DocumentChunk)
            .filter(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index.asc())
            .all()
        )

    def delete_by_document_id(self, document_id: int) -> None:
        self.db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document_id
        ).delete()

        self.db.commit()

    def get_chunks_by_document_id(self, document_id: int) -> list[DocumentChunk]:

        return (
            self.db.query(DocumentChunk)
            .filter(DocumentChunk.document_id == document_id)
            .all()
        )