from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": request.message}
        ]
    )
    return {
        "reply": response.choices[0].message.content
    }