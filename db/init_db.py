# db/init_db.py
from db.base import Base
from db.session import engine

from models.conversation import Conversation
from models.message import Message
from models.document import Document
from models.document_chunk import DocumentChunk

def init_db() -> None:
    Base.metadata.create_all(bind=engine)