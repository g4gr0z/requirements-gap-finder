"""Secret resolution: environment first, Streamlit secrets as fallback."""

import os
from typing import Optional

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def get_secret(name: str) -> Optional[str]:
    value = os.environ.get(name)
    if value:
        return value

    # Fallback for Streamlit Cloud, where env vars aren't available
    try:
        import streamlit as st

        return st.secrets.get(name)
    except Exception:
        return None