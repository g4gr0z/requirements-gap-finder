"""Streamlit front end. Run from the repo root: streamlit run app.py"""

import hmac
import os

import streamlit as st

from src.config import get_secret
from src.document_loader import SUPPORTED_TYPES, extract_text
from src.gap_detector import ROLES, Document, detect_gaps

SAMPLES = {
    "business": "sample_data/pdd_kyc_document_verification.md",
    "design": "sample_data/sdd_kyc_document_verification.md",
    "meeting": "sample_data/meeting_summary_clarification_call.md",
}
HINTS = {
    "business": "PDD, BRD, SOPs, process maps, exception logs",
    "design": "SDD, DSD, technical specifications",
    "meeting": "One or more structured meeting summaries",
    "supporting": "Anything else: email threads, test cases, notes",
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


def extract_cached(uploaded) -> str:
    """Extract once per file, not on every rerun."""
    cache = st.session_state.setdefault("_extract_cache", {})
    marker = (uploaded.name, uploaded.size)
    if marker not in cache:
        cache[marker] = extract_text(uploaded)
    return cache[marker]


def role_input(role: str) -> list:
    """Render one role's uploader and paste box, return its Documents."""
    st.markdown(f"**{ROLES[role]}**")
    st.caption(HINTS[role])

    documents = []

    uploaded_files = st.file_uploader(
        "Upload files",
        type=SUPPORTED_TYPES,
        accept_multiple_files=True,
        key=f"{role}_files",
        label_visibility="collapsed",
    )
    for uploaded in uploaded_files or []:
        text = extract_cached(uploaded)
        if text.strip():
            documents.append(Document(uploaded.name, role, text))
        else:
            st.warning(
                f"No text found in {uploaded.name}. If it is a scanned "
                "document, paste the content in below."
            )

    pasted = st.text_area(
        "Or paste content",
        value=st.session_state.get(f"{role}_pasted", ""),
        height=180,
        key=f"{role}_area",
        label_visibility="collapsed",
        placeholder="Or paste content here...",
    )
    if pasted.strip():
        documents.append(Document(f"pasted {role} content", role, pasted))

    return documents


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
        "**2. Add your documents** on the next tab. Any number per group, "
        "uploaded or pasted. Later meetings can be added as they happen — "
        "a summary that contradicts an earlier document is itself a finding."
        "\n\n"
        "**3. Review the questions** and take the ones that hold up into "
        "your next session with ops."
    )

    st.subheader("Why documents are grouped")
    st.markdown(
        "The analysis works by contrasting how the work is done today "
        "against how the automation is designed to do it. Grouping keeps "
        "that contrast intact — a pile of undifferentiated documents would "
        "lose the axis the gaps are found along."
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
        for role, path in SAMPLES.items():
            st.session_state[f"{role}_pasted"] = read_file(path)
            st.session_state.pop(f"{role}_area", None)
        st.rerun()

    documents = []
    top_left, top_right = st.columns(2)
    with top_left:
        documents += role_input("business")
    with top_right:
        documents += role_input("design")

    bottom_left, bottom_right = st.columns(2)
    with bottom_left:
        documents += role_input("meeting")
    with bottom_right:
        documents += role_input("supporting")

    roles_present = {d.role for d in documents}

    if st.button("Find gaps", type="primary"):
        # The comparison needs both sides of the contrast to mean anything
        if "design" not in roles_present:
            st.warning("A solution design document is needed.")
        elif not roles_present & {"business", "meeting"}:
            st.warning(
                "At least one business/process document or meeting summary "
                "is needed to compare the design against."
            )
        else:
            with st.spinner("Analysing..."):
                try:
                    result = detect_gaps(documents)
                except Exception as e:
                    st.error(str(e))
                    st.stop()

            st.success(
                f"{len(result.gaps)} gaps found across "
                f"{len(documents)} documents"
            )

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