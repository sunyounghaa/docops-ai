# prompt/system_prompt.py
from core.settings import settings

def get_system_prompt() -> str:
    """
    Return the system prompt used for chat.
    """

    return settings.SYSTEM_PROMPT

