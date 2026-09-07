# Meeting Summary Template

Paste this into Copilot (or any meeting assistant) after a requirements or
clarification call, with the transcript attached. The fixed schema is what
lets the detector consume every meeting consistently.

---

You are helping a developer capture requirements from a meeting about an
automation project. Read the attached transcript and produce a structured
summary using EXACTLY the following sections, in this order. Do not skip a
section — write "None mentioned" if nothing applies. Do not smooth over vague
or conditional language; if someone says "usually," "normally," "in most
cases," "typically," or similar hedge words, preserve that phrase verbatim
rather than turning it into a flat statement.

## Meeting Metadata
Date, attendees (name + role), stated purpose of the meeting.

## Decisions Made
Concrete decisions or confirmations reached during the meeting.

## Process Steps (As Described)
The process steps exactly as the ops/business person described them, in
order, preserving their own wording for how a human currently does each step
manually. Do not translate this into how the automation should do it.

## Business Rules & Exceptions Mentioned
Any rule, threshold, condition, or exception mentioned, even in passing.
Include hedge-word statements here, flagged as hedges.

## Terms & Definitions
Any domain term, system name, acronym, or internal label used, with whatever
definition was given. Flag if the same concept was referred to by two
different terms.

## Explicit Assumptions Stated By Ops
Anything said that reveals what ops assumes is obvious or always true from
their manual-process point of view.

## Open Items / Unresolved Questions
Anything left unresolved, deferred, or ended without a clear answer.

## Verbatim Quotes Worth Flagging
Direct quotes worth preserving exactly, particularly ones involving hedge
words, exceptions, or assumptions.

---

## Why the schema is fixed
Separating "Process Steps (As Described)" from "Business Rules & Exceptions"
is what lets the detector compare the human process against the automated
design and find the delta. Hedge-word preservation matters because "we
usually get a clean PDF" is where most missed automation exceptions live.
