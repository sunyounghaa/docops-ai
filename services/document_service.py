# services/document_service.py
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from core.settings import settings
from repositories.document_repo import create_document

ALLOWED_EXTENSIONS = {".pdf"}


def upload_document(db: Session, file: UploadFile):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing.",
        )

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed.",
        )

    storage_dir = Path(settings.document_storage_dir)
    storage_dir.mkdir(parents=True, exist_ok=True)

    stored_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = storage_dir / stored_filename

    try:
        file_bytes = file.file.read()

        with file_path.open("wb") as buffer:
            buffer.write(file_bytes)

        document = create_document(
            db=db,
            filename=file.filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
            file_type=file.content_type or "application/pdf",
            status="uploaded",
        )
        return document

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}",
        )