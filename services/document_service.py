# services/document_service.py
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from core.settings import settings
from repositories.document_repo import DocumentRepository
from repositories.document_chunk_repo import DocumentChunkRepository
from services.document_parser_service import DocumentParserService
from services.chunking_service import ChunkingService

ALLOWED_EXTENSIONS = {".pdf"}

document_parser_service = DocumentParserService()
chunking_service = ChunkingService()


def upload_document(db: Session, file: UploadFile):

    document_repo = DocumentRepository()
    document_chunk_repo = DocumentChunkRepository(db)

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

    storage_dir = Path(settings.DOCUMENT_STORAGE_DIR)
    storage_dir.mkdir(parents=True, exist_ok=True)

    stored_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = storage_dir / stored_filename

    try:
        file_bytes = file.file.read()

        with file_path.open("wb") as buffer:
            buffer.write(file_bytes)

        document = document_repo.create_document(
            db=db,
            filename=file.filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
            file_type=file.content_type or "application/pdf",
            status="uploaded",
        )

        document_repo.update_document_status(db, document, "processing")

        pages = document_parser_service.extract_pdf_pages(str(file_path))
        chunks = chunking_service.create_chunks(pages)

        if chunks:
            document_chunk_repo.create_many(
                document_id=document.id,
                chunks=chunks,
            )

        document = document_repo.update_document_status(db, document, "processed")
        return document

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}",
        )