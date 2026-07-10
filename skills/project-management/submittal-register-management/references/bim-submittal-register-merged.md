# Merged from bim-submittal-register skill

## 13-Column Template (AV format)

| Col | Header | Notes |
|---|---|---|
| A | Gate | e.g. "Detailed Design", "Coordinated IFC" |
| B | Level / Zone | Floor or system zone |
| C | Discipline | e.g. FLS, Electrical, Mechanical |
| D | Submission Category | Detailed Design, BIM, Material & Samples, Coordinated IFC |
| E | Drawing Package / Item | Unique reference code |
| F | Submission Description | Full description of deliverable |
| G | Responsibility | Who prepares it |
| H | Planned Submission Date | DD/MM/YYYY format |
| I | Review Duration (Days) | 3 days (design), 14 days (IFC) |
| J | Approval Authority | Always CG |
| K | Linked Activity ID | Program activity reference |
| L | Status | Planned / In Progress / Pending |
| M | Remarks | Notes, dependencies, clarifications |

## 3-Gate Structure

- Gate 1 — Detailed Design: Strategy, design reports, calculations, drawings, BIM models
- Gate 2 — Material Approval: Material submittals register, equipment submittals
- Gate 3 — Coordinated IFC: Per-floor IFC packages, specs, BIM LOD 500, ITP, O&M, training, spares
- Gate 1.5 (90% Detailed Development): For accessibility/compliance plans (SBC 201)

## CG-Requested Items

- Site Assessment & Survey Report
- MEP Design Risk Management Report
- MEP Value Engineering Study
- Concept Design Review & Gap Analysis Report
- Existing As-Built Drawing Survey
- RACI Matrix for interface parties

## User Preferences (Aseer Museum)

- Approval Authority: Always CG
- Responsibility: "MEP Designer Office" not "Consultant"
- Status: "Planned" default
- Linked Activity ID: must be populated
- SOW Alignment: cross-reference CG Responses
- Program Sync: >14 day variance = critical non-compliance
