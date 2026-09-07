"""Finds unresolved requirement gaps across a PDD, SDD and meeting summary."""

from typing import List

from pydantic import BaseModel, Field

from src.llm_provider import get_chat_model


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
        description='Which of "PDD", "SDD", "Meeting Summary" this gap draws '
        "from. Can be more than one."
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
before development starts. You will be given three documents about the same \
automation project:

1. PDD (Process Definition Document) -- how operations performs the process \
manually today.
2. SDD (Solution Design Document) -- how the automation is designed to \
replicate/replace that process.
3. Structured Meeting Summary -- notes from a requirements or clarification \
meeting with the operations subject matter expert.

Your job is NOT to summarize these documents. Your job is to find the GAPS \
between them -- specifically, places where:

- The manual process (PDD or meeting summary) relies on human judgement or \
"obviously" reasoning that the SDD has not translated into an explicit rule \
for the bot.
- The SDD defines automated behavior for one scenario, but the PDD/meeting \
summary reveals a related scenario or exception the SDD never addresses.
- The meeting summary contains hedge language ("usually," "normally," "in \
most cases," "typically," "generally"). These signal that ops is describing \
the common case and quietly leaving an uncommon case unaddressed. Treat \
these as HIGH PRIORITY.
- Two documents use different terms for what might be the same concept, or \
the same term is used inconsistently.
- A stated business rule has an edge case (a boundary condition, a conflict \
between two data sources, a timing/SLA gap) the SDD's design doesn't \
visibly handle.

For each gap, produce a question, a short rationale explaining the delta it \
exposes, which source document(s) it is grounded in, a supporting quote or \
close paraphrase, and whether a hedge word directly triggered it.

Do not invent scenarios that aren't grounded in the text. Do not restate a \
business rule as if it were a gap -- only flag it if there is a genuine \
unresolved ambiguity, conflict, or unaddressed exception. Prefer quality \
over quantity: 5-10 well-grounded gaps beats 20 generic ones.
"""

HUMAN_PROMPT_TEMPLATE = """\
## PDD (as-is manual process)
{pdd}

## SDD (to-be automated design)
{sdd}

## Structured Meeting Summary
{meeting_summary}
"""


def detect_gaps(
    pdd_text: str, sdd_text: str, meeting_summary_text: str
) -> GapAnalysisResult:
    model = get_chat_model()
    structured_model = model.with_structured_output(GapAnalysisResult)

    human_prompt = HUMAN_PROMPT_TEMPLATE.format(
        pdd=pdd_text, sdd=sdd_text, meeting_summary=meeting_summary_text
    )

    return structured_model.invoke(
        [("system", SYSTEM_PROMPT), ("human", human_prompt)]
    )
