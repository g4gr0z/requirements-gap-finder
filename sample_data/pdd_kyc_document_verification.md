# Process Definition Document

**Project:** Business Account Opening – KYC Document Verification
**Business area:** Meridian Bank, Business Banking Operations

> Sample document. Fictional scenario, no real customer or client data.

## 1. Process Overview
When a new business customer applies to open a business current account, the
Operations KYC team must verify the customer's identity documents and the
company's ownership structure before the account can be activated. This
document covers the document verification sub-process only.

## 2. As-Is Process (Manual)
1. Customer submits application via the Business Onboarding Portal, uploading:
   - A photo ID document (passport or UK driving licence) for each named
     director/beneficial owner.
   - A proof of business address (utility bill or lease, dated within 3 months).
   - A Companies House registration number.
2. An Ops analyst logs into the Portal queue and opens the next case.
3. The analyst opens each uploaded ID document and manually checks:
   - The document is one of the accepted types.
   - The name on the document matches the name entered on the application form.
   - The document is in date (not expired).
   - The document image is legible and not obviously tampered with.
4. The analyst looks up the company on Companies House to confirm registered
   directors and persons with significant control (PSC), and compares this
   against the shareholding percentages declared on the application form.
5. Any individual with more than 25% shareholding or voting rights is flagged
   for Enhanced Due Diligence (EDD).
6. The analyst runs a sanctions and PEP (Politically Exposed Person) screening
   check on each named individual via the internal Watchlist Screening tool.
7. If all checks pass, the analyst marks the case "KYC Verified" and the
   application moves to the Account Activation team.
8. If the sanctions screening returns a positive or partial match, the analyst
   escalates the case to the MLRO (Money Laundering Reporting Officer) team.

## 3. Business Rules
- Accepted ID document types: passport, UK photo driving licence.
- Proof of address must be dated within 3 months.
- >25% shareholding or voting control triggers EDD.
- Sanctions/PEP positive match triggers MLRO escalation.

## 4. Volumes & SLA
- Approx. 40–60 new business applications per day.
- Target: KYC verification completed within 1 business day of submission.
- Ops team operates Monday–Friday, 09:00–17:00.

## 5. Scope
**In scope:** Document type/legibility checks, name matching, Companies House
lookup, EDD flagging, sanctions/PEP screening, case status update.

**Out of scope:** Account activation, credit checks, ongoing periodic KYC
refresh (separate process).

## 6. Stakeholders
- Business Banking Operations (process owner)
- MLRO team (escalation recipient)
- IT/Automation team
