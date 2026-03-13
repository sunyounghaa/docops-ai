# db/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


# 모델 import 등록
from models.conversation import Conversation  # noqa: F401
from models.message import Message  # noqa: F401
from models.document import Document  # noqa: F401
from models.document_chunk import DocumentChunk  # noqa: F401
from models.chunk_embedding import ChunkEmbedding  # noqa: F401