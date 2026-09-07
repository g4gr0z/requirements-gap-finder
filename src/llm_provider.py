"""LLM provider setup. Swapping providers means changing only this module."""

import os

from langchain_google_genai import ChatGoogleGenerativeAI

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")


def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    # Fallback for Streamlit Cloud, where env vars aren't available
    try:
        import streamlit as st

        key = st.secrets.get("GEMINI_API_KEY")
        if key:
            return key
    except Exception:
        pass

    raise RuntimeError(
        "GEMINI_API_KEY not found. Set it as an environment variable, in .env, "
        "or in .streamlit/secrets.toml."
    )


def get_chat_model(temperature: float = 0.2, model: str = DEFAULT_MODEL):
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=get_api_key(),
        temperature=temperature,
    )
