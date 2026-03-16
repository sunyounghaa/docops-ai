# services/embedding_service.py
from __future__ import annotations

import os
from openai import OpenAI
from core.settings import settings

class EmbeddingService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"

    def generate_embedding(self, text: str) -> list[float]:
        cleaned_text = text.strip()
        if not cleaned_text:
            raise ValueError("Text is empty.")

        response = self.client.embeddings.create(
            model=self.model,
            input=cleaned_text,
        )

        return response.data[0].embedding