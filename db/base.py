# db/base.py
from db.base_class import Base

# 모델 import 등록
from models.conversation import Conversation  # noqa: F401
from models.message import Message  # noqa: F401
from models.document import Document  # noqa: F401
from models.document_chunk import DocumentChunk  # noqa: F401
from models.chunk_embedding import ChunkEmbedding  # noqa: F401