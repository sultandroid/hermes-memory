# Worked Example: Full SOW Audit & Filing (2026-07-21)

## Context
Full audit of 30 specialist packages against Project SOW, ER, Appendix A/B, and Compliance Matrix. Built 3-layer system (SOW, submission plan, tracker) for all packages. Filed SOW documents from OneDrive for 6 packages.

## Packages Filed This Session

| Package | Source Location | Files Found | Key Gaps |
|---------|----------------|-------------|----------|
| AD Engineering | Email attachments (Outlook) | Signed agreement, MEP SOW, Electrical SOW draft, CVs, cert | MEP installer not awarded |
| Studio ZNA | `24_Subcontractors/ZNA/02_Contract/` | Contract (Arabic), Consultancy Agreement (English) | ApxA 4.02 spares, 4 CG conditions, supplier TBD |
| Rawasin AV/IT | `24_Subcontractors/AV_IT/` + `90_Legacy_Source_Bank/07_Subcontractors/04_AV_IT_Contractor/` | PQ-0027, BOQ, PQ submittal | Media/software exclusion, spares, Q-Sys Code C, Audinate PQ |
| Graphics | `24_Subcontractors/Graphics_Specialist_Scope_of_Work.pdf` (root level) | SOW PDF | Content/copyright exclusions not in SOW |
| Nama FLS | `90_Legacy_Source_Bank/07_Subcontractors/_MANAGER_DASHBOARD/` + `06_Procurement/General/11_FLS/` | Scope request, status register | No signed contract, design not triggered, IFC-0004 blocked |
| Structural | `90_Legacy_Source_Bank/06_Procurement/General/12_Structural/Email_Data_Extraction/` | Email database | Not appointed, DD rejected twice, 2 conflicts |

## OneDrive Search Patterns That Worked

1. **Canonical folder** `24_Subcontractors/<name>/` — often has only contract/PQ
2. **Legacy source bank** `90_Legacy_Source_Bank/07_Subcontractors/<name>/` — most reliable for older documents
3. **Procurement folders** `90_Legacy_Source_Bank/06_Procurement/General/<name>/` — has status registers, email DBs
4. **Root-level files** in `24_Subcontractors/` — some SOWs are loose PDFs (e.g. `Graphics_Specialist_Scope_of_Work.pdf`)
5. **Archive** `99_Archive/02_Scope_Management/<name>/` — deep research docs (e.g. `AV_Deep_Research.md`)

## Common OneDrive Path Issues
- `24_Subcontractors/` uses canonical folder numbers (02_Lighting_Designer, 04_AV_IT_Contractor, etc.)
- `90_Legacy_Source_Bank/07_Subcontractors/` uses same numbering but has more content
- Some folders exist in legacy but not in canonical (e.g. `08_Rawasin_AV` only in legacy)
- `._*` Apple Double files must be filtered out with `-not -name "._*"`
- OneDrive EDEADLK errors: use `osascript` bridge for reads, `cp` for writes

## SOW Status Conventions Used
- ✅ Filed in repo (actual documents present in `03_Scope/<name>/`)
- 🟢 Approved (exists on OneDrive, not yet filed)
- 🟡 Draft RACI only (no formal package SOW)
- ❌ Missing

## Key Gaps Discovered
- ApxA 4.02: Lighting spares not confirmed in ZNA SOW
- ApxA 2.13: Media/AV software by MoC not documented in Rawasin SOW
- ApxA 4.01: AV spares not confirmed
- ApxA 2.12/3.01-3.05: Content/copyright by MoC not documented in Graphics SOW
- 6 open interface conflicts (SRC-001 through SRC-006) blocking SOW finalisation

## Classification Lesson
User corrected: supply-only packages (materials/equipment) don't need SOWs. Only specialists/contractors (design, install, consultancy) need SOWs. Panasonic (AV equipment), FF&E (furniture), and Material Testing Lab are supply-only — mark ⚪, not ❌. This was added to the skill as a mandatory pre-audit classification step.

## 3-Layer System Created
```
03_Scope/                          ← 27 folders (6 with actual documents)
02_Schedule/                       ← 27 folders (1 with actual plan: AD Engineering)
Technical_Office/Submission_Tracker/ ← 27 folders (1 populated: AD Engineering)
```

## Files Updated
| File | Change |
|------|--------|
| `specialist_register.md` | Added SOW/Plan columns to Tier 2 + Tier 3; all 27 specialists have paths |
| `subcontractor_sow_raci_register.md` | Updated ZNA, Graphics, Rawasin, MEP Designer statuses |
| `subcontractor_package_register.md` | Updated MEP Designer row with repo paths |
| `PROJECT_MEMORY.md` | AD Engineering entry with file paths |

## Audit Output
`Technical_Office/Submission_Tracker/SOW_Compliance_Audit.md` — 280 lines, 30 packages, per-source compliance tables, gap documentation, priority actions.
