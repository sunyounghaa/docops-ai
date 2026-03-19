# services/retrieval_service.py
from typing import Any

from sqlalchemy.orm import Session

from repositories.retrieval_repo import RetrievalRepository
from services.embedding_service import EmbeddingService
from utils.vector_utils import cosine_similarity, is_valid_vector


class RetrievalService:
    def __init__(
        self,
        db: Session,
        embedding_service: EmbeddingService | None = None,
    ):
        self.db = db
        self.retrieval_repo = RetrievalRepository(db)
        self.embedding_service = embedding_service or EmbeddingService()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        document_id: int | None = None,
    ) -> list[dict[str, Any]]:
        query_vector = self.embedding_service.generate_embedding(query)

        if not is_valid_vector(query_vector):
            raise ValueError("Invalid query embedding vector")

        candidates = self.retrieval_repo.get_indexed_chunks_with_embeddings(
            document_id=document_id
        )

        scored_results = []

        for candidate in candidates:
            chunk_vector = candidate["vector"]

            if not is_valid_vector(chunk_vector):
                continue

            if len(query_vector) != len(chunk_vector):
                continue

            try:
                score = cosine_similarity(query_vector, chunk_vector)
            except ValueError:
                continue

            scored_results.append(
                {
                    "chunk_id": candidate["chunk_id"],
                    "document_id": candidate["document_id"],
                    "content": candidate["content"],
                    "page_number": candidate["page_number"],
                    "chunk_index": candidate["chunk_index"],
                    "similarity_score": score,
                }
            )

        scored_results.sort(
            key=lambda item: item["similarity_score"],
            reverse=True,
        )

        return scored_results[:top_k]