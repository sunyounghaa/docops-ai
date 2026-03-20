# prompts/rag_prompt_builder.py
from __future__ import annotations

from typing import Iterable

from prompts.rag_system_prompt import RAG_QA_SYSTEM_PROMPT
from schemas.retrieval import RetrievedChunkSchema


class RagPromptBuilder:
    def __init__(
        self,
        max_chunks: int = 5,
        max_context_chars: int = 6000,
    ) -> None:
        self.max_chunks = max_chunks
        self.max_context_chars = max_context_chars

    def build_messages(
        self,
        question: str,
        retrieved_chunks: Iterable[RetrievedChunkSchema],
    ) -> list[dict[str, str]]:
        context_text = self.build_context_text(retrieved_chunks)

        user_prompt = self._build_user_prompt(
            question=question,
            context_text=context_text,
        )

        return [
            {
                "role": "system",
                "content": RAG_QA_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

    def build_context_text(
        self,
        retrieved_chunks: Iterable[RetrievedChunkSchema],
    ) -> str:
        chunks = list(retrieved_chunks)[: self.max_chunks]

        if not chunks:
            return "No relevant document context was retrieved."

        sections: list[str] = []
        total_chars = 0

        for idx, chunk in enumerate(chunks, start=1):
            section = self._format_chunk_section(
                idx=idx,
                chunk=chunk,
            )

            if total_chars + len(section) > self.max_context_chars:
                break

            sections.append(section)
            total_chars += len(section)

        if not sections:
            return "No relevant document context was retrieved."

        return "\n\n".join(sections)

    def _format_chunk_section(
        self,
        idx: int,
        chunk: RetrievedChunkSchema,
    ) -> str:
        lines = [
            f"[Chunk {idx}]",
            f"Document ID: {chunk.document_id}",
            f"Chunk Index: {chunk.chunk_index}",
        ]

        if chunk.page_number is not None:
            lines.append(f"Page: {chunk.page_number}")

        if chunk.score is not None:
            lines.append(f"Similarity Score: {chunk.score:.4f}")

        lines.append("Content:")
        lines.append(chunk.content.strip())

        return "\n".join(lines)

    def _build_user_prompt(
        self,
        question: str,
        context_text: str,
    ) -> str:
        return f"""Document Context:
{context_text}

Question:
{question}

Instructions:
Answer the question using only the document context above.
If the answer is not supported by the context, say so clearly."""