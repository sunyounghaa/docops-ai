from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from dependencies.db import get_db
from schemas.document_schema import DocumentUploadResponse, DocumentIndexResponse
from services.document_service import upload_document
from services.indexing_service import IndexingService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
def upload_document_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    document = upload_document(db=db, file=file)
    return DocumentUploadResponse.model_validate(document)

@router.post("/{document_id}/index", response_model=DocumentIndexResponse)
def index_document(
    document_id: int,
    db: Session = Depends(get_db),
) -> DocumentIndexResponse:
    try:
        service = IndexingService(db)
        result = service.index_document(document_id)
        return DocumentIndexResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))