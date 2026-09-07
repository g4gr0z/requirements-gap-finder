"""Finds unresolved requirement gaps across a project's requirement documents."""

from dataclasses import dataclass
from typing import List

from pydantic import BaseModel, Field

from src.llm_provider import get_chat_model

# Document roles. The contrast between "how it works today" and "how the
# automation is designed to work" is the axis gaps are found along, so
# documents are grouped rather than pooled.
ROLES = {
    "business": "Business and process documents (how the work is done today)",
    "design": "Solution design (how the automation is intended to work)",
    "meeting": "Meeting notes and summaries",
    "supporting": "Supporting material",
}


@dataclass
class Document:
    name: str
    role: str
    text: str


class GapQuestion(BaseModel):
    question: str = Field(
        description="The precise question a developer should ask the ops SME "
        "or BA to resolve this gap before building it."
    )
    rationale: str = Field(
        description="1-2 sentences on the manual-vs-automation delta this "
        "exposes."
    )
    source_documents: List[str] = Field(
        description="The exact name(s) of the document(s) this gap draws "
        "from, copied from the document headings given in the input."
    )
    supporting_quote: str = Field(
        description="Short verbatim quote or close paraphrase from the source "
        "that triggered this question."
    )
    is_hedge_anchored: bool = Field(
        description="True if a hedge word (usually/normally/typically/in most "
        "cases/generally) directly triggered this question."
    )


class GapAnalysisResult(BaseModel):
    gaps: List[GapQuestion]


SYSTEM_PROMPT = """\
You are a senior RPA/automation developer performing a requirements review \
before development starts. You will be given the requirement documents for \
an automation project, grouped under headings by role:

- Business and process documents describe how the work is done manually \
today (PDD, BRD, SOPs, process maps, exception logs).
- Solution design documents describe how the automation is intended to \
work (SDD, DSD, technical specifications).
- Meeting notes and summaries capture requirements or clarification \
sessions with operations subject matter experts. There may be several, \
from different points in the project.
- Supporting material is anything else provided for context.

Your job is NOT to summarize these documents. Your job is to find the GAPS \
between them -- specifically, places where:

- The manual process relies on human judgement or "obviously" reasoning \
that the solution design has not translated into an explicit rule for the \
bot.
- The design defines automated behavior for one scenario, but another \
document reveals a related scenario or exception it never addresses.
- A document contains hedge language ("usually," "normally," "in most \
cases," "typically," "generally"). These signal that someone is describing \
the common case and quietly leaving an uncommon case unaddressed. Treat \
these as HIGH PRIORITY.
- Two documents use different terms for what might be the same concept, or \
the same term is used inconsistently.
- Two documents contradict each other, or a later meeting revises \
something an earlier document states, without the design being updated to \
match.
- A stated business rule has an edge case (a boundary condition, a conflict \
between two data sources, a timing/SLA gap) the design doesn't visibly \
handle.
- Operating windows, schedules, volumes and trigger frequencies stated in \
one document don't line up with those in another. Compare business hours, \
SLAs, polling intervals, batch timings and volumes across all documents \
explicitly, even where no one has quoted anything about them.
- A document lists something as open, unresolved, deferred, or "not \
discussed." Anything in that category is a gap by definition -- convert \
each one into a concrete question, even if it appears nowhere else.

For each gap, produce a question, a short rationale explaining the delta it \
exposes, the exact name(s) of the source document(s) it is grounded in as \
given in the headings, a supporting quote or close paraphrase, and whether \
a hedge word directly triggered it.

You may reason about how a described real-world behaviour manifests \
technically -- for example, a customer photographing a document on a phone \
implies file-format and image-quality variability the design may not \
handle -- provided the behaviour itself is described in the documents. Do \
not invent business scenarios, rules, systems or actors that are not \
described. Do not restate a business rule as if it were a gap: flag it only \
where there is a genuine unresolved ambiguity, conflict, or unaddressed \
exception.

List every distinct gap that meets that bar. Do not stop early, and do not \
merge two separate unresolved issues into one entry to keep the list short: \
if a scenario raises two different questions, each gets its own entry. A \
thorough review typically surfaces 8-12 genuine gaps. Before finalising, \
re-read the categories above and check the documents against each one in \
turn.
"""


def format_documents(documents: List[Document]) -> str:
    sections = []
    for role, heading in ROLES.items():
        in_role = [d for d in documents if d.role == role and d.text.strip()]
        if not in_role:
            continue
        sections.append(f"# {heading}")
        for doc in in_role:
            sections.append(f"## {doc.name}\n{doc.text}")
    return "\n\n".join(sections)


def detect_gaps(documents: List[Document]) -> GapAnalysisResult:
    model = get_chat_model()
    structured_model = model.with_structured_output(GapAnalysisResult)

    return structured_model.invoke(
        [("system", SYSTEM_PROMPT), ("human", format_documents(documents))]
    )