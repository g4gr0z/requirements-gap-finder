"""Streamlit front end. Run from the repo root: streamlit run app.py"""

import hmac
import os

import streamlit as st

from src.config import get_secret
from src.document_loader import SUPPORTED_TYPES, extract_text
from src.gap_detector import detect_gaps

SAMPLES = {
    "pdd": "sample_data/pdd_kyc_document_verification.md",
    "sdd": "sample_data/sdd_kyc_document_verification.md",
    "summary": "sample_data/meeting_summary_clarification_call.md",
}
TEMPLATE_PATH = "prompts/meeting_summary_template.md"

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


def read_file(path: str) -> str:
    return open(path, encoding="utf-8").read() if os.path.exists(path) else ""


def meeting_prompt() -> str:
    """Pull the copyable prompt body out of the template file."""
    parts = read_file(TEMPLATE_PATH).split("\n---\n")
    return parts[1].strip() if len(parts) > 2 else ""


def document_input(label: str, key: str, placeholder: str) -> str:
    uploaded = st.file_uploader(
        f"Upload {label}", type=SUPPORTED_TYPES, key=f"{key}_file"
    )

    if uploaded is not None:
        # Re-extract only when the file actually changes, not on every rerun
        marker = (uploaded.name, uploaded.size)
        if st.session_state.get(f"{key}_marker") != marker:
            text = extract_text(uploaded)
            st.session_state[f"{key}_marker"] = marker
            st.session_state[key] = text
            if not text.strip():
                st.warning(
                    f"No text found in {uploaded.name}. If it is a scanned "
                    "document, paste the content in manually."
                )

    return st.text_area(
        label,
        value=st.session_state.get(key, ""),
        height=260,
        placeholder=placeholder,
    )


st.title("Requirements Gap Finder")

start_tab, analyse_tab = st.tabs(["Start here", "Find gaps"])

with start_tab:
    st.subheader("What this does")
    st.markdown(
        "Operations describe a process the way a person performs it. The "
        "details that don't matter to a human — exceptions, edge cases, "
        "implicit validation, system-state assumptions — are exactly what "
        "automation needs, and they usually surface mid-build as rework.\n\n"
        "This reads your requirement documents together and returns the "
        "clarifying questions worth asking before development starts, each "
        "one cited back to the document and quote that raised it."
    )

    st.subheader("Using it on a live project")
    st.markdown(
        "**1. After each requirements or walkthrough meeting**, run the "
        "prompt below against the transcript in Copilot. The fixed structure "
        "matters — it is what lets the analysis compare the manual process "
        "against the automated design.\n\n"
        "**2. Save the output.** Paste it into the meeting summary box on "
        "the next tab.\n\n"
        "**3. Upload the PDD and SDD** as PDF or Word, or paste them in.\n\n"
        "**4. Review the questions** and take the ones that hold up into "
        "your next session with ops."
    )

    st.subheader("Prompt to run in Copilot after a meeting")
    prompt_text = meeting_prompt()
    if prompt_text:
        st.code(prompt_text, language="text")
    else:
        st.info(f"Prompt template not found at {TEMPLATE_PATH}.")

    st.subheader("Document formats")
    st.markdown(
        "- PDF, Word (.docx), Markdown and plain text can be uploaded "
        "directly. Word tables are read as well as body text.\n"
        "- **Confluence:** export the page (`•••` → Export → PDF or Word) "
        "and upload it, or copy the page content and paste it in.\n"
        "- Scanned PDFs have no text layer to read. If nothing comes "
        "through, paste the content manually."
    )

with analyse_tab:
    if st.button("Load sample documents"):
        for key, path in SAMPLES.items():
            st.session_state[key] = read_file(path)
            st.session_state.pop(f"{key}_marker", None)

    col1, col2, col3 = st.columns(3)

    with col1:
        pdd = document_input(
            "PDD", "pdd", "Paste the Process Definition Document..."
        )
    with col2:
        sdd = document_input(
            "SDD", "sdd", "Paste the Solution Design Document..."
        )
    with col3:
        summary = document_input(
            "Meeting summary", "summary",
            "Paste the structured meeting summary...",
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
                    st.markdown(
                        f"**Sources:** {', '.join(gap.source_documents)}"
                    )
                    st.markdown(f"> {gap.supporting_quote}")