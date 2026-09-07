 # Solution Design Document

**Project:** Business Account Opening – KYC Document Verification (Automation)

> Sample document. Fictional scenario, no real customer or client data.

## 1. Solution Summary
A UiPath automation ("KYC-Doc-Bot") will replace steps 2–7 of the manual
process defined in the PDD. The bot polls the Business Onboarding Portal
queue, retrieves new cases, performs document checks via Document
Understanding, performs the Companies House and Watchlist Screening lookups,
and updates the case status.

## 2. To-Be Workflow
1. **Trigger:** Bot polls the Portal queue every 15 minutes for cases in
   status "Submitted."
2. **Document Extraction:** For each uploaded ID document, the bot uses the
   Document Understanding framework to classify the document type and extract:
   full name, date of birth, document expiry date, document number.
3. **Name Match:** Bot compares extracted name to the name field on the
   application form (fuzzy match, threshold 90%).
4. **Expiry Check:** Bot compares extracted expiry date to current system
   date; flags as failed if expired.
5. **Companies House Lookup:** Bot calls the Companies House public API with
   the registration number to retrieve current officers and PSC list.
6. **Shareholding Comparison:** Bot compares declared shareholding percentages
   from the application form against PSC data; any individual >25% is tagged
   `EDD_REQUIRED = true`.
7. **Sanctions Screening:** Bot logs into the Watchlist Screening tool (UI
   automation, no API available) and submits each named individual; captures
   the result (Clear / Positive / Partial).
8. **Status Update:** Bot writes the outcome back to the Portal case:
   - All checks pass → status "KYC Verified"
   - Sanctions screening Positive/Partial → status "Escalated – MLRO Review"
   - Any other failed check → status "Manual Review Required," routed to an
     Ops analyst queue with a note on which check failed.

## 3. Inputs
- Case record from Business Onboarding Portal (JSON via internal API).
- Uploaded documents (PDF/JPG/PNG, retrieved via Portal document store).

## 4. Outputs
- Updated case status in Portal.
- Structured log entry per case (case ID, checks performed, results,
  timestamp) written to the automation's SQL log table.

## 5. Exception Handling
- Document Understanding confidence below 80% on any extracted field → case
  routed to "Manual Review Required" with reason "Low OCR confidence."
- Companies House API timeout or no result → retry twice, then route to
  "Manual Review Required."
- Watchlist Screening tool UI element not found (selector failure) → retry
  once, then raise a System Exception per standard REFramework handling.

## 6. Reusable Components
- `DocumentUnderstanding.ExtractIDFields` (shared with other onboarding bots)
- `CompaniesHouseLookup.GetOfficersAndPSC`
- `WatchlistScreening.SubmitAndRetrieveResult`

## 7. Assumptions
- One case = one company; all directors/BOs are processed within the same
  transaction.
- Documents are uploaded before the bot's polling cycle picks up the case
  (no mid-cycle uploads handled).
