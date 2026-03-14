# services/embedding_service.py
from openai import OpenAI
from sqlalchemy.orm import Session
from repositories.document_chunk_repo import DocumentChunkRepository
from repositories.chunk_embedding_repo import ChunkEmbeddingRepository
from models.chunk_embedding import ChunkEmbedding
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class EmbeddingService:

    def __init__(self, db: Session):
        self.db = db
        self.chunk_repo = DocumentChunkRepository(db)
        self.embedding_repo = ChunkEmbeddingRepository(db)

    def generate_embeddings(self, document_id: int):

        chunks = self.chunk_repo.get_chunks_by_document_id(document_id)

        for chunk in chunks:

            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=chunk.content
            )

            vector = response.data[0].embedding

            embedding = ChunkEmbedding(
                document_chunk_id=chunk.id,
                embedding_model="text-embedding-3-small",
                embedding_dimension=len(vector),
                vector=vector,
                status="completed"
            )

            self.embedding_repo.create_embedding(embedding)

        self.db.commit()