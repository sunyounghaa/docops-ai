# db/init_db.py
from db.base_class import Base
from db.session import engine

from models.conversation import Conversation
from models.message import Message
from models.document import Document
from models.document_chunk import DocumentChunk
from models.chunk_embedding import ChunkEmbedding

def init_db() -> None:
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()