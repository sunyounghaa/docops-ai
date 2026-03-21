# routers/qa.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.db import get_db
from schemas.qa import QARequestSchema, QAResponseSchema
from services.qa_service import QAService

router = APIRouter(prefix="/qa", tags=["qa"])


@router.post("", response_model=QAResponseSchema)
def answer_question(
    request: QARequestSchema,
    db: Session = Depends(get_db),
) -> QAResponseSchema:
    qa_service = QAService(db)
    return qa_service.answer_question(request)