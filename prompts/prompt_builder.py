# prompt/prompt_builder.py
from core.settings import settings
from prompts.system_prompt import get_system_prompt

def apply_history_window(history):
    """
    Apply history windowing based on MAX_HISTORY_MESSAGES
    """
    max_messages = settings.MAX_HISTORY_MESSAGES
    return history[-max_messages:]

def build_chat_messages(history):
    """
    Construct messages for LLM chat completion.
    """

    windowed_history = apply_history_window(history)

    messages = [
        {
            "role": "system", 
            "content": get_system_prompt()}
    ]

    for m in windowed_history:
        messages.append(
            {
            "role": m.role,
            "content": m.content
            }
        )

    return messages