# Subcontractor Contract / Appointment Status Verification

Use when the user asks "is X contracted yet?", "is X appointed?", "is the X contract done?", or "give me the X scope summary" for a subcontractor/specialist on Aseer Museum (or any Samaya project). The answer is a **status verdict**, not a scope analysis.

## The core distinction to nail

| State | Meaning | Evidence |
|-------|---------|----------|
| **Prequalifying** | Candidate, PQ submitted, not appointed | Specialist register status = "Prequalify"; no contract file |
| **PQ approved (Code B)** | CG approved candidate, but NO contract | PQ-XXXX Code B; "leading candidate" language |
| **In agreement / negotiation** | SOW being stamped, contract drafting | Emails about "stamp the SOW", "advance payment", "complete contracting procedures" |
| **Appointed / Contract signed** | Contract executed | Signed contract PDF in `00_Contracts/` or `01_Contracts/`; register status = "Appointed" |

**Do not assume "PQ approved" = "contracted".** PQ Code B is only prequalification approval. The contract is a separate, later step. The user's questions (TLC, ICT) were specifically about whether the contract was signed — the answer was "no" for TLC and "yes (just signed)" for ICT.

## Where to look (in priority order)

1. **Contract folders** — `00_Contracts/` and `01_Contracts/` (OneDrive project root). Look for `*Contract*.pdf`, `*Agreement*.pdf`, or a named subfolder (`01_Main_Contract`, `02_NRS_Contract`, `04_MEP_Contract`, etc.). A signed contract here = appointed.
2. **Specialist register** — `Technical_Office/Specialist_Management/specialist_register.md`. Status column: `Prequalify` vs `Appointed`. Notes column carries the leading candidate + PQ codes.
3. **Package register** — `01_Registers/subcontractor_package_register.md`. Look for "Track X appointment" / "appointment pending" language.
4. **Scope READMEs** — `03_Scope/<Firm>/README.md`. Often states appointment status explicitly (e.g. "contracting process still under negotiation").
5. **Subcontractor SOW RACI register** — `01_Registers/subcontractor_sow_raci_register.md`.
6. **NCR / risk registers** — a "delay in contracting with X" NCR (e.g. NC-1E0-0010 for ICT) confirms the contract was NOT done at that date; its closure signals appointment.

## Reading the contract PDF

Contract PDFs are often large and OneDrive throws `Resource deadlock avoided` on direct read. Workaround: `cp` to `/Volumes/MIcro/.pi-tmp/work/` first, then `pdfminer.high_level.extract_text()`.

Key fields to extract:
- **Date** (signature date — the single most important fact)
- **Parties** (who signed for each side)
- **Scope** (systems covered, RIBA stage / LOD limit)
- **Contract Price** (SAR, excl. VAT)
- **Payment schedule** (stages, %, amounts)
- **Exclusions** (e.g. "AV by others")

## Pitfalls

1. **Register may name a different firm than the signed contract.** On Aseer, the specialist register listed "SBS" as ICT SI, but the actual signed contract was with **SPS (Saudi Projects & Supplies Co.)**. Always read the contract PDF for the real party — don't trust the register's firm name.
2. **A contract dated "today/yesterday" is a live status change.** Check the signature date against the register's last_updated. A just-signed contract means the "in agreement" status is now stale — flag that the register needs updating.
3. **Email previews are truncated to ~255 chars** in Outlook.sqlite `Message_Preview`. For full bodies, the content is in the proprietary `Blocks` table (not decodable via sqlite). Use the preview + project registers + contract PDF to reconstruct, or ask the user to open the email.
4. **Contract PDFs in OneDrive can be 0-byte / corrupt** (sync issue). If `extract_text` fails with "No /Root object", the file didn't sync — re-sync or use the Micro-volume copy.
5. **Scope summary ≠ contract status.** When the user asks "give me the X scope summary", deliver the scope table AND the appointment status up front — they usually want to know whether it's contracted, not just what it covers.

## Example verdicts (Aseer, Aug 2026)

- **TLC (landscape)**: PQ-0127 Code B, design offer SAR 175k received, but **contract NOT signed** — "contracting process still under negotiation". → Prequalifying/negotiation.
- **ICT (SPS)**: contract **signed 15/08/2026**, SAR 106,050, RIBA Stage 4/LOD 300. → Appointed. Closes NCR NC-1E0-0010 + risk C-056.
- **Structural**: not appointed, DD rejected twice (Code C), quotation received. → Prequalifying.
