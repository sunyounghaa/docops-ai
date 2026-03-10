# repositories/document_repo.py
from sqlalchemy.orm import Session

from models.document import Document

def create_document(
        db: Session,
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