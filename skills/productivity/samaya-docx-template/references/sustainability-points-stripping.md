# Sustainability Document: Points-Stripping Reference

## Core rule

The ER mandates **code compliance** (Mostadam Manual + SBC 1001), NOT a rating tier or points target. Every sustainability document (strategy, plan, SOW, R&R) must be framed as a compliance plan, not a points-chasing exercise.

## What to strip — complete reference

### DC block

| Pattern | Action |
|---------|--------|
| `<div class="k">Rating tier</div><div>...</div>` | Remove entire line |

### Snap cards / metric cards

| Pattern | Action |
|---------|--------|
| `Voluntary target` / `SILVER 45+ pts` green snap | Remove entire card |
| `Voluntary stretch` / `GOLD 60+ pts` amber snap | Remove entire card |
| `Design credits ~25` snap | Remove entire card |
| `Constr. credits ~22` snap | Remove entire card |
| Orphan `SILVER` / `GOLD` divs | Remove |

### Column headers

| Old | New |
|-----|-----|
| `Target pts` | `Compliance` |
| `Target` | `Compliance` |
| `Stretch` | `Status` |
| `Credit` | `Item` |

### Phase-band total rows

| Old | New |
|-----|-----|
| `Target <b>14 / 16 pts</b>` | `Compliance verified` |
| `Target <b>14 / 15 pts</b>` | `Compliance verified` |

### Body text

| Pattern | Action |
|---------|--------|
| `~X pts · design-led` | Remove `~X pts ·` |
| `Stretch ≥ 24% (5+ pts)` | Remove entirely |
| `(5 pts at 5%+ on-site renewable)` | Replace with `(per Mostadam Manual)` |
| `(3 pts at 75% of regularly-occupied)` | Replace with `(per Mostadam Manual)` |
| `Samaya commits to <b>SILVER 45+ pts</b> as minimum` | Replace with `Samaya commits to full code compliance` |
| `Owner of <b>design-stage credits</b> (~25 pts)` | Replace with `Owner of <b>design-stage compliance</b>` |
| `Owner of <b>construction-stage credits</b> (~22 pts)` | Replace with `Owner of <b>construction-stage compliance</b>` |
| `credit pool` / `credit pools` | Replace with `compliance category` / `compliance categories` |
| `credit-targeting log` | Replace with `compliance log` |
| `credit-targeting` | Replace with `compliance` |
| `Pre-credit application + targeted` | Replace with `Pre-compliance review +` |
| `targeted-points map setup` | Replace with `compliance framework setup` |
| `pts on track / drift / corrective actions` | Replace with `compliance status / drift / corrective actions` |
| `Voluntary target` | Replace with `Compliance` |
| `Voluntary stretch` | Replace with `Status` |
| `Samaya aspiration (not ER-mandated)` | Replace with `Code compliance` |
| `Samaya stretch goal (not ER-mandated)` | Replace with `Code compliance` |
| `GREENGUARD Gold` | Replace with `GREENGUARD` |
| `Gallery (Tier B)` | Replace with `Gallery` |
| `sub-credit pickups in CM-05 stretch to 16 with full enhanced Cx` | Replace with `full enhanced Cx` |
| `major win on MT-01 (existing-building re-use intrinsic to refurb)` | Replace with `existing-building re-use intrinsic to refurb` |
| `(construction-phase subset)` | Remove |
| `design-stage EN credits (~10 pts) addressed in Part B §6` | Replace with `design-stage EN credits addressed in Part B §6` |
| `Mostadam credit-targeting log (per §14)` | Replace with `Mostadam compliance log (per §14)` |
| `Pre-DD assessor onboarding` | Replace with `Assessor onboarding` |
| `Strategy review + assessor onboarding + targeted-points map setup` | Replace with `Strategy review + assessor onboarding + compliance framework setup` |
| `Proposed energy use ≥ 14% improvement below ASHRAE 90.1 baseline (Mostadam EN-04 minimum). Stretch ≥ 24% (5+ pts).` | Replace with `Proposed energy use per Mostadam EN-04 minimum requirement.` |
| `EN-13 Renewable Energy (5 pts at 5%+ on-site renewable) · IN Innovation pickup if > 10%.` | Replace with `EN-13 Renewable Energy (per Mostadam Manual)` |
| `IEQ-06 Daylight (3 pts at 75% of regularly-occupied` | Replace with `IEQ-06 Daylight (per Mostadam Manual)` |
| `recommends design changes to lift credit-pool toward Gold stretch` | Replace with `recommends design changes for compliance improvement` |

### SVG elements

| Pattern | Action |
|---------|--------|
| `<text ... fill="#64748B">~35 of ~45 in-scope pts</text>` | Remove |
| `<text ... fill="#64748B">~7 of ~45 pts + ER §2.4 access</text>` | Remove |
| `<text ... fill="#64748B">~3 pts + LCC audit trail</text>` | Remove |

### TOTAL POINTS row

| Pattern | Action |
|---------|--------|
| `<tr style="background:#0F766E;">...TOTAL POINTS...</tr>` | Remove entire row |

### ER tier paragraph

| Old | New |
|-----|-----|
| `The ER does not pre-set a Mostadam tier (Silver / Gold / Platinum). The tier is set with the accredited Mostadam assessor at DD stage based on cost-benefit + design feasibility. <b>SILVER 45+ pts</b> as minimum, <b>GOLD 60+</b> as stretch.` | `The ER mandates compliance with the Mostadam Manual and SBC 1001 codes. The accredited assessor verifies compliance at each stage gate.` |

### Employer row

| Old | New |
|-----|-----|
| `Endorses sustainability initiative + targeted points (ER §3.7 Performance Req). Funds Mostadam certification.` | `Endorses sustainability initiative per ER §3.7. Funds Mostadam certification.` |

### ER cross-reference table

| Old | New |
|-----|-----|
| `Compliance with sustainability requirements + targeted points (General Cleaning section — corrected from §2.7 in C03)` | `Compliance with sustainability requirements (General Cleaning section — corrected from §2.7 in C03)` |

### Revision log (historical record — keep as factual)

| Pattern | Keep? |
|---------|-------|
| `(e) Rating tier reframed as Samaya voluntary aspiration — ER does not mandate a Mostadam tier.` | Keep — it's a factual record of a C03 change. Rephrase to `(e) Rating tier removed — ER does not mandate a Mostadam tier; strategy reframed as code compliance.` |

## What to keep

- ER section references verbatim (e.g. ER §2.5 "targeted points" is a section title — keep as factual citation)
- Revision log entries describing historical changes (factual record)
- Code names: Mostadam Manual, SBC 1001, SBC 601/602, SASO, ASHRAE 90.1
- Compliance matrices with credit names and actions
- Subcontractor obligations tables
- Procurement sustainability specifications
- Reporting cadence and verification procedures

## Verification checklist

Before presenting a sustainability document:

1. Scan for: Silver, Gold, 45+, 60+, "pts", "stretch", "rating tier", "credit pool", "total points", "target pts", "targeted points"
2. Check column headers — "Target pts" → "Compliance", "Stretch" → "Status"
3. Check DC block — no "Rating tier" line
4. Check snap cards / metric cards — no voluntary target/stretch badges
5. Check compliance matrix — no TOTAL POINTS summary row
6. Check RACI matrix — no "owner of X credits (~Y pts)" language
7. Check body paragraphs — no "Samaya commits to SILVER" or "aspiration" language
8. Check SVG text elements — no "~X of ~Y pts" labels
9. Check phase-band total rows — no "Target X / Y pts" language
10. Check ER cross-reference table — no "targeted points" in Samaya's own descriptions (keep only if verbatim ER section title)

## Automation

The `scripts/html-to-docx-converter.py` script in this skill has a `--strip-points` flag that applies all the above transformations automatically. Run:

```bash
python3 scripts/html-to-docx-converter.py input.html output.docx --strip-points
```

The `strip_points_language()` function in the script implements every pattern in this reference. If the HTML source has new patterns not covered, add them to the function and update this reference.
