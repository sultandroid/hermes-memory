# Excel Schedule File Structure — 5-Sheet Layout

## Purpose

Standard 5-sheet Excel workbook for design-phase baseline schedules. Extends the 4-sheet layout with an Assumptions sheet (live model parameters) and splits DMP gate compliance into its own sheet. Used for Aseer Museum (MOC-MUS-ASE) Rev 1 schedule rebuild.

## Sheet Layout

| Sheet # | Name | Content | Row Count |
|---|---|---|---|
| 1 | Assumptions | Live model parameters: NTP anchor date, KSA weekend code, CG review SLA (calendar days), Civil Defense review period, consultant review period, tender/prequal return period, Ramadan start/end dates, Ramadan duration factor (1.4×), public holidays list (Founding Day, Eid al-Fitr, Eid al-Adha, National Day). **Blue cells = input** — changing NTP or CG SLA re-anchors the entire model. | ~24 rows |
| 2 | Baseline Schedule | Full activity schedule: 110+ activities across 9 phases (Mobilization, Client Input, Assessment, 50% Design, Material Waves, Mock-ups & Samples, 90% Design + BIM, Authorities, 100% IFC, Close-out & Handover, Post-Design Procurement). Each row: Activity ID, Activity Name, Phase, Type (Work/Review/◆ MS), Dur In, Ram× flag, Eff Dur, Predecessors, Start, Finish, Day#, Responsible, Notes. All dates are formula-computed from logic + calendars. | 119+ rows |
| 3 | DMP Gates | Gate compliance comparison: DMP target day/date vs model-computed milestone day/date with gap (days). Gates tracked: D35 (50%), D65 (90%), D82 (IFC submitted), D88 (AFC/IFC approved), D90 (site start enabler), D300 (TOC). Includes mitigation position note per gate. | ~11 rows |
| 4 | Client Delay Tracker | EOT dashboard: 7 client input items (exhibition text, copyright, AV software, site access, 3 CG SLA monitors) each with Required Date, Day Req, Actual Received (blue input cell), auto-calc Delay Days, Claimed days, Contract Clause, Notice ref, Notes. Bottom: total claimed delay, measured EOT (network push), baseline vs live design completion dates. WIRED to the network — late Actual Received pushes all milestones. | ~17 rows |
| 5 | Basis of Schedule | Narrative: what changed from previous revision, declared fast-track overlaps, acceleration levers, limits (Excel model is for management/negotiation only — contractual baseline must be rebuilt in P6). | ~31 rows |

## Phase Mapping

Used for all schedule sheets:

| Phase | Color | Notes |
|---|---|---|
| MILESTONE | Purple (#E8D5F5) | Zero-duration key events |
| MOBILIZATION | Light grey (#F2F2F2) | Team setup, CDE, prequal send |
| ASSESSMENT | Light blue (#D6E4F0) | Surveys, point cloud, condition survey, hazmat screening, assessment reports, record model (scan-to-BIM) |
| CLIENT INPUT | Red (#F8D7DA) | Exhibition text, copyright, AV software, site access from client — wired to network as delay drivers |
| 50% DESIGN | Light green (#E2EFDA) | Concept design all disciplines — starts SS+5 into assessment |
| MATERIAL WAVES | Red (#F8D7DA) | 6 rolling waves (arch finishes A/B, specialist, MEP, electrical/ELV, signage) — each with submit → CG review → revise → re-review cycle |
| MOCK-UPS & SAMPLES | Light yellow (#FFF2CC) | Samples + mock-ups fabrication → CG mock-up review/approval (fabrication release hold point) |
| 90% DESIGN + BIM | Light blue (#D6E4F0) | Detailed design with approved materials + 2 BIM federation/clash cycles |
| AUTHORITIES | Orange (#FCE4D6) | Fire & life safety strategy → Civil Defense review → incorporate comments |
| 100% IFC | Light green (#E2EFDA) | Final IFC, BIM validation, CG review, CRS closure, CG confirmation |
| CLOSE-OUT & HANDOVER | Light grey (#F2F2F2) | Final design report, design handover to construction |
| POST-DESIGN PROCUREMENT | Teal (#D5F5E3) | Fabrication drawings, long-lead POs, fabrication window (parallel to construction) |
| DMP GATES | Light orange (#FCE4D6) | D35-D88 design gates plus D300 TOC — computed vs target gap analysis |

## Color Palette

```
Navy header:    #1F3864
Yellow header:  #FFD966
White text:     #FFFFFF
```

## Key Formulas

The Client Delay Tracker should have manual-entry cells for Actual Received Date (column G). Delay Days auto-calculate = Actual - Required. EOT Days = Delay Days (adjusted for concurrency where applicable).

## File Placement

Place the schedule file in TWO locations inside the project directory:
1. `Time Schedules/Aseer_Museum_Baseline_Schedule.xlsx` — primary
2. `Submittals/Aseer_Museum_Baseline_Schedule.xlsx` — redundant copy

Also update PROJECT_MEMORY.md with a reference line pointing to the file.

## Activity ID Conventions

| Prefix | Type |
|---|---|
| MS#### | Milestone |
| MB#### | Prelim / Permit / Mobilization |
| A#### | Assessment / Design / Approval |
| PR#### | Procurement / Material Submittal |
| AP#### | Approval of Material Submittal |
| M### | Mobilization / Management |

## Durations

- Milestones: 0 days (displayed as ◆)
- Working days: use "Xd" format (e.g. "12d", "5d")
- Max sequential duration without approval gate: 15 days
- Minimum meaningful design activity: 8 days (electrical layout) — anything less than 5 days is unrealistic for museum fit-out
