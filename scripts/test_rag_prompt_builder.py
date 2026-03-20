# scripts/test_rag_prompt_builder.py
from prompts.rag_prompt_builder import RagPromptBuilder
from schemas.retrieval import RetrievedChunkSchema


def test_with_chunks() -> None:
    print("\n=== TEST: WITH RETRIEVED CHUNKS ===\n")

    builder = RagPromptBuilder(max_chunks=3, max_context_chars=4000)

    retrieved_chunks = [
        RetrievedChunkSchema(
            document_id=1,
            page_number=3,
            chunk_index=9,
            content=(
                "The Transformer follows this overall architecture using "
                "stacked self-attention and point-wise fully connected layers."
            ),
            score=0.6018,
        ),
        RetrievedChunkSchema(
            document_id=1,
            page_number=2,
            chunk_index=8,
            content=(
                "The Transformer is the first transduction model relying "
                "entirely on self-attention without sequence-aligned RNNs."
            ),
            score=0.5331,
        ),
    ]

    question = "What is the core idea of the Transformer architecture?"

    messages = builder.build_messages(
        question=question,
        retrieved_chunks=retrieved_chunks,
    )

    _print_messages(messages)


def test_empty_chunks() -> None:
    print("\n=== TEST: EMPTY RETRIEVAL ===\n")

    builder = RagPromptBuilder()

    messages = builder.build_messages(
        question="What is the main idea?",
        retrieved_chunks=[],
    )

    _print_messages(messages)


def _print_messages(messages: list[dict[str, str]]) -> None:
    for idx, message in enumerate(messages, start=1):
        print("=" * 80)
        print(f"Message {idx}")
        print(f"role: {message['role']}")
        print("-" * 80)
        print(message["content"])
        print()


def main() -> None:
    test_with_chunks()
    test_empty_chunks()


if __name__ == "__main__":
    main()