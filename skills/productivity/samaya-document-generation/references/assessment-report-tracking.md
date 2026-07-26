# Assessment Report Tracking — Multi-Source Workflow

When the user asks "who does the electrical/mechanical assessment" or "what's the status of assessment reports":

## Step 1: Find the Company

Search the **prequalification register** for the scope:

grep -i "testing.*assessment\|assessment.*electrical\|PQ-008" prequalification_register.md

Key patterns:
- PQ-0084 = TABCOMM (testing & assessment of Elec, Plumb, Mech, except HVAC)
- PQ-0085 = Global Innovation (BMS assessment, later superseded by GITCO PQ-0118)
- PQ-0097 = AD Engineering (MEP design, post-assessment)

## Step 2: Find Submitted Reports

Check the **deliverables master list** for Phase 2 (Site Assessment) deliverables under codes S-P-*:

S-P-02 = Engineering Site Report — MEP
S-P-09 to S-P-20 = Measurement & Validation reports (power, fire, BMS, HVAC, CHW, etc.)

Then search Outlook SQLite for assessment document codes with `LIKE '%Assessment%' AND LIKE '%MOC-MUS-ASE%'`.

Document codes follow: `1E0-ZD-XXXX` (electrical) or `1M0-ZD-XXXX` (mechanical).

## Step 3: Check CG Response Status

CG responses come from hmabrouk@cg.com.sa or melbaz@cg.com.sa. 
CG codes: B = Approved w/ comments, C = Revise & Resubmit.
Search Outlook SQLite for the doc ref with `Message_SenderAddressList LIKE '%@cg.com.sa%'` and check `Message_Preview` for "B -" or "C -".

## Step 4: Verify Against Adel Darwish Snapshots

The Adel folder snapshots (`99_Archive/adel_snapshots/file_list.txt`) reveal approval status through folder structure — presence of an `Approval/` subdirectory under a doc ref folder = CG has responded. Presence of `Rev.01/` = revision submitted after initial comments.

## Step 5: Update All Registers

Update in this order:
1. `03_Scope/{Company}/README.md` — full tracker
2. `01_Registers/submittal_register.md` — Assessment Reports Dashboard
3. `01_Registers/prequalification_register.md` — PQ entry notes
4. `Technical_Office/Specialist_Management/specialist_register.md` — company row
5. `01_Registers/risk_register.md` — PRR-MEP-02 risk entry

## Common Assessment Reports (Aseer Museum)

Electrical (ZD-0084 to ZD-0098) — TABCOMM — 3 Code B, 5 Pending, 1 Code C
Mechanical (ZD-0065 to ZD-0070) — TABCOMM — ZD-0065 Approved, ZD-0070 Rev.01 Pending
BMS (RP-0039) — GITCO — Code B
Fire Alarm/Suppression (MEP-ZD-0067) — AD Engineering — Code C
Structural/Arch (RP-0003) — TBC — Likely Approved

## Pitfalls

- OneDrive files are unreliable (Resource deadlock avoided). Use repo clone at /Volumes/MIcro/Temp/aseer-museum-pm/.
- Emails show submission, not approval. CG codes appear as "B - Approved with Comments".
- Adel snapshots are periodic — check file dates for recency.
- ZD-0065/0070 were submitted earlier (Jun) than ZD-0084+ (Jul) despite higher numbers.
- CG can recall and reissue same day (Code C recalled → reissued as Code B).
