# Meeting Summary — Loan Notification Follow-Up Call

> Sample document, generated using `prompts/meeting_summary_template.md`.
> Fictional scenario, no real customer or client data.

## Meeting Metadata
Attendees: Dan (Ops SME), Rachel (Underwriting), developer (automation team).
Purpose: follow-up on open points after the SDD was circulated.

## Decisions Made
- The bot will send from the shared Operations mailbox (confirmed again).
- Underwriting will continue to receive failures as a summary email rather
  than individual alerts.

## Process Steps (As Described)
- "Since April the sign-off threshold has been seventy-five thousand, not
  fifty — that changed when the delegated authority limits were revised."
- "If a loan comes in late on Friday it just waits, we pick it up Monday
  morning with the rest."
- "When something fails I don't always go back to it the same day, it
  depends what else is on."

## Business Rules & Exceptions Mentioned
- "The threshold is seventy-five thousand now. I think the PDD still says
  fifty, that wants updating."
- Hedge: "most of the time the tracker update and the email happen together,
  but if the spreadsheet's locked by someone else I just do it after."
- "There's no hard deadline on clearing the failed ones, within a couple of
  days is fine."

## Terms & Definitions
- "Notification Failed" queue and "exceptions list" were both used for the
  same thing during the call.

## Explicit Assumptions Stated By Ops
- "Obviously if underwriting hasn't signed off yet the customer shouldn't
  hear anything."

## Open Items / Unresolved Questions
- No agreed rule for what the bot should do with a loan that sits in the
  failed queue for more than a few days.
- Not discussed: whether the bot should re-check loans it previously
  skipped for missing underwriting sign-off, or whether someone re-submits
  them manually once signed off.

## Verbatim Quotes Worth Flagging
- "Since April the sign-off threshold has been seventy-five thousand, not
  fifty."
- "I think the PDD still says fifty, that wants updating."
- "If the spreadsheet's locked by someone else I just do it after."
