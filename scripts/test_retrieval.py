# scripts/test_retrieval.py
from db.session import SessionLocal
from services.retrieval_service import RetrievalService


def main():
    db = SessionLocal()
    try:
        service = RetrievalService(db)

        results = service.retrieve(
            query="What is the transformer architecture?",
            top_k=3,
            document_id=1,
        )

        for item in results:
            print("=" * 80)
            print("score:", item["similarity_score"])
            print("page:", item["page_number"])
            print("chunk_index:", item["chunk_index"])
            print("content:", item["content"][:300])
    finally:
        db.close()


if __name__ == "__main__":
    main()