# DocOps AI

LLM-powered FastAPI server with conversation persistence using SQLAlchemy.

This project implements a production-style architecture for building LLM-backed services, including layered separation (router -> service -> repository), database persistence, and session-based conversation management.

---

## 🚀 Overview

This server provides a chat API backed by OpenAI models and stores conversation history in SQLite.

Key capabilities:

- FastAPI-based REST API
- OpenAI LLM integration
- Conversation & Message data modeling
- SQLAlchemy 2.0 ORM
- Session-based chat persistence
- Clean architectural separation of concerns
- Swagger auto-generated API documentation

---

## 🛠 Tech Stack

- Python 3.13
- FastAPI
- Uvicorn
- OpenAI Python SDK
- pydantic-settings (Pydantic v2)
- SQLAlchemy 2.0
- SQLite

---

## 🧱 Architecture

Request lifecycle:

Router -> Service -> Repository -> Database

### Layer Responsibilities

**Router**
- HTTP handling
- Input validation
- Exception handling
- Response shaping

**Service**
- Chat orchestration logic
- Session management
- LLM invocation
- Persistence coordination

**Repository**
- Database CRUD abstraction
- SQLAlchemy query handling

**Models**
- Conversation / Message entity separation
- Foreign key relationships
- Token usage tracking

---

## 📂 Project Structure
```
docops-ai/
│
├── main.py
├── core/
│ └── settings.py
├── db/
│ └── base.py
│ └── session.py
│ └── init_db.py
├── dependencies/
│ └── db.py
├── models/
│ └── conversation.py
│ └── message.py
│ └── __init__.py
├── repositories/
│ └── conversation_repo.py
│ └── message_repo.py
├── routers/
│ └── chat.py
├── services/
│ └── chat_service.py
│ └── llm_service.py
├── schemas/
│ └── chat_schema.py
│ └── session_schema.py
├── requirements.txt
├── .env
└── README.md
```

---

## 🗃 Data Model

### Conversation

- `session_id` (public session identifier)
- `model`
- `created_at`
- `updated_at`

### Message

- `conversation_id` (FK -> conversations.id)\
- `role` (user / assistant / system / tool)
- `content`
- `request_id`
- `model`
- `prompt_tokens`
- `completion_tokens`
- `total_tokens`
- `created_at`

Both user and assistant messages are persisted per request.

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

### 4. Configure Environment Variable

Create `.env` file in project root:
```
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o-mini
OPENAI_TIMEOUT_SEC=30
APP_ENV=local
DATABASE_URL=sqlite:///./app.db
```

---

## ▶️ Run Server

```bash
python -m uvicorn main:app --reload
```

Swagger documentation:
```
http://127.0.0.1:8000/docs
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
### Chat

```
POST /chat
```

Request:
```json
{
    "message": "Hello",
    "session_id": null
}
```

If `session_id` is omitted or null, a new session is created.

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