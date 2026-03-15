# models/chunk_embedding.py
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class ChunkEmbedding(Base):
    __tablename__ = "chunk_embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    document_chunk_id: Mapped[int] = mapped_column(
        ForeignKey("document_chunks.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    embedding_model: Mapped[str] = mapped_column(String, nullable=False)
    embedding_dimension: Mapped[int] = mapped_column(Integer, nullable=False)

    vector: Mapped[list] = mapped_column(JSON, nullable=True)

    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )