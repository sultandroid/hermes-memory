# Structural Register Pattern — Aseer Museum (Worked Example)

39 items, 5 categories, 4-tier dependency model. Generated 30 Jun 2026.

## Architecture

The structural register follows a **survey → assessment → design → IFC** chain. Each item assigned a tier that determines which stage sheets it appears in. Items can have item-level start date overrides (e.g., BIM starts 15 Jul instead of the baseline 29 Jun).

```python
def mk(ref, desc, disc, tier, pkg, rm='', start=None):
    s = start or BASE
    if tier == 1:  # Survey — immediate
        return [s, add30(s,1), add30(add30(s,1),1), EM]
    elif tier == 2:  # Assessment — needs Tier 1
        return [EM, s+30+REVIEW, s+60+2*REVIEW, EM]
    elif tier == 3:  # Design — needs Assessment
        return [EM, EM, s+60+2*REVIEW, EM]
    elif tier == 4:  # IFC only
        return [EM, EM, EM, d(2026,8,28)]
```

## Categories & Items

### A — SURVEYS (Tier 1, 29 Jun)
| Ref | Item | Remarks |
|-----|------|---------|
| ST-001 | Dilapidation survey — full building condition | |
| ST-002 | Cloud/3D laser scan survey — existing building geometry | |
| ST-003 | As-built drawing review & verification | |
| ST-004 | Structural investigation report — existing building appraisal | |
| ST-005 | Structural design criteria & methodology | |

### B — ASSESSMENT (Tier 2, 29 Jul 90%)
| Ref | Item | Remarks |
|-----|------|---------|
| ST-006 | Slab and weight loading assessment | Needs ST-001/002 |
| ST-007 | Structural loading calculations & load schedules | Needs ST-001/002 |
| ST-008 | Structural site conditions report | Needs ST-001 |
| ST-009 | Core test results analysis & interpretation | Needs site investigation |
| ST-010 | Structural capacity assessment — floors & roof slabs | Needs ST-003 + core tests |

### C — DESIGN (Tier 3, 11 Sep 100%)
| Ref | Item | Sub-Package | Remarks |
|-----|------|-------------|---------|
| ST-011 | Structural strengthening design — existing building | Strengthening | Needs ST assessment + Arch GA |
| ST-012 | Strengthening details — beam/column/junction | Strengthening | Needs ST-011 approved |
| ST-013 | New steel stairs design — 2-flight | Stairs | Needs Arch GA + assessment |
| ST-014 | New steel stairs design — 3-flight | Stairs | Needs Arch GA + assessment |
| ST-015 | Stair structural connections & anchorage details | Stairs | Needs ST-013/014 |
| ST-016 | Ceiling support system design — exhibition halls | Design | Needs assessment + Arch GA |
| ST-017 | Sunshade structural design | Design | Needs Arch GA |
| ST-018 | Balustrade & handrail support design | Design | Needs Arch GA |
| ST-019 | ETABS structural model & analysis | BIM/Model | Needs assessment data |
| ST-020 | Structural opening schedules & lintel details | Design | Needs Arch GA |
| ST-021 | Structural general arrangement drawings (plans, sections) | Design | Needs all inputs |

### C1 — BIM MODELS (start 15 Jul per BEP)
| Ref | Item | Stage Dates | Remarks |
|-----|------|-------------|---------|
| ST-022 | BIM — Existing Conditions Model (LOD 300) | 50%=15 Jul, 90%=21 Aug | Existing only to 90% |
| ST-023 | BIM — Scope / Design Model (LOD 300->350) | 50%=15 Jul, 90%=21 Aug, 100%=27 Sep | |
| ST-024 | BIM — Design Model Development (LOD 350->500) | 100%=27 Sep | Progressive refinement |

**BIM rules:**
- Existing Conditions: no 100% or IFC (LOD 300 handoff only)
- Scope/Design Model: no IFC (goes to 100% only)
- As-Built Model tracked under IFC/Handover (ST-029)
- All BIM starts 15 Jul, not 29 Jun baseline — requires cloud survey data first

### D — IFC/HANDOVER (Tier 4, 28 Aug)
| Ref | Item | Sub-Package |
|-----|------|-------------|
| ST-025 | Structural ITP — Inspection & Test Plan | QA/Commissioning |
| ST-026 | AFC documentation — Designer certification | QA/Commissioning |
| ST-027 | Material submittals — structural steel, anchors, bolts | Submittals |
| ST-028 | Record drawings / As-built structural | Handover |
| ST-029 | BIM — As-Built Model (LOD 500) | BIM |
| ST-030 | Structural O&M manual | Handover |
| ST-031 | Training for MoC — structural maintenance | Handover |
| ST-032 | Spares — structural components (1-year) | Handover |

### E — RIGGING (merged from Rigging register)
| Ref | Item | Tier | Remarks |
|-----|------|------|---------|
| ST-033 | Rigging design philosophy & criteria | 1 (29 Jun) | |
| ST-034 | Rigging load schedule | 1 (29 Jun) | |
| ST-035 | Ceiling suspension point layout | 3 (11 Sep) | Needs slab assessment + Arch ceilings |
| ST-036 | Rigging design details (trusses, beams, brackets) | 3 (11 Sep) | After layout approval |
| ST-037 | Anchor pull-out test procedure & results | 4 (28 Aug) | |
| ST-038 | Rigging ITP | 4 (28 Aug) | |
| ST-039 | Rigging O&M manual | 4 (28 Aug) | |

## Sheet Distribution

| Stage Sheet | Items Shown | What's Included |
|-------------|-------------|-----------------|
| 50% Design | 9 | Surveys (5), BIM Existing+Scope (2), Rigging Tier 1 (2) |
| 90% Design | 14 | Surveys (5), Assessment (5), BIM (2), Rigging Tier 1 (2) |
| 100% Design | 27 | Surveys (5), Assessment (5), Design (11), BIM (3), Rigging Tier 1+3 (3) |
| IFC/AFC | 11 | Handover (8), Rigging Tier 4 (3) |

Each stage sheet shows EM for all other columns — only its own stage date column populated.

## mk() Helper Limitations

The `mk()` helper works for uniform tier-based items but breaks for:
- Items with different start dates (BIM starts 15 Jul not 29 Jun) — pass `start=`
- Items that skip specific stages (BIM Existing: no 100%/IFC) — use raw tuple
- Items with special date overrides per user direction

**Pattern:** Use `mk()` for bulk tier 1-4 items, then append raw tuples for exceptions.

## Pitfalls Encountered

1. **Date + int arithmetic**: `add30(s,1) + REVIEW` fails because `add30` returns `date` and `REVIEW` is `int`. Use `timedelta(days=...)` for compound offsets.

2. **Date formatting**: Writing `date` objects to openpyxl cells with `number_format='DD/MM/YYYY'` is correct for Excel. But when building display strings, format with `.strftime('%d/%m/%Y')`. Mixing `date` objects and `EM` strings in the same list requires conditional formatting before writing.

3. **Stage masking**: Each stage sheet must show EM in all stage columns except its own. Without masking, the 90% sheet wrongly shows the 50% and 100% dates in columns 4 and 6.

4. **Empty placeholder files**: Subcontractor folders (e.g., `11_Structural_Contractor`) may contain zero-byte SCOPE_REQUEST.md and _PACKAGE_STATUS.md files. Don't assume they have content — verify with `head -c 8` before reading.
