# services/chunking_service.py
class ChunkingService:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def create_chunks(self, pages: list[dict]) -> list[dict]:
        chunks: list[dict] = []
        chunk_index = 0

        for page in pages:
            page_number = page["page_number"]
            text = page["text"]

            page_chunks = self._split_text(text)

            for content in page_chunks:
                chunks.append(
                    {
                        "chunk_index": chunk_index,
                        "page_number": page_number,
                        "content": content,
                    }
                )
                chunk_index += 1

        return chunks

    def _split_text(self, text: str) -> list[str]:
        text = text.strip()
        if not text:
            return []

        chunks: list[str] = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= text_length:
                break

            start = end - self.chunk_overlap

        return chunks