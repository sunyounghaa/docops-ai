from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from dependencies.db import get_db
from schemas.document_schema import DocumentUploadResponse
from services.document_service import upload_document

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
def upload_document_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    document = upload_document(db=db, file=file)
    return DocumentUploadResponse.model_validate(document)