# Email Pipeline Execution — 2026-07-24 (14:30)

## Summary
95 emails scanned (48h window). 33 project-critical identified. 52 files extracted, 47 routed to project folders.

## Key Documents Routed

### CG/Hossam Mabrouk
| Doc Code | Description | Routed To |
|----------|-------------|-----------|
| ZD-0093 | Risk Management Plan | `02.17_Risk_Management_Plan/01_Source_Files/` |
| ZD-0092 | UPS Assessment | `Electrical/UPS_Assessment/` |
| ZD-0091 | Earthing Assessment (+ CG response x3 copies) | `Electrical/Earthing_Lightning/` |
| ZD-0086 | Project Execution Plan | `02.2_Project_Execution_Plan/01_Source_Files/` |
| ZD-0095 | QA/QC CV (Aftab Adeel) | `09_General/01_Prequalification/` |
| 1A0-1G-0008 | Arch DD First Floor 50% | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-ZD-0096 | Arch Title Block Template | `03_Design_Files/Architecture/` |
| PQ-0126 | Landscaping PINE | `Landscaping/01_Prequalification/` |
| PQ-0127 | Landscaping TLC | `Landscaping/01_Prequalification/` |

### PM/Waris
| Doc Code | Description | Routed To |
|----------|-------------|-----------|
| — | SMP Rev01 (.docx/.pdf/CR/Review) | `02.5_HSE_Plan/01_Source_Files/` |
| — | All Discipline Trackers (submission plan) | `02_Schedule/` |
| — | Executive Minutes + Actions List | `00_Status/` |
| — | Stockholder List | `00_Status/` |

### Design/Hesham
| Doc Code | Description | Routed To |
|----------|-------------|-----------|
| ZD-0098 | EMDP/SDP Assessment | `03_Design_Files/Electrical/` |
| ZD-0090 | MDP Assessment | `Electrical/Current_Condition_MDP/` |
| ZD-0088 | ATS Assessment | `Electrical/ATS_Assessment/` |
| — | Daily Reports (22-23 Jul) | `00_Status/Daily_Reports/` |

### Subcontractors
| Topic | Description | Routed To |
|-------|-------------|-----------|
| Landscaping | Evergreen Prequal + Zip | `Landscaping_Specialist_Evergreen/01_Prequalification/` |
| Acoustic | Technical & Financial Proposal | `03_Acoustic_AME/` |
| Ceiling | Baffle Ceiling RFQ + Finishes Schedule | `ASM_Ceiling_Systems/` |
| Rigging | SOW RACI (x2 copies) | `06_Rigging/01_Scope_of_Work/` |
| Molitor | Scope of Work + Archive Zip | `Molitor/01_Scope_of_Work/` |
| AV/IT | Distributor Cert + MediaCast License | `AV_IT/` |

### Other
| Doc Code | Description | Routed To |
|----------|-------------|-----------|
| — | Schedule Update 23-07 (.xer/.xml/.pdf) | `02_Schedule/` |
| — | Safety Observation SOR-013 | `02.5_HSE_Plan/` |
| ZD-0020 Rev.03 | Stakeholder Plan (legacy) | `03_Design_Files/` |
| 1A0-1G-0006 | Arch DD (legacy) | `02_Submittals/01_DD_Gate/Architecture/` |

## New Document Codes Encountered

This session introduced routes for:
- **1E0-ZD-0088/90/91/92/98** — Electrical assessment reports with specific subfolders per assessment type
- **1A0-1G-0008** — Arch DD First Floor 50% (newest DD package)
- **1A0-ZD-0096** — Title Block template (not a DD submittal; goes to design files)
- **1K0-ZD-0093** — RMP
- **1K0-ZD-0095** — QA/QC CV
- **Evergreen_Prequalification** — New landscaping specialist

## Pitfalls Encountered (New)

1. **ZD-0096 destination**: Title Block template goes to `03_Design_Files/Architecture/`, not `02_Submittals/01_DD_Gate/Architecture/`. It's a template, not a design gateway submittal.
2. **Keyword-only filenames**: Files like "TB for approval.pdf", "TECHNICAL & FINANCIAL PROPOSAL.pdf", "A2742-1910C.pdf" have no doc code in the name. Need filename-keyword routing rules, not doc-code regex.
3. **-2700 errors persisted**: 3 emails (49037, 49079, 49019) had corrupt attachment metadata. Only forwarded .eml saved for each — no PDF/Excel. Standard Outlook behaviour for certain malformed messages.
4. **Sibling write_file collision**: A concurrent subagent wrote to `/tmp/gen_extract_scripts.py` while the main thread wrote its own. The collision was detected by the `write_file` tool warning but the sibling's content was silently overwritten. Use unique temp paths per session to avoid.

## Registers
- No new NCRs, risks, or register-impacting items detected
- Review log saved to `03_Plans/08_Risk/reviews/email_scan_2026-07-24.md`
- Git commit `4cfb9f5`, pushed to origin/main
