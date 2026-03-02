# DocOps AI

FastAPI 기반 LLM API 서버입니다.  
OpenAI API를 활용하여 간단한 채팅 응답을 제공하는 백엔드 서비스입니다.

---

## 🚀 Project Goal

- FastAPI 기반 API 서버 구축
- OpenAI LLM 연동
- 엔지니어링 구조 분리 (router / service / schema)

---

## 🛠 Tech Stack

- Python 3.13
- FastAPI
- Uvicorn
- OpenAI Python SDK
- pydantic-settings

---

## 📂 Project Structure
```
docops-ai/
│
├── main.py
├── core/
│ └── settings.py
├── routers/
│ └── chat.py
├── services/
│ └── llm_service.py
├── schemas/
│ └── chat_schema.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Setup

### 1. Clone

```bash
git clone <repository-url>
cd docops-ai
```

### 2. Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variable

Create `.env` file in project root:
```
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o-mini
OPENAI_TIMEOUT_SEC=30
APP_ENV=local
```

---

## ▶️ Run Server

```bash
python -m uvicorn main:app --reload
```

Server runs at:
```
http://127.0.0.1:8000
```

---

## 📡 API Endpoints

### Health Check

```
GET /health
```

Response:
```json
{
    "status": "ok"
}
```

---
### Chat Endpoint

```
POST /chat
```

Request:
```json
{
    "message": "Hello"
}
```

Response:
```json
{
  "reply": "Hello! How can I assist you today?",
  "request_id": "084e880f-1564-49f6-89d8-0f5ab3373e48",
  "session_id": "fc764c93-77fd-4849-bb5f-ff8c6c451798",
  "usage": {
    "prompt_tokens": 8,
    "completion_tokens": 9,
    "total_tokens": 17
  }
}
```
> Token usage is returned per request to support cost tracking and observability.
---

## 📌 Notes
- `.env` file is ignored via ```.gitignore```
- OpenAI API usage may incur costs
- Each request generates a unique  `request_id`
- Session-based design supports future RAG integration
- Token usage is returned for cost tracking