# Solution Design Document

**Project:** Personal Loan – Approval Notification (Automation)

> Sample document. Fictional scenario, no real customer or client data.

## 1. Solution Summary
A UiPath automation ("LoanNotifyBot") will replace steps 1–5 of the manual
process defined in the PDD. The bot retrieves approved loans from the
Lending System, performs the pre-send checks, sends the notification email
with the offer letter attached, and updates the Notifications Tracker.

## 2. To-Be Workflow
1. **Trigger:** Bot runs every 30 minutes and calls the Lending System API
   for loans with status "Approved".
2. **Email present:** Bot checks the customer record has an email address
   and that it passes format validation.
3. **Amount match:** Bot compares the loan amount on the approval record
   against the amount on the customer's offer record; must match exactly.
4. **Offer letter present:** Bot checks the document store for the signed
   offer letter (PDF) filed under the loan reference.
5. **Threshold check:** Loans above £50,000 are skipped unless the
   Underwriting sign-off flag is set on the record.
6. **Send:** Bot sends the approval email from the shared Operations
   mailbox using the standard template, with the offer letter attached.
7. **Log:** Bot appends loan reference, timestamp and "BOT" to the
   Notifications Tracker.
8. **Failures:** Any failed check moves the loan to a "Notification Failed"
   queue and sends a summary email to the Underwriting team.

## 3. Inputs
- Approved loan records from the Lending System API (JSON).
- Signed offer letters from the document store (PDF).

## 4. Outputs
- Notification email to the customer.
- Row appended to the Notifications Tracker spreadsheet.
- Failure queue entries and Underwriting summary email.

## 5. Exception Handling
- Lending System API timeout → retry twice, then raise a System Exception
  per standard REFramework handling.
- Offer letter not found in the document store → "Notification Failed".
- Amount mismatch between records → "Notification Failed".
- Malformed email address → "Notification Failed".

## 6. Reusable Components
- `LendingSystem.GetApprovedLoans`
- `DocumentStore.RetrieveOfferLetter`
- `Outlook.SendTemplatedMail`

## 7. Assumptions
- Each approved loan is notified exactly once.
- Offer letters are always present in the document store as PDFs, filed
  under the loan reference.
