"""Streamlit front end. Run from the repo root: streamlit run app.py"""

import hmac
import os

import streamlit as st

from src.config import get_secret
from src.gap_detector import detect_gaps

SAMPLES = {
    "pdd": "sample_data/pdd_kyc_document_verification.md",
    "sdd": "sample_data/sdd_kyc_document_verification.md",
    "summary": "sample_data/meeting_summary_clarification_call.md",
}

st.set_page_config(page_title="Requirements Gap Finder", layout="wide")


def check_password() -> bool:
    expected = get_secret("APP_PASSWORD")

    # Fail closed: an unconfigured password must not leave the app open
    if not expected:
        st.error(
            "APP_PASSWORD is not configured. Set it as an environment "
            "variable or in Streamlit secrets before using this app."
        )
        return False

    if st.session_state.get("authenticated"):
        return True

    with st.form("login"):
        entered = st.text_input("Password", type="password")
        if st.form_submit_button("Enter"):
            # Constant-time comparison avoids leaking the password via timing
            if hmac.compare_digest(entered, expected):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    return False


if not check_password():
    st.stop()


st.title("Requirements Gap Finder")
st.caption(
    "Reads a PDD, an SDD and a structured meeting summary, and surfaces the "
    "clarifying questions likely to have been missed."
)


def read_sample(path: str) -> str:
    return open(path, encoding="utf-8").read() if os.path.exists(path) else ""


if st.button("Load sample documents"):
    for key, path in SAMPLES.items():
        st.session_state[key] = read_sample(path)

col1, col2, col3 = st.columns(3)

with col1:
    pdd = st.text_area(
        "PDD", value=st.session_state.get("pdd", ""), height=300,
        placeholder="Paste the Process Definition Document...",
    )
with col2:
    sdd = st.text_area(
        "SDD", value=st.session_state.get("sdd", ""), height=300,
        placeholder="Paste the Solution Design Document...",
    )
with col3:
    summary = st.text_area(
        "Meeting summary", value=st.session_state.get("summary", ""), height=300,
        placeholder="Paste the structured meeting summary...",
    )

if st.button("Find gaps", type="primary"):
    if not (pdd.strip() and sdd.strip() and summary.strip()):
        st.warning("All three documents are needed.")
    else:
        with st.spinner("Analysing..."):
            try:
                result = detect_gaps(pdd, sdd, summary)
            except Exception as e:
                st.error(str(e))
                st.stop()

        st.success(f"{len(result.gaps)} gaps found")

        # Hedge-anchored gaps first: they carry the strongest signal
        for i, gap in enumerate(
            sorted(result.gaps, key=lambda g: not g.is_hedge_anchored), 1
        ):
            with st.expander(f"{i}. {gap.question}", expanded=i <= 3):
                if gap.is_hedge_anchored:
                    st.markdown("`hedge-anchored`")
                st.markdown(gap.rationale)
                st.markdown(f"**Sources:** {', '.join(gap.source_documents)}")
                st.markdown(f"> {gap.supporting_quote}")