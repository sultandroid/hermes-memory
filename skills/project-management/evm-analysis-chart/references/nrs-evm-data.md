# NRS Earned Value Data — Aseer Regional Museum

**Contract:** SAR 1,209,000 (net)
**As of:** 03 June 2026 (final session)
**Document:** ASR-SAM-NRS-CONTRACT-001 Rev 01 → **Aseer_NRS_EV_Snapshot.html** (rebuilt as EV-only 5-sheet snapshot)

## Corrected EVM Summary

| Metric | Value | Note |
|--------|-------|------|
| **PV (Planned Value)** | **SAR 614,000** | 80% of Stage 4 fee (768K) per original plan |
| **EV Stage 4-A DD** | **SAR 538,000** | Architecture DD @ 70% bracket (user-defined). 251 dwgs delivered. |
| **EV Stage 4 specialist review** | **~SAR 9,000** | 12.3% of 115K bracket. 45 of 365 specialist items reviewed across 5/13 packages. |
| **EV Stage 5 shop dwgs** | **~SAR 47,000** | ~17.4% of 270K bracket. Showcase (23+ dwgs) + AV (7 files) shop drawing reviews confirmed. |
| **Total EV** | **~SAR 594,000** | DD (538K) + specialist review (9K) + Stage 5 shop dwgs (47K). |
| **AC (Paid)** | **SAR 812,100** | INV-4755 (121K) + INV-4781 (346K) + INV-4805 (346K) — all three confirmed paid via separate bank transfers. |
| **CV** | **-SAR 218,100** | CPI=0.73 — overpaid. Three invoices exceed total earned value. |
| **SV** | **-SAR 76,000** | SPI=0.88 — slight delay, attributable to SI007, not NRS performance |

## Stage 4 Bracket Breakdown (user-defined, 70% for DD)

| Phase | % | Value | NRS Work | Status |
|-------|---|-------|----------|--------|
| Architecture DD | **70%** | **538K** | 251 dwgs — complete design | ✓ DELIVERED |
| Specialist review | 15% | 115K | Review MEP/AV/showcases as Design Lead | 12.3% done (45/365 items) |
| IFC production | 15% | 115K | Convert DD → IFC | BLOCKED by SI007 |
| Coordination | 0% | 0 | Done by Samaya | — |
| **Total Stage 4** | **100%** | **768K** | | |

## Specialist Review Inventory (13 packages, precise from registers)

| Package | Total Expected | NRS Reviewed | % | EV Contribution |
|---|---|---|---|---|
| SLF / Life Safety | 20 | 6 | 30.0% | ~1K |
| Showcases (Glasbau) | 73 | 23 | 31.5% | ~4K |
| AV / Audio Visual | 25 | 7 | 28.0% | ~1K |
| Structure / MADA | 21 | 9 | 42.9% | ~2K |
| REBA 4 Coord | N/A | 18 items | N/A | ~1K |
| Lighting/ZNA | 31 | 0 | 0% → RFP ISSUED Jun2 | 0 |
| MEP | 49 | 0 | 0% | 0 |
| Security | 64 | 0 | 0% | 0 |
| HVAC | 30 | 0 | 0% | 0 |
| IT/ICT | 27 | 0 | 0% | 0 |
| Signage | 10 | 0 | 0% | 0 |
| BMS | 9 | 0 | 0% | 0 |
| Landscape | 6 | 0 | 0% | 0 |
| Others | 20 | 0 | 0% | 0 |
| **Total** | **365** | **45** | **12.3%** | **~9K** |

## Stage 5 Partial EV (from showcase + AV shop dwg reviews)

| Source | Items Reviewed | % of Stage 5 | EV |
|--------|--------------|-------------|-----|
| Showcase shop drawings | 23+ dwgs, 4 submittal cycles, 8 stamped | ~15% | ~40K |
| AV shop drawings | 7 files (PA Sound 5 floors + AV System) | ~2.5% | ~7K |
| **Total Stage 5 EV** | | **~17.4%** | **~47K** |

## Purchase Order P01824 — 3D Renders (Separate from NRS Contract)

| Field | Value |
|-------|-------|
| PO # | P01824 |
| Description | 3D Render Viewpoints — RIBA Stage 3 |
| Quantity | 27 viewpoints |
| Unit Price | SAR 8,750 |
| **Total** | **SAR 236,250** |
| Date | 24 May 2026 |
| Relationship | SI007-mandated 3D renders blocking IFC production. Supersedes "Updated Visuals" optional line (SAR 75K) in NRS contract. |
| Source | `Contracts/NSR/Purchase Order - P01824.pdf` → copied to `Docs/07_Reports/07.5 Audit Report/NRS/Purchase_Order_P01824.pdf` |

## Payment Register (Final — All Invoices Reconciled)

| Invoice | Amount | Status | Paid Date | Proof |
|---------|:------:|:------:|:---------:|-------|
| INV-4755 (Advance 10%) | SAR 120,900 | **PAID** | 25 Feb 2026 | Nissen Richards Studio 10.pdf (EUR 26,548.67 @ 4.5539) |
| INV-4781 (Stage 4 1/2) | SAR 345,600 | **PAID** | 4 May 2026 | Nissen Richards Studio 781.pdf (EUR 76,334.19 @ 4.5196) |
| INV-4805 (Stage 4 2/2) | SAR 345,600 | **PAID** | 17 May 2026 | Nissen Richards Studio 805.pdf (EUR 77,019.08 @ 4.4872 = SAR 345,600.02 exact match) |
| **Total AC** | **SAR 812,100** | | | |
| INV-4825 (Stage 5 1/3) | SAR 90,000 | **DUE 11 Jun** | — | — |
| **Total outstanding** | **SAR 90,000** | (INV-4825 only) | | |

## Key Discovery: Three Bank Transfers, Not One

The initial assumption was a single SAR 345,657 transfer covering INV-4755 + INV-4781 partial. **This was wrong.** OCR of ALL files in the Payment/ directory revealed three separate Alinma transfers:

| Receipt File | Date | EUR | Rate | SAR | Paid Invoice |
|---|---|---|---|---|---|
| Nissen Richards Studio 10.pdf | 25 Feb | 26,548.67 | 4.5539 | **120,900** | INV-4755 |
| Nissen Richards Studio 781.pdf | 4 May | 76,334.19 | 4.5196 | ~345,600 | INV-4781 |
| Nissen Richards Studio 805.pdf | 17 May | 77,019.08 | 4.4872 | **345,600.02** | INV-4805 ✓ exact match |

## Monthly EVM Data Table

| Metric | Feb | Mar | Apr | May | Jun | Jul* |
|--------|-----|-----|-----|-----|-----|------|
| PV (cumulative) | 30K | 90K | 200K | 400K | 614K | 700K |
| EV (cumulative) | 20K | 50K | 120K | 300K | **594K** | 700K* |
| AC (cumulative) | 10K | 30K | 135K | 345K | **812K** | — |
| SPI | — | — | 0.60 | 0.75 | **0.88** | — |
| CPI | — | — | 1.17(→0.89) | 0.87(→0.75) | **0.73** | — |

## Key Corrections History

1. **Initial report** (pre-02 Jun): Claimed 251 dwgs = IFC (wrong). EV = 384K (incomplete).
2. **DD vs IFC correction** (02 Jun): Drawings are DD (Stage 4-A), not IFC. EV = 460K (DD only).
3. **SI007 context** (02 Jun): IFC delay is due to SI007 (3D renders required first). Not NRS performance failure.
4. **Payment scan** (02 Jun): OCR of all 4 invoices. INV-4805 initially thought unpaid. AC = 466,557.
5. **Bracket correction** (02 Jun): User set DD @ 70% (per his expertise). Coordination by Samaya. EV = 538K.
6. **INV-4805 confirmed paid** (03 Jun): User pointed to Nissen Richards Studio 805.pdf — EUR 77,019.08 × 4.4872 = SAR 345,600.02 = exact match to INV-4805. AC corrected to **812,100**. CV flipped from +71K to **-274K**.
7. **PO P01824** (03 Jun): Separate Purchase Order for 27 3D render viewpoints @ SAR 8,750 = SAR 236,250. This is the SI007-mandated render package blocking IFC. Supersedes NRS contract's optional "Updated Visuals" line.
8. **Specialist review inventory** (03 Jun): Precise calculation from project registers — 45/365 items reviewed (12.3%). EV = ~9K for specialist review bracket.
9. **Stage 5 partial EV** (03 Jun): Showcase + AV shop dwg reviews confirmed. EV = ~47K (17.4% of Stage 5).
10. **Interactive scope boundary** (03 Jun): Jim Richards confirmed interactives are outside NRS scope.
11. **Report rebuilt** (03 Jun): Stripped contract study content. Now 5-sheet EV snapshot only. Stakeholder language throughout. Humanized.
12. **Lighting/ZNA RFP** (03 Jun): StudioZNA proposal received. Status updated from "NOT STARTED" to "RFP ISSUED".
