"""LLM provider setup. Swapping providers means changing only this module."""

from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import get_secret

DEFAULT_MODEL = get_secret("GEMINI_MODEL") or "gemini-3.6-flash"


def get_chat_model(temperature: float = 0.2, model: str = DEFAULT_MODEL):
    api_key = get_secret("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Set it as an environment variable, in "
            ".env, or in .streamlit/secrets.toml."
        )

    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=temperature,
    )