# DocOps AI – Project Journey

## 1. Project Goal

Build an LLM-powered backend system for document understanding.

Core capabilities:

- document upload and processing
- question answering via RAG
- extensibility for summarization and report generation

The focus of this project is not just feature implementation, but designing a scalable and explainable LLM backend architecture.

---

## 2. Phase 1 – Chat Backend

### What
- implemented FastAPI-based chat API
- added conversation persistence
- managed message history

### Why
LLM systems are inherently conversational.  
Managing context and message history is a fundamental requirement.

### Key Decision
Adopted layered architecture:

Router → Service → Repository → Database

---

## 3. Phase 2 – Document Processing Pipeline

### What
- document upload API
- PDF parsing
- text chunking
- storing chunks in database

### Why
RAG requires structured and retrievable document units.

### Challenge
- balancing chunk size vs context preservation
- handling PDF parsing reliability

---

## 4. Phase 3 – Embedding & Indexing

### What
- generated embeddings for document chunks
- stored embeddings in database

### Why
To enable semantic search over documents.

---

## 5. Phase 4 – Retrieval Layer

### What
- implemented cosine similarity-based retrieval
- top-k chunk selection

### Key Insight
Even a simple embedding + cosine similarity setup provides strong baseline retrieval performance.

---

## 6. Phase 5 – RAG Prompt Builder

### What
- transformed retrieved chunks into context
- designed grounded QA system prompt
- generated ChatCompletion messages

### Key Decision
- enforce context-based answering
- explicitly prevent hallucination

---

## 7. Phase 6 – RAG QA API

### What
End-to-end QA pipeline:

Question → Retrieval → Prompt → LLM → Answer

### Architecture Flow

Document → Chunk → Embedding → Retrieval → Prompt → Generate

### Result
Fully working RAG-based QA API with source attribution.

---

## 8. Phase 7 – Containerization (In Progress)

### What
- introduced environment-based configuration
- started Docker containerization

### Why
- remove local environment dependency
- prepare for cloud deployment (AWS EC2)

### Challenges
- missing dependencies (e.g., pypdf)
- separating config from code
- handling file storage paths

---

## 9. Lessons Learned

- LLM backend systems differ significantly from traditional CRUD systems
- prompt design directly impacts output quality
- retrieval quality determines overall system performance
- environment configuration should be externalized early
- containerization reveals hidden dependency issues

---

## 10. Next Steps

- complete Docker setup
- deploy to AWS EC2
- implement QA result persistence
- add token usage tracking
- improve source citation in answers