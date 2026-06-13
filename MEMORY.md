# MEMORY — Procedural Knowledge

> Injected into every Hermes agent session. Compact, focused on stable facts.

## Aseer Museum (Project 219)

| Property | Value |
|----------|-------|
| Odoo ID | 219 on SAMAYA Odoo |
| Contract | MoC × Samaya, lump-sum, NTP 01-Dec-25 → 07-Sep-26 |
| Design Lead | NRS (Nissen Richards Studio) — A2742 (interior arch + scenography) |
| Consultant | CG (Consultancy Group) — Hossam Mabrouk (hmabrouk@cg.com.sa), Mohammad Elbaz (melbaz@cg.com.sa) |
| AV/IT/Interactives | Rawasin (T2-09) |
| Interactive Design | Subcon 19 |
| Subcon RFI Register | `Docs/09_Registers/Subcontractor_RFI_Register/` |

### Team
- **Sultan Issa** (ID 151) — Technical Office Mgr (DD packages ONLY)
- **Mohamed Samir** (ID 564) — Site / Procurement
- **Hani Alghamdi** (ID 478) — Purchasing
- **Hesham Abdelhameed** (ID 163) — Document Control
- **Ahmed Salah** (ID 162) — Project Coordination
- **Ali Abdelrahman** (ID 160) — Technical Office (design only)
- **Adel Darwish** (ID 7) — PM
- **Mohamed Elshaikh** (ID 157) — Project Planner (NOT general team)

### Odoo Task Rules
- **MAIN** (package): `parent_id=False` → Kanban card
- **SUBTASK** (deliverable): `parent_id=PackageID` → hidden inside parent
- **SUB-SUBTASK**: `parent_id=StageSubID` → 2 levels deep
- ALL tasks MUST have `date_assign` + `date_deadline`
- Progress: 0.0–1.0 scale (NOT 0–100)
- State: `1_done` / `03_approved` / `02_changes_requested` / `01_in_progress`
- Kanban filter: `parent_id=False`
- Assignee: `user_ids: [(4, uid)]` (NOT `user_id`)
- Tags: `tag_ids: [(4, tag_id)]`

### Stage IDs (Samaya, Project 219)
| ID | Name | Use |
|----|------|-----|
| 35 | 01 Initiation | Prequal, studies, pricing, S00101 |
| 36 | 02 DD Stage | Design, plans, specialist pkgs |
| 39 | 03 Procurement | SC-01 Replica, material approvals |
| 659 | 04 Off-site Manufacturing | Replica, mfg orders |
| 40 | 05 On-site Work / Execution | Construction, site |
| 479 | 06 Handover | As-built, snagging |

### Key Packages
| ID | Name | Stage |
|----|------|-------|
| 3011 | 00 — Pre-Qualification & Procurement | 35 |
| 3014 | 02 — Pricing & RFQs | 35 |
| 2945 | 00 General | 36 |
| 2938 | 01 Architecture | 36 |
| 2939 | 02 Structural | 36 |
| 2940 | 03 MEP & IT | 36 |
| 2941 | 04 Life Safety | 36 |
| 2946 | 05 Projects Plans | 36 |
| 3013 | S00101 Contract Scope | 39 |

### Tags
| ID | Name |
|----|------|
| 140 | Prequalification |
| 141 | Plans & Procedures |
| 130 | A1-Architecture |
| 132 | S1-Structure |
| 133 | M1-MEP |
| 134 | L1-Life Safety |

### Submittal Registers
- Spec-first, Excel from spec
- 50%/90%/100%/IFC stages
- Appendix B only (subcontractor list)
- Non-DD packages skip 50/90/100/IFC stages

---

## BIM Unit Projects

| Project | Path | Doc Prefix |
|---------|------|-----------|
| Aseer Museum | `Aseer-Museum/` | MOC-MUS-ASE |
| Zamzam Visitor Center | `Zamzam - Visitor Center/` | ZAM-NWC |
| Masjid Alnoor | `Masjid Alnoor/` | — |
| Hera' Ghar | `Hera' Ghar/` | — |

---

## Schedule Audit Rules

- File ending at design gate (IFC) = design-phase-only, NOT full project
- Look for "DESIGN PHASES" in name
- Activity prefixes: PE/AS/EN/PR (design) vs CN/IN/TC/HD (construction)
- Check contract completion before flagging unrealistic timelines
- **Mohamed Elshaikh (ID 157)** = Project Planner, not general team

---

## OneDrive Rules

- OneDrive-locked PDFs ([Errno 11]): DON'T retry — use pre-existing `EXTRACT_*.md` in `Docs/07_Reports/07.5 Audit Report/`
- When extracting email attachments: ALWAYS copy to project folder, NEVER reference `/tmp` paths in Odoo

---

## Exchange Script

The memory exchange script at `~/.hermes/scripts/memory_skills_exchange.sh` syncs between:
Hermes · Claude Code · Codex · Kimi · Pi Agent · Gemini · OpenClaw · Kilo

Unified output: `~/.hermes/shared_exchange/UNIFIED_MEMORY.md`
