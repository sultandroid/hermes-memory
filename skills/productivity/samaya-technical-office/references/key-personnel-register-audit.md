# Key Personnel Register Audit — Cross-Reference Against Subcontractors & Contract

## When to Load

- User asks "why is X missing from the KPR?"
- User asks "who in Samaya handles Y?"
- User asks to audit KPR completeness against subcontractors or contract requirements
- A new subcontractor folder was created and needs to be reflected in KPR

## Audit Methodology

### Step 1: Read the Key Personnel Register

Read `Aseer_Museum_Key_Personnel_Register.xlsx` → extract all rows:
- Tier 1 (Management) — 6 roles
- Tier 2 (Design Specialists) — ~22 roles
- Tier 3 (Testing & Authority) — ~10 roles

Note assigned entities (Rawasen, ZNA, Glasbau Hahn, NRS, TBC, etc.) and MoC Approval Status.

### Step 2: Read the Subcontractor Prequalification Register

Read `Docs/02_Plans_and_Procedures/02.1_DMP/03_Registers_and_Lists/Subcontractor_Prequalification_Register.md` — extract Categories A–H:

| Category | Scope | MoC Approval? |
|----------|-------|--------------|
| A — Management | 6 roles | ✅ Yes |
| B — Exhibition Design | 7 specialists (AV, Interactives, Setworks, Models, Graphics, Lighting, Showcase) | ✅ Yes |
| C — Engineering Design | 5 specialists (Structural, MEP, FLS, Shade, Landscaping) | ✅ Yes |
| D — Construction Trades | 21 trades (Demolition, Steel, MEP, Showcases, Rigging, etc.) | 🟡 Review |
| E — Testing & Commissioning | 5 ITCA disciplines | ✅ Yes |
| F — Authority-Registered | 6 specialists (SEC, Municipality, CITC, MOI, Fire Dept, Fire-Proofing) | ✅ Yes |
| G — Material Suppliers | 20+ long-lead material categories | No |
| H — Excluded / MoC-Direct | 6 items (Scenographer, AV Content, Mounts, Art Handling, Conservation, CMS) | N/A |

### Step 3: Cross-Reference

For each specialist requiring MoC approval (Categories B, C, A), check if the KPR has:
1. A corresponding row with the right role title
2. An assigned entity (not TBC)
3. Matching MoC Approval status

Gaps fall into 3 types:

| Gap Type | Signal | Example |
|----------|--------|---------|
| **Not yet identified** | Prequal Register has it, KPR doesn't | Interactive Design Specialist (wasn't in original SoW Appendix B; identified via NRS RFI) |
| **Listed but unassigned** | KPR has the role, but entity = TBC | Landscaping Specialist (R19), Acoustic Specialist (R32) |
| **Assigned but entity wrong** | KPR assigns to wrong entity | Mech/Electromech Interactives (R15) assigned to Rawasen — covers hardware only, not interactive design |

### Step 4: Check Subcontractors/ Folder

The numbered folders (01–19) reveal what actually exists vs what's in the formal register. Cross-reference:

| Subcontractor # | Trade | In KPR? | In Prequal Register? |
|-----------------|-------|---------|---------------------|
| 03_AV_IT | Rawasin | ✅ R11 AV Hardware | ✅ B-01 |
| 04_Lighting | ZNA | ✅ R12 | ✅ B-06 |
| 02_Showcases | Glasbau Hahn | ✅ R13 | ✅ B-07 |
| 19_Interactive_Design | (new) | ❌ MISSING | ❌ Not in original Appendix B |
| 14_Rigging | (D-21) | ❌ MISSING | ✅ D-21 |

### Step 5: Trace to Contract Source

When a specialist exists in Subcontractors/ but not in KPR, check:
- **SoW Appendix B** — defines the 20 original specialist categories. If not there, the specialist was identified after KPR issuance
- **NRS RFI / scope gap** — the trigger document that identified the need
- **T2 allocation table** (`Knowledge Notes - Stakeholder Mgmt Plan Rev02.md`) — shows contractual responsibility umbrella

## Scope Tracing Methodology

When user asks "who does X in Samaya?" or "is X in Samaya's scope?":

```
1. Check Category H (Excluded/MoC-Direct)
   ├─ If listed → Samaya provides coordination only, not the work
   │  e.g., H-03 Mounts Package → Samaya provides mounting points + display case coordination
   │
2. If not in H, check Categories B, C, D
   ├─ B = Exhibition Design (AV, Lighting, Showcases, Interactives, etc.)
   ├─ C = Engineering Design (Structural, MEP, FLS, etc.)
   ├─ D = Construction Trades (Rigging, Steel, MEP Install, etc.)
   │
3. Check KPR for assigned Key Personnel
   ├─ Who is the named individual/entity?
   │
4. Check RACI matrix for R/A/C/I
   ├─ Who is Responsible? Accountable? Consulted? Informed?
   │
5. Check subcontractor SCOPE_REQUEST.md
   ├─ Specific scope detail, interfaces, sign-offs
```

### Worked Example: "Who provides mounting points?"

| Layer | Finding | Source |
|-------|---------|--------|
| Category H | H-03 Mounts Package = Supplied by others (MoC-direct) | Prequal Register |
| Category D | D-21 Specialist Rigging covers structural anchors, catwalks, suspension | Prequal Register |
| KPR | Eng. Ahmed Gad (Structural) approves capacity; Rigging Contractor installs | KPR R8 |
| RACI | CTR (Samaya) = R/A for "Provide Attendance for Other MoC Contractors" | RACI row 160 |
| SCOPE_REQUEST | Rigging sub engineers, installs, load-tests, certifies anchors | `14_Rigging_Contractor/SCOPE_REQUEST.md` |

**Conclusion:** Structural anchors/rigging = Samaya scope via D-21. Custom artifact mounts = MoC-direct (H-03). Samaya provides structural mounting points (via Rigging sub + Structural Engineer) and coordinates with Showcase Specialist (Glasbau Hahn) for display case integration.

## Common Gaps to Flag

| Missing Role | Why It's Missing | Fix |
|-------------|-----------------|-----|
| Interactive Design Specialist | Not in original SoW Appendix B (identified 2026-06-07 via NRS RFI A2742-6.04-018) | Add Tier 2 row: Interactive Design Specialist → TBC → Pending submission |
| Rigging Specialist | D-21 exists in Prequal Register but never promoted to KPR | Add Tier 2/3 row for Rigging coordination |
| Acoustic Specialist | Listed as TBC (R32) — no entity assigned | Source an acoustic consultant |
| Landscaping Specialist | Listed as TBC (R19) — no entity assigned | Source a landscape architect |

## Pitfalls

- **KPR is a snapshot, not live** — Rev C02 was 2026-05-06. Subcontractors created after that date (e.g., #19 Interactive Design on 2026-06-07) won't appear. Check Subcontractors/ folder dates.
- **SoW Appendix B is not exhaustive** — the original 20 specialist categories didn't cover Interactive Design. New needs emerge during design development.
- **NRS scope exclusion ≠ Samaya gap** — When NRS says "not our scope," the responsible party is likely a T2 subcontractor, not a new gap to fill. Check T2 allocation table first.
- **T2-09 umbrella** — Interactives sit under Rawasin umbrella per T2 allocation. New Interactive Design sub coordinates with Rawasin (sister company), not replaces them.
- **H-03 ≠ D-21** — Mounts Package (object mounting hardware) is MoC-direct. Specialist Rigging (structural anchors, catwalks) is in Samaya scope. Don't conflate.
- **Document Control** — KPR additions should be made in the Excel file itself, tracked with a revision bump, and reflected in the KPR summary (roles total, approval count).

## KPR-to-HTML Plan Alignment

When updating a management plan HTML (e.g., Resource Management Plan) to match the KPR:

### Approval Status Mapping

| KPR Status | HTML Treatment | Example |
|------------|---------------|---------|
| Approved / Approved with Comments (Code B) | Show entity name + approval date | AD Engineering · Code B approved 15-Jun |
| Pending submission | Show person's name — they are ON BOARD | Eng. Mohamed Samir (do NOT blank out) |
| C - Revise and Resubmit (Code C) | Show person's name + "Code C" status | Dr. Ehab Foda — Code C (revise & resubmit) |
| Vacant | Show "Vacant" — the role has no person | QA/QC Manager: Vacant |
| TBC / Not yet appointed | Show "TBC" — no one hired yet | T&C Manager: TBC |
| Nominated - pending approval | Show entity + "Nominated" | Lumotion (nominated — NDA signed) |

### User Preferences for Personnel Display

- **NO** "pending MoC submission" labels next to names
- **NO** "Overseas" or location qualifiers next to names
- **NO** blanking out names of on-board personnel (pending submission = on board)
- Show the name only; the KPR is the authoritative source for approval status
- The plan document does not need to restate KPR approval status for every role

### Entity Name Corrections (Common Errors)

| Wrong (in HTML) | Correct (per KPR) |
|-----------------|-------------------|
| Nama Al Amal | Nama Consulting |
| Glassbühne | Glasbau Hahn |
| NRS (generic) | NRS — Nissen Richards Studio (first reference), NRS thereafter |

### Tier Structure (KPR Rev C05, 2026-06-19, updated 19-Jun)

- **Tier 1** (6 roles): PD, Construction Manager, BIM Manager, HSSE Manager, QA/QC Manager, T&C Manager
- **Tier 2** (~22 roles): Structural, MEP Design, Lighting, FLS, Showcases, Setworks, AV, Interactives, Models, Graphics, Shade, Landscaping, Arch, Interior, Accessibility, IT/Data, Land Surveyor, Acoustic, Rigging, Sustainability, Scenographer, Procurement
- **Tier 3** (1 role): ITCA (Critical Path) — Fire-Proofing Contractor removed per Appendix B
- **Statutory**: SEC Electrical, Municipality Structural, CITC Telecom, MOI Security

### Appendix B — Authoritative Specialist Package List

**Source**: `Subcontractors/_MANAGER_DASHBOARD/APPendix B.pdf` (NRS, Jan 25)

Appendix B defines the approved specialist contractor packages. When populating a plan's specialist roles:

- **Follow ONLY Appendix B** — do not add roles from the KPR or other sources that aren't in Appendix B
- If a role exists in the KPR but NOT in Appendix B, remove it from both the plan AND the KPR
- User directive: "we follow only the Appendix B" — don't add extra work that isn't required

**Example**: Licensed Fire-Proofing Contractor was in KPR (Tier 3, ER §3.2.B.3) but NOT in Appendix B. Removed from both plan and KPR. Fire-stopping scope absorbed into Nama Consulting's FLS discipline ("fire-stopping design" added to Nama's scope, installation by M&E Contractor).

**Appendix B packages** (specialist + management):
- Specialist: Model Maker, Lighting Designer, Graphics, AV Hardware, Conservation Showcase, Specialist Rigging, FF&E, Exhibition Fit-Out (Setworks), Interactives, M&E, Fire Life Safety, Structural, Health & Safety, IT/Data, Surveyor, Accessibility, Architect, Acoustic, Interior Design, Landscape
- Management: Exhibition Fit-Out Contractor (management works)

**Not in Appendix B (do NOT add to plans)**: Fire-Proofing Contractor, Conservation Consultancy (standalone)

### KPR Excel Updates When Removing Roles

When removing a role from the KPR Excel:
1. `ws.delete_rows(row_num)` — remove the row
2. Update the entity that absorbs the removed scope (e.g. Nama gets fire-stopping in discipline + notes)
3. Summary formulas use `COUNTIF`/`COUNTA` — they auto-recalculate, but verify the ranges still cover correct rows after deletion (e.g. `B2:B31` → `B2:B30`)
4. Statutory rows shift up by 1 after deletion — update any `B35:B38` range references to `B34:B38`
5. Save and verify with a read-back

### KPR Excel Updates When Adding Roles

When adding a new role to the KPR Excel:

- **Do NOT use `ws.insert_rows()`** — it silently loses data on save in OneDrive-synced files. The row appears inserted in memory but the written values vanish when the file is saved and reopened.
- **Instead**: find the first empty row before the STATUTORY header and write directly to it with `ws.cell(row=N, column=c).value = ...`. This is reliable.
- After adding, verify with a read-back: `ws.cell(row=N, column=1).value` should return the value you wrote.

### TBC Cell Highlighting

Highlight all TBC cells in the KPR so unfilled roles are visually obvious:

```python
from openpyxl.styles import PatternFill
yellow = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
for row in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=ws.max_column):
    for cell in row:
        if cell.value and 'TBC' in str(cell.value):
            val = str(cell.value).strip()
            if val == 'TBC' or val.startswith('TBC ') or val.startswith('TBC(') or val.startswith('TBC\n'):
                cell.fill = yellow
```

This catches both Name-column TBCs and Authority Registration TBCs (e.g. "TBC — Saudi Council / equivalent").

### CG Site Instruction Exception to Appendix B Rule

Appendix B is the authoritative specialist package list, BUT a CG site instruction can mandate a role that isn't in Appendix B. In that case:

- **Add the role to both the KPR and the plan** — the CG site instruction is a formal directive that supersedes Appendix B
- **Note the CG site instruction reference** in the KPR remarks column (e.g. "Per CG site instruction MOC-MUS-CG-ASE-1KN-PQ-013")
- **Add "per CG site instruction" to the plan's role description** so CG/MoC can see it's their own requirement, not Samaya adding scope
- Example: ICT / Security System Integrator is NOT in Appendix B but was formally requested via CG site instruction → added to KPR Tier 2 and plan
