# services/qa_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session

from prompts.rag_prompt_builder import RagPromptBuilder
from repositories.document_repo import DocumentRepository
from schemas.qa import QARequestSchema, QAResponseSchema, QASourceSchema
from schemas.retrieval import RetrievedChunkSchema
from services.llm_service import OpenAIKeyMissingError, OpenAIUpstreamError, generate_reply
from services.retrieval_service import RetrievalService


class QAService:
    def __init__(self, db: Session) -> None:
        self.document_repository = DocumentRepository(db)
        self.retrieval_service = RetrievalService(db)
        self.rag_prompt_builder = RagPromptBuilder()

    def answer_question(self, request: QARequestSchema) -> QAResponseSchema:
        document = self.document_repository.get_by_id(request.document_id)

        if document is None:
            raise HTTPException(
                status_code=404,
                detail=f"Document not found: {request.document_id}",
            )

        if document.status != "indexed":
            raise HTTPException(
                status_code=400,
                detail=f"Document is not indexed yet: {request.document_id}",
            )

        retrieved_results = self.retrieval_service.retrieve(
            query=request.question,
            top_k=request.top_k,
            document_id=request.document_id,
        )

        retrieved_chunks = [
            RetrievedChunkSchema(
                chunk_id=result["chunk_id"],
                document_id=result["document_id"],
                content=result["content"],
                page_number=result["page_number"],
                chunk_index=result["chunk_index"],
                score=result["similarity_score"],
            )
            for result in retrieved_results
        ]

        messages = self.rag_prompt_builder.build_messages(
            question=request.question,
            retrieved_chunks=retrieved_chunks,
        )

        try:
            answer, _usage = generate_reply(messages)
        except OpenAIKeyMissingError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except OpenAIUpstreamError as e:
            raise HTTPException(status_code=502, detail=str(e))

        sources = [
            QASourceSchema(
                chunk_id=chunk.chunk_id,
                page_number=chunk.page_number,
                chunk_index=chunk.chunk_index,
                score=chunk.score if chunk.score is not None else 0.0,
                content=chunk.content,
            )
            for chunk in retrieved_chunks
        ]

        return QAResponseSchema(
            document_id=request.document_id,
            question=request.question,
            answer=answer,
            sources=sources,
        )