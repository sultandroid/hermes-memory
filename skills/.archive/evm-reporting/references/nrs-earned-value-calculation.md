# NRS Earned Value Calculation — 03 June 2026

## Contract
- **Total:** SAR 1,209,000
- **Stage 4 (IFC Package):** SAR 768,000 (63.5%)
- **Stage 5 (Off-site Fab Review):** SAR 270,000 (22.3%)
- **Stages 5-6 (On-site Fab Review):** SAR 171,000 (14.2%)

## Brackets (user-defined)
- Architecture DD: **70%** of Stage 4 = **SAR 538,000**
- Specialist review (Design Lead): **15%** of Stage 4 = **SAR 115,000**
- IFC production: **15%** of Stage 4 = **SAR 115,000**
- Coordination: **0%** (handled by Samaya)

## What's Delivered
- Architecture DD: 251 drawings — 75/25 split applied (see Scenario B below)
- Specialist review (from register: 45/365 items = 12.3%): ~SAR 15K
- Showcase + AV shop drawing reviews (from register: ~17.4% of Stage 5): ~SAR 47K

## Payments (AC)
| Invoice | Date | Amount | Paid via |
|---------|------|--------|----------|
| INV-4755 (Advance 10%) | 19 Feb 2026 | SAR 120,900 | Nissen Richards Studio 10.pdf (EUR 26,548.67 @ 4.5539) |
| INV-4781 (Stage 4 1/2) | 23 Mar 2026 | SAR 345,600 | Nissen Richards Studio 781.pdf (EUR 76,334.19 @ 4.5196) |
| INV-4805 (Stage 4 2/2) | 29 Apr 2026 | SAR 345,600 | Nissen Richards Studio 805.pdf (EUR 77,019.08 @ 4.4872) |
| **Total AC** | | **SAR 812,100** | |

## Scenario B — Final EV Metrics (03 June 2026 Rev 02)
After user questioned the "100% DD vs 13% specialist" logic, switched to a 75/25 split:

| Component | Calculation | EV (SAR) |
|-----------|-------------|:--------:|
| DD — Standalone (75% × 538K) | Unconditional | 403.5K |
| DD — Coordination-dependent (25% × 538K = 134.5K × 12.3%) | 16.5K |
| **Subtotal DD** | | **420K** |
| Specialist review (12.3% of 115K bracket) | | 15K |
| Stage 5 shop dwg reviews | | 47K |
| **Total EV** | | **~483K** |
| **AC** | | **812K** |
| **CV (CPI)** | | **-329K (0.59)** |
| **PV** | | **614K** |
| **SV (SPI)** | | **-131K (0.79)** |

## Key Lessons
1. Always OCR all bank receipts — there may be 3+ separate transfers (advance + monthly x2)
2. INV-4805 was assumed unpaid; bank receipt Nissen Richards Studio 805.pdf proved it was paid (EUR 77,019.08 × 4.4872 = SAR 345,600.02 exact match)
3. NRS review work on showcases and AV was found by searching project files
4. **CRITICAL — DD/Specialist dependency:** User corrected the assumption that 100% DD EV was claimable while specialist coordination was at 13%. Always present Scenario B (75/25 split) as a proposal before finalizing DD EV when specialist work is incomplete. See SKILL.md "DD/Specialist Dependency" section for full methodology.
5. Cross-document stale values: After updating EV Snapshot, audit Contract Study and all related reports. Codex found a stale `+71K` CV inside a Contract Study SVG metric card that standard grep missed.
