# services/document_parser_service.py
from pypdf import PdfReader

class DocumentParserService:
    def extract_pdf_pages(self, file_path: str) -> list[dict]:
        reader = PdfReader(file_path)
        pages: list[dict] = []

        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            cleaned_text = self._clean_text(text)

            if not cleaned_text:
                continue

            pages.append(
                {
                    "page_number": index,
                    "text": cleaned_text,
                }
            )

        return pages

    def _clean_text(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines()]
        non_empty_lines = [line for line in lines if line]
        return "\n".join(non_empty_lines).strip()
