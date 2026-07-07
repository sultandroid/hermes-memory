# Aseer Museum — Complete Subcontractor Register Workflow (June 2026)

This covers the full lifecycle of creating, serializing, consolidating, and programming submittal registers for all Appendix B subcontractor packages.

## Phase 1: Individual Package Registers

For each subcontractor discipline in Appendix B (`Subcontractors/_assets/APPendix B.pdf`):

1. **Read SOW + ER** — extract deliverables from specific SOW sections (6.22.x for design, 8.x for off-site fab) and ER (3.x for MEPF/IT/Security)
2. **Write SPEC.md** → `Subcontractors/NN_xxx_Contractor/_MANAGER_DASHBOARD/SPEC.md`
   - Scope, exclusions, deliverables by stage, standards, coordination interfaces, long-lead items, quality gates
3. **Generate Excel register** from SPEC.md data
   - 4 sheets: 50% / 90% / 100% / IFC+AFC
   - Exact SOW wording in descriptions
   - References only SOW § and ER §
   - Category headers matching SOW structure
   - Deploy to 3 locations: `02_Submittals/`, `Docs/09_Registers/`, `Subcontractors/NN_xxx/`
4. **QC review** via `delegate_task` to Kimi/Claude before presenting to user

### Long-Lead Flagging Rules
- Showcases: 14 weeks → 8 items at 50%
- MEP: 12-16 weeks → 13 items at 50%
- Exhibition Fit-Out: 8-12 weeks
- AV/IT: TBC but early coordination needed
- Structural+Rigging: survey-first — start in Month 1

## Phase 2: Numbering & Serialization

### Subcontractor Folders (per Appendix B order)
1. Renumber existing folders to match Appendix B sequence
2. Use temp names to avoid conflicts
3. Related packages grouped together:
   - Technology: Lighting(02) → Graphics(03) → AV(04)
   - MEP cluster: MEP(10) → MEP Designer(13) → FLS(11)
   - Structural: Structural(12) → Rigging(06)
   - Fit-out: FF&E(07) → Exhibition(08) → Interactives(09)
4. Merge duplicate packages
5. Non-Appendix-B items merged into related folders

### 09_Registers Folder Serialization
1. `_Master_Register_Index/` — no serial, sorts first
2. `_Master_Submittal_Register/` — no serial, sorts second
3. `01_...` to `31_...` — serialized real registers
4. Remove loose `.xlsx` files at root
5. `Specialist/` kept as-is

## Phase 3: Master Consolidation

After all individual registers exist:

1. **Master_Submittal_Register.xlsx** — Dashboard + 16 package sheets
2. **Design_Schedule_Programme.xlsx** — 5 sheets with DMP milestones
   - D0=LOA, D35=50%, D65=90%, D82=IFC, D88=AFC, D90=site, D300=TOC
3. Deploy both to all 16 subcontractor `_MANAGER_DASHBOARD/` folders

## Phase 4: Generator Script Path Maintenance

After renumbering, audit all generator scripts at `02_Submittals/*.py` for correct subcontractor paths, then regenerate all registers.
