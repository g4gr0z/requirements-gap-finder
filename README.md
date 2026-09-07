Requirements Gap Finder

An AI agent that ingests requirement artifacts (PDD, SDD, and a structured meeting summary) and proactively surfaces the clarifying questions a developer is likely to have missed before development starts — and gets better at it over successive engagements.

Why

On automation projects, operations teams describe a process from a manual, human point of view. Details that don't matter to a human doing the task (exception handling, edge cases, implicit validation, system-state assumptions) are exactly the details automation needs — and they tend to surface mid-development instead of during requirements gathering. This project tries to catch that gap earlier, by having an agent read the requirement documents specifically looking for the manual-vs-automation delta, and by building a growing checklist of gap patterns from past projects that new requirements get checked against.

How it works (planned architecture)
Structured intake — a standard prompt (see prompts/) pasted into Copilot after every requirements meeting, forcing a consistent summary schema instead of an unstructured recap. It deliberately preserves hedge-word language ("usually," "normally") since that's where most unhandled edge cases hide.
Gap-detection core — an LLM reasoning pass over the PDD + SDD + structured meeting summary together, comparing the manual process description against the automated solution design.
Growing checklist (RAG memory) — a vector store of gap patterns from past projects, tagged by project type, retrieved against new requirements for analogous questions. Grows via developer feedback and gaps logged after real development.
Web UI — upload documents, view ranked/cited questions, give feedback, browse the accumulated checklist.
