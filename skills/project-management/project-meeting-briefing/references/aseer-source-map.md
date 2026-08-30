# Aseer Museum — Meeting Briefing Source Map

Where to read the LIVE status for each discipline before an internal meeting. Read these, not the stale summary.

## Per-discipline submission trackers (`02_Schedule/`)
| Discipline | Tracker file | Notes |
|-----------|--------------|-------|
| AD Engineering (Mech) | `02_Schedule/AD_Engineering/README.md` | 3-gate plan (DD → Material → IFC) |
| AD Engineering (Elec/ICT) | `02_Schedule/AD_Engineering/AD_Engineering_Electrical_ICT_Tracker.md` | Live per-package status; created 2026-08-30 |
| Rigging | `02_Schedule/Rigging_Contractor/README.md` | Often "Not started / Firm TBD" |
| Acoustics | `02_Schedule/Acoustic_Specialist/README.md` | TransOrient onboarding status |
| Graphics | `02_Schedule/graphics_submission_plan.md` | Client-blocked (MoC content) |
| AV/Rawasin | `02_Schedule/Rawasin_AV_IT/README.md` | Sister company; interactive folded in |
| Lighting (ZNA) | `02_Schedule/Studio_ZNA_Lighting/README.md` | |
| Showcases (Glasbau Hahn) | `02_Schedule/Glasbau_Hahn_Showcases/README.md` | |

## Master registers (`01_Registers/`)
- `submittal_register.md` — master submittal log with CG codes + dates. **Read this for any "did X submit / what code" question.**
- `risk_register.md`, `rfi_register.md`, `ncr_register.md` — as needed.

## Status / actions
- `00_Status/action_items.md` — open actions, owners, due dates (has per-meeting sections like `AD30-*`).
- `00_Status/project_status.md` — **STALE auto-snapshot; cross-check only, never primary evidence.**
- `00_Command_Center/master_dashboard.md` — auto-generated weekly; stale.

## Outlook SQLite (freshest for "submitted today" / latest CG reply)
Path + queries in the `outlook-data-extraction` skill. Use for:
- "What was submitted today" → search subject for the doc ref (e.g. `ZD-0116`, `Demolition routing`).
- Latest CG reply → search sender `@cg.com.sa` + subject.
- Who said what / who's chasing whom → search sender/recipient.

## Recurring meeting topics (as of 2026-08-30)
- **Fire Alarm** — Civil Defence revision loop + 3-stamp chain (Civil Defence → NRS → consultant). Accelerate via staggered parallel dispatch.
- **AD Engineering excuses** — "no date commitment", "blocked on power" (refuted: power submitted), "needs Civil Defence coordination" (refuted: TO coordinates). Instruct: work from the tender, don't stop work.
- **Fire Fighting pump** — potential Variation Order claim (SAR 350–650K); Blue House didn't mention pumps; Employer Requirement > Design Base Report; missing building license + prior Civil Defence approval = owner (MoC) obligation.
- **Skylight/Atrium** — isolate Basement+LGF (fire-rated partition); smoke curtain ≈ SAR 300–400K (don't propose it — let architect request); smoke fans on skylight placement problem.
- **Rigging** — no contractor approved (SOROOH Code D); outreach via Mouns (no names yet); Showtex (Rowena) is equipment-focused.
- **Structure** — expose for cloud survey (scan-only, NO demolish per ZD-0106); concrete core avg 74% (NOT COMPLY), Core-01 Ground C4 = 15.8 MPa.
- **Doors/hardware** — patinated brass on moving parts is risky (seizes locks/cylinders); powder coated raised to CG; hinge selection = torque + max leaf width, not just weight.
