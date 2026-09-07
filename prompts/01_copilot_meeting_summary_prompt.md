# Standard Prompt: Requirements Meeting → Structured Summary

Paste this into Copilot right after any requirements-gathering or follow-up meeting
(the walkthrough, PDD/SDD review, or any clarification call). Attach or paste the
transcript/notes first, then this prompt. The fixed schema is what lets the gap-finder
agent consume every meeting consistently, no matter who ran it or how rambling it was.

---

**PROMPT TO PASTE INTO COPILOT:**

> You are helping a developer capture requirements from a meeting about an automation
> project. Read the attached transcript/notes and produce a structured summary using
> EXACTLY the following sections, in this order. Do not skip a section — write "None
> mentioned" if nothing applies. Do not smooth over vague or conditional language; if
> someone says "usually," "normally," "in most cases," "typically," or similar hedge
> words, preserve that phrase verbatim rather than turning it into a flat statement —
> those hedges usually mean an unhandled edge case.
>
> ## Meeting Metadata
> Date, attendees (name + role, e.g. "ops SME" / "developer" / "BA"), stated purpose of
> the meeting.
>
> ## Decisions Made
> Concrete decisions or confirmations reached during the meeting. Bullet list, one
> decision per line.
>
> ## Process Steps (As Described)
> The process steps exactly as the ops/business person described them, in order,
> preserving their own wording for how a human currently does each step manually.
> Do not translate this into "how the bot should do it" — capture the human process
> as told.
>
> ## Business Rules & Exceptions Mentioned
> Any rule, threshold, condition, or exception case that was mentioned, even in
> passing. Include hedge-word statements here too (e.g. "usually the document is a
> PDF" belongs here, flagged as a hedge).
>
> ## Terms & Definitions
> Any domain term, system name, acronym, or internal label used, with whatever
> definition or context was given. Flag if the same concept was referred to by two
> different terms in the meeting (e.g. "KYC refresh" vs "new KYC").
>
> ## Explicit Assumptions Stated By Ops
> Anything ops said that reveals what they assume is "obvious" or "always true" from
> their manual-process point of view (e.g. "well obviously if it's not signed we just
> send it back").
>
> ## Open Items / Unresolved Questions
> Anything left unresolved, deferred, or where the meeting ended without a clear
> answer.
>
> ## Verbatim Quotes Worth Flagging
> Any direct quotes that seem important to preserve exactly as said, particularly
> ones involving hedge words, exceptions, or assumptions.

---

### Why this shape
- Fixed sections = reliable input for the gap-finder agent — no guessing what a
  "summary" contains this time.
- Separating "Process Steps (As Described)" from "Business Rules & Exceptions" is
  what lets the agent later compare the human/manual view against the automated
  SDD view and spot the delta.
- Hedge-word preservation is doing a lot of work: in practice, "we usually get a
  clean PDF" is where most missed automation exceptions live.
