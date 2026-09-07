# Meeting Summary (Generated via Standard Copilot Prompt)

**Status:** SYNTHETIC — written for prototyping only.
**Source meeting (fictional):** Follow-up clarification call between the Ops
KYC SME and the developer, held after the PDD/SDD above had already been
shared.

---

## Meeting Metadata
Date: (synthetic) — Attendees: Priya (Ops KYC SME), developer (automation
team) — Purpose: clarify a few open points before build starts on
KYC-Doc-Bot.

## Decisions Made
- Confirmed accepted ID document types remain passport and UK driving
  licence only for this phase.
- Confirmed the 25% shareholding threshold for EDD is fixed and not
  configurable per case.

## Process Steps (As Described)
- "Normally the customer uploads a scan or a phone photo of their passport
  — most people just take a picture of it on their phone and upload that."
- "Once we get a sanctions hit we usually just email the MLRO distribution
  list and wait to hear back, there's no fixed queue for it really."
- "If the Companies House lookup shows a different set of directors than
  what's on the form, normally I'd just go with whatever Companies House
  says since that's the official record."

## Business Rules & Exceptions Mentioned
- Hedge: "usually the photo upload is fine, but every so often someone
  uploads a screenshot of a screenshot and it's basically unreadable — we
  just email them and ask for a better one."
- Hedge: "in most cases the passport and the application form have the exact
  same name, but sometimes someone's changed their name or it's a maiden
  name thing, so we just use judgement."
- "If a case comes in on a Friday evening, it usually just sits until Monday,
  nobody works the weekend on this."
- "We don't really have a strict SLA for the sanctions escalation, it kind of
  depends how busy MLRO is."

## Terms & Definitions
- "KYC Verified" and "KYC Cleared" were both used in this call to mean the
  same status — flagging as the same concept, two labels used interchangeably.
- PSC = Persons with Significant Control (Companies House terminology).

## Explicit Assumptions Stated By Ops
- "Obviously if the document's expired we just bounce it back to the
  customer, that's not really a judgement call."
- "I'd assume if the name doesn't match at all the bot would just flag it,
  same as we would."

## Open Items / Unresolved Questions
- No agreed process yet for what happens if Companies House data conflicts
  with the application form's declared shareholding (beyond "go with
  Companies House").
- No agreed SLA or explicit hold state for cases waiting on MLRO response.
- Not discussed: what happens to a case if the customer never re-uploads a
  requested replacement document.

## Verbatim Quotes Worth Flagging
- "Most people just take a picture of it on their phone and upload that."
- "There's no fixed queue for it really" (re: MLRO escalation).
- "Normally I'd just go with whatever Companies House says" (re: director
  mismatch).
- "It kind of depends how busy MLRO is" (re: SLA).
