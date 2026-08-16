# Subcontractor Scope Summary — Recurring "give me a summary of [discipline] scope" pattern

The user frequently asks for a one-shot summary of a subcontractor's scope (Structural, ICT/Telecom, Landscape, MEP, FLS, etc.). This is a **class-level task** — the same file set and output shape apply to every discipline. Do NOT treat it as a one-off.

## Where the data lives (check in this order)

| Source | What it gives you |
|--------|-------------------|
| `03_Scope/<Discipline>/README.md` | **Primary** — status, firm, appointment status, scope bullets, compliance gaps table, key gaps |
| `01_Registers/drawing_register.md` | Deliverable drawing codes (S-D-P-001, T-D-P-002, etc.) + source clause (ER §x / SoW §x) |
| `01_Registers/subcontractor_sow_raci_register.md` | Package scope, interface notes, appointment status |
| `Technical_Office/Specialist_Management/specialist_register.md` | Firm name, PQ code, CG code, appointment stage |
| `01_Registers/subcontractor_package_register.md` | Package-level status + candidate list |
| `02_Schedule/<Discipline>/README.md` | Submission plan, gates, milestones, slippage |
| `03_Plans/15_Subcontractor_Deliverables/Draft_SOW_RACI/<N>_<Discipline>_SOW_RACI_Draft.md` | Detailed included-scope table + exclusions/interfaces + deliverables |

## Output shape (the user expects this exact structure)

1. **Status line** — 🟡/🔴/🟢 + appointment state (Prequalifying / Appointed / Not appointed) + firm name.
2. **Scope table** — item | detail (from README scope bullets + drawing register).
3. **Deliverables table** — drawing codes + source clause (ER/SoW refs).
4. **Key problems table** — severity + issue (open conflicts, Code C rejections, not-appointed gaps).
5. **Compliance table** — Appendix A/B recognition, ER/SOW coverage, quotation status.
6. **Bottom line** — one-sentence verdict + the critical risk.

## Discipline-specific notes (Aseer Museum)

- **Structural** (`03_Scope/Structural_Contractor/`): Stramp, terrace sunshade, internal stairs, rigging supports, heritage strengthening. Watch SRC-003 (rigging cert) + SRC-005 (Stramp/landscaping boundary) open conflicts. DD rejected twice (Code C).
- **ICT/Telecom** (`03_Scope/CITC_Telecom/`): telecoms (fibre/Cat 6a, Wi-Fi, data points, BMS points) + MOI security (CCTV, ACS, AI cameras). ICT SI = SBS (approved, in agreement); CITC Telecom Engineer = TBD (not appointed). Authority submissions to CITC + MOI are critical-path.
- **Landscape** (`03_Scope/Evergreen_Landscaping/` + `03_Scope/TLC_Landscaping/`): hardscape/softscape/irrigation. TLC = leading candidate (PQ-0127 Code B) but **contract not executed**; Evergreen (PQ-0122 C) + PINE (PQ-0126 C) rejected. 50% gate slipped.
- **MEP**: design by AD Engineering, install by MEP Contractor (not awarded). Smoke management is in scope (ER §1.2 item l) — design by AD, validation by FLS specialist, install by MEP contractor.

## Pitfalls

1. **"Contract not done yet" is a common follow-up** — always state appointment/contract status explicitly in the summary (Prequalifying vs Appointed vs Contract executed). The user will ask if you don't.
2. **Design-vs-install split** — for MEP/FLS/ICT, state who designs vs who installs. A "not appointed" installer is a different risk than a "not appointed" designer.
3. **Drawing register codes are the deliverable evidence** — cite the code + source clause (e.g. `S-D-P-001 | 50% Detailed Structural Plan | ER §3.1.A.3`), not just prose.
4. **Check the specialist register for the firm + PQ code** — the README may say "TBD" while the specialist register names the actual candidate (e.g. SBS for ICT).
