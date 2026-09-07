# Process Definition Document

**Project:** Personal Loan – Approval Notification
**Business area:** Meridian Bank, Personal Lending Operations

> Sample document. Fictional scenario, no real customer or client data.

## 1. Process Overview
Once a personal loan application is approved, Operations notifies the
customer by email and attaches their offer letter. This document covers the
notification step only, not the approval decision itself.

## 2. As-Is Process (Manual)
1. Each morning at 10:00, an Ops analyst exports the "Approved Loans" report
   from the Lending System, listing loans approved the previous working day.
2. For each loan on the report, the analyst checks:
   - A customer email address is present on the record.
   - The loan amount on the report matches the amount on the approval record
     in the Lending System.
   - The signed offer letter is present in the document store.
3. If all three checks pass, the analyst sends the customer the approval
   email using the standard template, attaching the offer letter.
4. The analyst records the loan reference, date sent and their initials in
   the Notifications Tracker spreadsheet.
5. If any check fails, the analyst emails the Underwriting team and leaves
   that loan out of the day's batch.

## 3. Business Rules
- Only loans with status "Approved" are notified.
- Loans above £50,000 require Underwriting sign-off before the notification
  is sent.
- Notification must be sent within 2 business days of approval.

## 4. Volumes & SLA
- Approx. 30–50 approvals per day.
- Ops team operates Monday–Friday, 09:00–17:30.

## 5. Scope
**In scope:** Report export, the three pre-send checks, sending the
notification email, tracker update, failure escalation to Underwriting.

**Out of scope:** The approval decision, offer letter generation, customer
responses to the notification.

## 6. Stakeholders
- Personal Lending Operations (process owner)
- Underwriting team (escalation recipient)
- IT/Automation team
