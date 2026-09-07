# Expected Gaps — Answer Key (For Evaluating the Agent Later)

This is a ground-truth list, written by hand, of the clarifying questions a
sharp developer *should* raise after reading the PDD + SDD + meeting summary
together. Once milestone 2 (gap-detection core) is built, run it against the
three synthetic documents and compare its output to this list — this is how
we'll know if the agent is actually catching real gaps or just paraphrasing
the documents back.

Each entry cites which document(s) it's triangulated from.

1. **Photo-of-a-photo / unreadable uploads.** SDD says low OCR confidence
   (<80%) routes to Manual Review. Meeting summary reveals ops currently
   handles this by *emailing the customer* for a better copy — a resubmission
   loop the SDD never designs for. Question: does the bot re-open the case
   when the customer re-uploads, or does "Manual Review Required" become a
   dead end requiring a human to manually restart the bot's checks?
   *(SDD §5 vs. Meeting Summary "Process Steps")*

2. **Name-mismatch judgement calls.** SDD uses a 90% fuzzy-match threshold
   and treats anything below it as a failure. Meeting summary reveals ops
   currently uses human judgement for legitimate mismatches (maiden names,
   legal name changes) rather than a hard rule. Question: should below-90%
   matches always go to Manual Review, or does the bot need a way to accept
   a documented name-change reason?
   *(SDD §2 step 3 vs. Meeting Summary "Business Rules")*

3. **Companies House vs. application-form conflicts.** PDD/SDD assume the
   comparison is a simple flag-if->25%, but never state what happens when
   the *director/PSC list itself* differs between Companies House and the
   form (not just percentages). Meeting summary says ops "normally" defers
   to Companies House — but this was never written into the SDD as a rule.
   Question: should the bot auto-resolve conflicting director data by
   trusting Companies House, or must every conflict route to Manual Review?
   *(PDD §2 step 4, SDD §2 step 6, Meeting Summary "Process Steps")*

4. **MLRO escalation has no defined SLA or bot behavior while waiting.**
   SDD stops at "status → Escalated – MLRO Review." Meeting summary reveals
   there's no fixed queue or SLA on the ops side either. Question: does the
   bot need to poll for an MLRO decision and resume the case automatically,
   or is escalation a one-way handoff to a fully manual process from that
   point? This affects whether "Escalated" is a terminal bot state or needs
   a resume path.
   *(SDD §2 step 8 vs. Meeting Summary "Open Items")*

5. **Weekend/off-hours submissions.** PDD states Ops works Mon–Fri 9–5, and
   meeting summary confirms weekend cases "just sit." But the SDD's bot
   polls every 15 minutes with no mention of business-hours scheduling.
   Question: should the bot itself only run Mon–Fri, or is it fine for the
   bot to process cases 24/7 even though downstream Manual Review and MLRO
   escalation only get picked up during business hours (i.e., could create
   a backlog appearance)?
   *(PDD §4 vs. SDD §2 step 1)*

6. **"KYC Verified" vs "KYC Cleared" terminology conflict.** Meeting summary
   flags both terms used for what's presumably the same status, but the SDD
   only defines "KYC Verified." Question: confirm with ops/BA whether these
   are truly the same status or whether "Cleared" refers to a different
   downstream step (e.g., after Account Activation) — using the wrong one
   in the Portal status field could silently break a downstream integration.
   *(PDD §2 step 7 vs. Meeting Summary "Terms & Definitions")*

7. **Non-passport/licence document formats never explicitly rejected.**
   Ops mentions people uploading "a picture on their phone" — but neither
   document specifies bot behavior for unsupported file types (e.g. HEIC
   from an iPhone) versus a supported type that's simply low quality. These
   are different failure modes (format rejection vs. OCR confidence) but
   the SDD only designs for the latter.
   *(SDD §5 vs. Meeting Summary "Process Steps" & "Business Rules")*

8. **Abandoned cases (customer never re-uploads).** Explicitly listed as an
   open item in the meeting summary and never addressed in either document.
   Question: does a case in "Manual Review Required" ever time out or
   auto-close, or does it stay open indefinitely?
   *(Meeting Summary "Open Items")*

## What "good" looks like from the agent
A useful v1 doesn't need to find all 8 — but it should reliably catch the
ones anchored on a hedge word (#1, #2, #3, #7) since those are the clearest
signal, and it should be able to cite *which document(s)* each question came
from, the same way this answer key does. That citation is what makes the
tool trustworthy enough for a developer to actually act on its suggestions.
