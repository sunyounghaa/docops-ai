# scripts/test_qa_api.py
import requests


def main() -> None:
    url = "http://127.0.0.1:8000/qa"
    payload = {
        "document_id": 1,
        "question": "이 문서에서 Transformer의 핵심 구조는 무엇인가요?",
        "top_k": 3,
    }

    response = requests.post(url, json=payload, timeout=30)

    print("status_code:", response.status_code)
    print("response:")
    print(response.json())


if __name__ == "__main__":
    main()