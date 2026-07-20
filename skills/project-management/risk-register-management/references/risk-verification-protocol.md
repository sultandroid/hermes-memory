# Risk Register Verification Protocol

> One-by-one audit of every risk entry against repo evidence.
> Use when the user says "verify all risks" or "check facts one by one."

## Workflow

1. **Read the full risk register** (`01_Registers/risk_register.md`) — all 51+ risks
2. **Load reference files in parallel:**
   - `01_Registers/submittal_register.md` — real submission/approval dates
   - `01_Registers/drawing_register.md` — drawing status
   - `01_Registers/ncr_register.md` — NCR status
   - `01_Registers/rfi_register.md` — RFI/TQ status
   - `02_Schedule/master_programme.md` — schedule dates
   - `02_Schedule/submission_plan_risk_assessment.md` — submission plan
   - `Technical_Office/Specialist_Management/prequalification_log.md` — PQ status
   - `03_Plans/08_Risk/treatment/` — risk treatment files
3. **For each risk, verify:**
   - **Owner** — site/construction risks → Construction Manager, not Technical Office Mgr
   - **Dates** — must match actual submittal/approval records, not estimates
   - **Evidence column** — references must point to files that exist in the repo OR OneDrive/Aconex
   - **Status** — Open/Watch/Mitigated/Closed must match current reality
   - **P×S scores** — consistent with actual severity (Critical ≥12, High 8-11, Medium 4-7, Low ≤3)
   - **Factual claims** — every claim must be traceable to repo data (submittal codes, NCR numbers, meeting minutes refs)
4. **Report all discrepancies** with exact line numbers and recommended fixes

## Common Discrepancies Found in Practice

| Issue | Example | Fix |
|-------|---------|-----|
| Wrong owner | PRR-FLS-01: Technical Office Mgr | Change to Construction Manager |
| Evidence ref to non-existent file | DDR-STR-001, GAP-MAT-001 | These exist in OneDrive/Aconex, not the repo. Update evidence to note external location or create the file. |
| Excel formula in markdown | `=IF(J5>=12,"Critical",...)` | Replace with actual severity value (Critical/High/Medium/Low) |
| Stale RBS counts | Category says 8 but only 6 risks listed | Recalculate from actual risk IDs |
| Person name instead of role | "Eng. Shehab Elharbi (Rawasin)" | Use role title: "AV Lead" |
| Consolidated risk still counted | PRR-COM-05 merged into PRR-COM-01 but still counted | Remove merged ID from RBS count |

## Evidence Reference Resolution

When a risk's Evidence column references a file that doesn't exist in the repo:

1. **Search the repo** with `search_files` — if not found, it may be:
   - A OneDrive file (e.g. `DDR-STR-001` is a design risk register sheet, not a standalone file)
   - An Aconex transmittal reference
   - A file that was planned but never created
2. **If it's a OneDrive/Aconex reference**, note it in the evidence column: `"DDR-STR-001 (OneDrive — Design Risk Register sheet)"`
3. **If it genuinely doesn't exist**, flag it as a gap: `"GAP-STR-001 — file not created yet"`
4. **Never fabricate evidence** — if you can't find the source, say so

## Adel Darwish Bank Access

When evidence references point to files in "Adel Darwish's files" (OneDrive path: `Adel Darwish's files - 01- Execution Documents/`):

- Delegate file reading to a local agent that can access OneDrive
- The bank contains: meeting minutes, RFI logs, submittal registers, inspection reports
- Key sub-folders: `05- Request For Information-RFI/`, `06- Weekly Meeting MOM/`, `07- Submittal Log/`
- Files may be .xlsb format — use pyxlsb to read
- Cross-reference findings against the repo's markdown registers for consistency
