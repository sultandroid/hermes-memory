# NRS EV Session — 03 Jun 2026 (Updated Rev 02, Scenario B)

## Data Points (frozen)

| Field | Value |
|---|---|
| Contract total | SAR 1,209,000 |
| Stage 4 (IFC Package) | SAR 768,000 (63.5%) |
| Stage 5 (Off-site Fab Review) | SAR 270,000 (22.3%) |
| Stages 5-6 (On-site Fab Review) | SAR 171,000 (14.2%) |
| Advance 10% | SAR 120,900 (INV-4755) |
| Stage 4 advance share | 10% × 768K = 76,800 |
| Stage 4 net balance | 768K - 76,800 = 691,200 |

## Payment Ledger

| INV | Amount | SAR | Paid Date | Proof |
|---|---|---|---|---|
| INV-4755 (Advance) | EUR 26,548.67 @ 4.5539 | 120,900 | 25 Feb 2026 | Nissen Richards Studio 10.pdf |
| INV-4781 (Stage 4 1/2) | EUR 76,334.19 @ 4.5196 | 345,600 | 4 May 2026 | Nissen Richards Studio 781.pdf |
| INV-4805 (Stage 4 2/2) | EUR 77,019.08 @ 4.4872 | 345,600 | 17 May 2026 | Nissen Richards Studio 805.pdf |
| **Total AC** | | **812,100** | | |
| INV-4825 (Stage 5 1/3) | Due 11 Jun 2026 | 90,000 | DUE | — |

## Brackets (user-agreed)

| Component | % of Stage 4 | Value | Status |
|---|---|---|---|
| Architecture DD | 70% | 538K | 75/25 SPLIT — 404K standalone + 17K coord-dependent |
| Specialist review (Design Lead) | 15% | 115K | PARTIAL — 12.3% items (13% value) |
| IFC production | 15% | 115K | BLOCKED by SI007 |
| Coordination | 0% | 0 | Done by Samaya |

## EV Calculation — Scenario B (Final)

| EV Component | Value | Method |
|---|---|---|
| DD — Standalone (75% × 538K) | 403.5K | Unconditional — drawing delivery |
| DD — Coordination-dependent (25% × 538K × 13%) | 16.5K | Tracks specialist progress |
| **Subtotal DD** | **420K** | |
| Specialist review (13% × 115K, effort-weighted) | 15K | 5/13 packages, 45/365 items |
| Stage 5 shop dwg reviews (17.4% × 270K) | 47K | 27 showcase + 7 AV dwgs reviewed |
| **Total EV** | **483K** | |
| **AC** | **812K** | |
| **CV** | **-329K (CPI=0.59)** | |
| **SV** | **-131K (SPI=0.79)** | |

## User-Questioned EV Logic (this session)

User asked: "Did you see the percentage we give to DD done against the efforts remaining with specialists? Is this logic correct?"

**Analysis: Claiming 100% DD EV (538K) while specialist coordination is at 13% progress is aggressive.** DD drawings feed into specialist coordination — NRS may need to revise them after specialist inputs.

**Recommendation from Claude (Scenario B — 75/25 split):**
- Unconditional (75%): 404K — standalone architectural output that won't change
- Coordination-dependent (25%): 17K at current specialist progress — will fill up as coordination advances
- Result: DD EV 421K, Total EV 483K, CV -329K (from -212K)

Full analysis: `Docs/07_Reports/07.5 Audit Report/NRS/NRS_EV_Scenario_Analysis.md`

## Specialist Packages — Item Counts

| Package | Total | NRS Reviewed | % | EV |
|---|---|---|---|---|
| SLF / Life Safety / Fire | 20 | 6 | 30.0% | ~2K |
| Showcases (Glasbau Hahn) | 73 | 23 | 31.5% | ~7K |
| AV / Audio Visual | 25 | 7 | 28.0% | ~2K |
| Structure / MADA | 21 | 9 | 42.9% | ~3K |
| REBA 4 Coordination | N/A | 18 items | — | ~1K |
| Lighting/ZNA | 31 | 0 | RFP ISSUED Jun 2 | 0 |
| MEP | 49 | 0 | NOT STARTED | 0 |
| Security | 64 | 0 | NOT STARTED | 0 |
| HVAC | 30 | 0 | NOT STARTED | 0 |
| IT/ICT | 27 | 0 | NOT STARTED | 0 |
| Signage | 10 | 0 | NOT STARTED | 0 |
| BMS | 9 | 0 | NOT STARTED | 0 |
| Landscape | 6 | 0 | NOT STARTED | 0 |
| **Total** | **365** | **45** | **12.3% items** | **~15K** |

## Showcase Review Analysis

- **27 unique showcase shop drawings** across 7 types (Types 1, 2, 3, 4, 5a, 6a, 6b)
- **4 submittal cycles** (Sub 08, Sub 09, Mid-Apr batch, Sub 10)
- **23 NRS review PDFs** found in `05_Returned_Submittals/`
- Reviews are **substantive** (structural integration, ceiling fixings, door operation)
- **Closure: 0%** — no NRS comments formally closed, no GBH responses received

## PO P01824 — 3D Renders (SI007)

| Field | Value |
|---|---|
| PO | P01824 |
| Description | 3D Render Viewpoints — RIBA Stage 3 |
| Quantity | 27 viewpoints |
| Unit Price | SAR 8,750 |
| Total | SAR 236,250 |
| Date | 24 May 2026 |
| Purpose | SI007-mandated renders blocking IFC production |

## External Scope Confirmations

- **Interactives outside NRS scope** — Jim Richards confirmed via email (2 Jun). Gallery 9 RFI clarifies NRS has no contractual responsibility for interactive design.

## New File This Session

- `Docs/11_Correspondence/11.4_NRS_and_Subs/2026-06-02_A2742-6.04-018_Gallery9_RFI.pdf` — new Gallery 9 RFI

## Cross-Document Audit Findings

After EV Snapshot update to Scenario B, Codex audited the Contract Study and found:
- 19 stale value occurrences (538K, -76K, 0.88, -274K)
- **1 SVG-embedded metric card** with `+71K` CV instead of `-329K` — standard grep found the string but patch missed it due to unique context
- CPI: 0.60 in Contract Study vs 0.59 in EV Snapshot (both correct from 483/812=0.5948, but aligned to 0.59)

**Lesson:** Always run Codex audit after EV number changes. SVG metric cards and legend text are common stale value hiding spots.

## Report Location

`/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/Docs/07_Reports/07.5 Audit Report/NRS/Aseer_NRS_EV_Snapshot.html` (3 sheets, Rev 02)
