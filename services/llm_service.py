# services/llm_service.py
from openai import OpenAI
from core.settings import settings

class OpenAIKeyMissingError(Exception): ...
class OpenAIUpstreamError(Exception): ...

_client: OpenAI | None = None

def get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise OpenAIKeyMissingError("OPENAI_API_KEY is missing.")
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client

def generate_reply(messages: list[dict]) -> tuple[str, dict | None]:
    client = get_client()

    try:
        resp = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=messages,
            timeout=settings.OPENAI_TIMEOUT_SEC,
        )
    except Exception as e:
        raise OpenAIUpstreamError(f"OpenAI request failed: {e}")
    
    reply = resp.choices[0].message.content or ""
    usage = None
    if getattr(resp, "usage", None):
        usage = {
            "prompt_tokens": getattr(resp.usage, "prompt_tokens", None),
            "completion_tokens": getattr(resp.usage, "completion_tokens", None),
            "total_tokens": getattr(resp.usage, "total_tokens", None),
        }
    return reply, usage