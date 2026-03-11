# repositories/document_repo.py
from sqlalchemy.orm import Session

from models.document import Document


class DocumentRepository:
    def create_document(
        self,
        db: Session,
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
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    def get_document_by_id(self, db: Session, document_id: int) -> Document | None:
        return db.query(Document).filter(Document.id == document_id).first()

    def update_document_status(self, db: Session, document: Document, status: str) -> Document:
        document.status = status
        db.commit()
        db.refresh(document)
        return document