# schemas/document_schema.py
from datetime import datetime

from pydantic import BaseModel, ConfigDict

class DocumentUploadResponse(BaseModel):
    id: int
    filename: str
    stored_filename: str
    file_path: str
    file_type: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)