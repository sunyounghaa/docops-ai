# repositories/document_repo.py
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.document import Document


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(
        self,
        *,
        filename: str,
        stored_filename: str,
        file_path: str,
        file_type: str,
        status: str = "uploaded",
    ) -> Document:
        document = Document(
            filename=filename,
            stored_filename=stored_filename,
            file_path=file_path,
            file_type=file_type,
            status=status,
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_by_id(self, document_id: int) -> Document | None:
        stmt = select(Document).where(Document.id == document_id)
        return self.db.scalar(stmt)

    def update_status(self, document: Document, status: str) -> Document:
        document.status = status
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document