# Contract Review from Outlook Email Attachment

Session: 2026-07-01 — ZNA Studio Lighting Consultancy Agreement.

## Trigger

User says "check emails related to X" then "yes and check the contract" — meaning extract the contract attachment from the latest relevant email(s) and produce a contract summary with red flags.

## Workflow

1. Query Outlook for emails matching the topic (subject, sender, or both).
2. Expand the full thread with `Conversation_ConversationID`.
3. Identify emails with attachments likely to contain the contract / fee proposal / SOW.
4. Extract attachments to `/tmp/<topic>_extracts/` using AppleScript; skip inline images (`image/*`).
5. List extracted files. Identify contract file (`.docx` or `.pdf`).
6. Read DOCX contract: `textutil -convert txt -stdout contract.docx` for overview; parse `word/document.xml` with Python for precise article extraction.
7. Read related PDFs (fee proposal, SOW approval, prequal approval) with `pdftotext`.
8. Build a structured summary.

## Contract Summary Template

| Section | Finding | Status |
|---|---|---|
| Parties | Client / Consultant names and registration details | Check placeholders |
| Recitals / Project | Contract No., project name, MoC, PMC/Lead Designer | Verify |
| Scope (Article 2) | Full services list; any scope limitations or overrides | Flag overrides |
| Contract Documents (Article 3) | List of schedules and appendices | Verify attached |
| Order of Precedence (Article 4) | Hierarchy; note Fee Proposal is subordinate | Verify |
| Deliverables (Article 5) | What the consultant must produce | Verify against register |
| Programme / Milestones (Article 6) | Durations, resource days, deadlines | Verify feasibility |
| Fees (Article 14 / Schedule 4) | Lump sums, optional stages, currency | Flag numeral/word mismatches |
| Payment Terms (Article 14) | Due dates, stop-work rights, VAT/WHT, bank charges | Verify |
| Payment Schedule (Schedule 5) | Milestones + percentages + amounts | **Often blank — flag** |
| Variations (Article 15) | Procedure, daily rates, no-reduction-by-fee-provision | Note |
| IPR (Article 16) | Licence vs assignment, moral rights | Note |
| Confidentiality (Article 17) | Period, permitted disclosures | Note |
| Insurance (Article 18) | PI, PL, EL limits and periods | **Often blank — flag** |
| Suspension (Article 19) | Notice periods, remobilisation costs | Note |
| Termination (Article 20) | Convenience vs cause vs non-payment | Note |
| Liability (Article 21) | Cap, excluded losses, carve-outs | **Cap often blank — flag** |
| Indemnity (Article 22) | Scope, notice/consent requirements | Note |
| Dispute Resolution (Article 23) | Arbitration seat / institution | Note |
| Governing Law (Article 24) | Jurisdiction | Note |
| Execution / Appendices | Signatures, notice details, daily rates, register of attached docs | Verify placeholders |

## Common Red Flags

- **Blank placeholders** in `[ • ]` form: effective date, CR numbers, addresses, insurance limits, liability caps, payment schedule amounts.
- **Fee numeral/word mismatch**: e.g., "£28,227" vs "twenty-two thousand, two hundred and twenty-seven" — must be reconciled before execution.
- **Payment Schedule (Schedule 5) not completed** even when a fee proposal exists.
- **Scope override**: contract expands scope beyond consultant's original proposal (e.g., "complete control engineering" overrides "design intent only"); confirm consultant accepted this in writing.
- **Mock-up / sample / commissioning cost ambiguity**: contract says consultant reviews mock-ups, but does not state who pays for fabrication/materials — flag for clarification.
- **Fee Proposal subordinate clause**: any conflict between Fee Proposal and Contract Documents resolved against Fee Proposal — ensure the consultant understands this.

## Example Output Language

User expects a concise findings table and a short list of gaps/action items. No prices beyond what is in the contract (user rule: no prices/monetary values except where directly quoting contract terms is necessary for the review).

## Tools Used

- `sqlite3` for Outlook query
- AppleScript + `osascript` for attachment extraction
- `textutil` for DOCX → text
- Python `zipfile` + `xml.etree.ElementTree` for structured DOCX parsing
- `pdftotext` for PDF fee proposals / approval forms
