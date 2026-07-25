# Submittal Package Audit (RMP Rev CG-Ready Checklist)

Before declaring an RMP (Risk Management Plan) submittal package ready for CG review, verify every item below.

## Package Contents

The submittal lives at `04_Registers/05_Submittle/REV{N}/` and must contain:

| File | Source | Notes |
|------|--------|-------|
| CRS (MOC-MUS-ASE-1K0-ZD-0093_CRS_RMP_Rev{N}.xlsx) | Generated from CG comment response | All comments Closed |
| Appendix A — PRR snapshot | Live server deployed file | Seq matches RMP doc |
| Appendix B — DDR snapshot | Same | — |
| Appendix C — HSE snapshot | Same | — |
| Appendix D — AVR snapshot | Same | — |

## Audit Checklist

### 1. RMP Document Alignment

| Check | What to Verify |
|-------|----------------|
| Appendix filenames | RMP Section 9 lists each appendix with filename (e.g. `EXP-RISK-PRR-2026-040_RevC12`). Confirm every file in `05_Submittle/REV{N}/` exactly matches. |
| Register counts | RMP Table 29 (Register Status Summary) shows per-register risk counts. Compare against actual JSON data — may drift between RMP revisions. |
| Rating distribution | RMP Table 5 (Risk Snapshot) shows Total/Critical/High/Medium/Low. Compare with register counts. If totals match but rating distribution differs, there's a scoring change not reflected in the RMP. |

### 2. CRS Resolution

| Check | What to Verify |
|-------|----------------|
| All comments Closed | Every CG comment row has status=Closed (column H) |
| Reply content | Originator Reply (column F) addresses the comment substantively |
| Risk ID cross-reference | If reply references a risk ID (e.g. PRR-PRC-06), verify the ID exists in the current register JSON |
| Reply accuracy | If reply says "risk entry PRR-PRC-XX covers [topic]", confirm the risk's title/cause/consequence actually describe that topic. If not, update the risk data before submitting. |

### 3. Risk Factor Coverage

RMP Section 2 (Project Risk Profile, Table 4) lists project-specific risk factors. Every factor should map to an active PRR entry:

| RMP Risk Factor | Example PRR ID |
|----------------|----------------|
| Tight Schedule | PRR-SCH-01 |
| Fire & Life Safety Blockers | PRR-FLS-01 |
| Design/MEP Mobilisation | PRR-DES-01, PRR-MEP-01 |
| Authority/Stramp Approvals | PRR-APP-04 |
| Commercial/EOT Exposure | PRR-COM-01 |
| Procurement Long Leads | PRR-PRC-06, PRR-PRC-02 |
| New MoC Object List | PRR-CNS-02 |
| Existing Building Conditions | PRR-SIT-01 |
| Museum-Grade Environment | PRR-CNS-01 |
| CG Review/NCR Backlog | PRR-DES-07 |
| **Middle East Shipping Disruption** | **PRR-PRC-06** (must mention Middle East/shipping in title or cause) |

### 4. CRS Comment 5 — Middle East Shipping (known CG focus area)

- CRS Comment 5 asks about long-lead/overseas procurement risk from Middle East shipping/logistics
- The reply must reference a specific PRR entry (PRR-PRC-06)
- PRR-PRC-06's title must explicitly mention "Middle East shipping" — the CRS reply claims this risk covers it, so the risk text must match
- If the risk was updated after the CRS was saved, re-download the snapshot for the submittal folder

### 5. Scoring Band Verification

Each register's ratings must match its RMP-documented scoring band — see `references/scoring-system-alignment.md` for full table and verification script:

| Register | Scale | Critical | High | Medium | Low |
|----------|-------|----------|------|--------|-----|
| PRR | PxS 4x4 | 12-16 | 8-11 | 4-7 | 1-3 |
| DDR | PxI 4x5 | 12-20 | 8-11 | 4-7 | 1-3 |
| HSE | CxL 5x5 | 16-25 | 10-15 | 5-9 | 1-4 |
| AVR | PxS 4x4 | 12-16 | 8-11 | 4-7 | 1-3 |

Common failure: applying 4x4 bands to HSE (score 16 → High) when 5x5 bands say 16 → Critical. Always use the per-register band table.

Import ratings vs server data — the web page may have stale data if the JSON source was updated but the HTML page wasn't rebuilt (DDR/HSE are static HTML, not auto-built like PRR/AVR).

### 6. Snapshot File Integrity

- All Excel files downloadable (HTTP 200) from live server
- Files have 644 permissions (not 700) — web server readability. rsync `-az` preserves source permissions; add `--chmod=644` or fix post-deploy.
- File version seq matches what RMP appendix section lists (minor filename date drift is normal — CG reviews content, not filenames)
- CRS file saved correctly (openpyxl can silently fail on merged-cell workbooks — check file size > 0)
