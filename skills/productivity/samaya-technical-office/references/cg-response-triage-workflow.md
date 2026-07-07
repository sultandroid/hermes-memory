# CG Response Triage & Submittal Workflow

## When to Use

CG (Consultant/PMC) has returned review comments on a design/visualization/material submittal. You need to process the response, triage comments, coordinate with the designer, update project systems, and prepare a formal reply.

## Workflow

### Phase 1: Receive & Verify

1. **Read the CG email, not just the PDF** — The email header may state a different status than the PDF body text. E.g., email says "C — Revise and Resubmit" while PDF says "generally accepted." Always trust the email status line first.

2. **Save the PDF** to the project submittals folder:
   ```
   06_PDFs/Submittals/YYYY-MM-DD_SubmittalNo___Description.pdf
   04_Submittals/ (copy)
   ```

3. **Extract all comments** from the PDF into a structured list. Classify each:
   - **✅ Fair** — valid technical corrections, accept and action
   - **❌ Illogical** — against project stage, scope, or agreed plan
   - **❓ Needs clarification** — CG didn't specify enough detail
   - **⚠️ Spec issue** — relates to material spec that may be insufficiently defined

#### 2. Search all schedule JSON files

Before accepting or rejecting any material/finish comment:
   - Search ALL schedule JSON files under `data/schedules/*.json` (19+ types: finishes, setwork, showcase, graphic, wayfinding, FF&E, AV, etc.)
   - Use Python/execute_code to scan for terms like 'patinated', 'brass', 'bronze', 'copper', RAL codes, specific finish codes (FI_ME_01, FI_ST_03, etc.)
   - Do NOT rely on browser/UI views of the hotspot app — virtualized tables may not show all rows in the DOM
   - For each match, extract: Material ID, Description, Treatment/Finish, Colour, Supplier
   - Key finding pattern: if supplier is "TBC Locally Sourced" with no RAL/product code, the spec is not fully defined
   - CG's "revert to approved spec" is valid only if the approved spec has a defined product reference. If TBC, the contractor must source and submit for approval — CG cannot demand an undefined product.
   
#### 3. Cross-reference against project stage
   - Arch viz renders are not coordinated shop drawings — MEP/systems in renders is typically out of scope
   - Package scope definitions (what was agreed to be included/excluded) may override CG assumptions
   - The submittal register structure was agreed at project kickoff

### Phase 3: Coordinate with Designer (NRS)

6. **Forward your analysis to NRS** for their input before drafting the formal response:
   - Group into "Accept & fix" vs "Our position to push back"
   - Flag items needing clarification
   - Ask for their confirmation on scope/technical points
   - **Tone**: informal/collaborative — "my read on each point"

7. **Consolidate NRS feedback** into the triage matrix:
   - NRS may confirm your pushback or raise additional issues
   - They may ask for specification references you don't have
   - Update the classification based on their input

### Phase 4: Respond to Designer First

8. **Reply to NRS** confirming alignment on each point:
   - Which items are accepted for action
   - Which items you'll push back to CG (with NRS backing)
   - Which items need CG clarification first

### Phase 5: Update Project Systems

9. **Update Odoo task** — create/update task with:
   - Correct CG status (A/B/C/D — from email, not PDF narrative)
   - Full email thread context (timeline of emails, who said what)
   - NRS feedback per comment point
   - Strategy decisions made
   - Progress: 0.3 (received) → 0.5 (triaged) → 0.7 (coordinated) → 0.9 (response drafted)

10. **Update Submittals Log** (Excel) — correct or add:
    - Status column: A/B/C/D from email
    - Remarks column: summary of key comments, NRS feedback, decision

11. **Update memory** — compress old entries if needed; add:
    - Submittal number + date + status
    - Key decisions (e.g., "sample first, then render")
    - NRS confirmations (e.g., "G7/G10/G13 excluded per scope")

### Phase 6: Draft Formal Response to CG

12. **Respond to each comment** based on triage:

| Classification | Response Strategy |
|---------------|------------------|
| ✅ Fair | Concur, action underway, timeline |
| ❌ Illogical | Push back with contractual/scope basis |
| ❓ Needs clarification | Ask CG for specifics before actioning |
| ⚠️ Spec issue | "Will source matching sample for approval, then update deliverables once approved — no double work" |

13. **Key principles for the response:**
    - **Sample first, render once** — When CG rejects a specified finish, source and submit an approved sample FIRST. Get CG approval. Then update renders. Never render twice.
    - **Spec responsibility** — If the approved spec lacks product code/RAL/supplier (e.g., "TBC Locally Sourced"), CG cannot demand "revert to approved spec" without providing the missing reference. The contractor's obligation is to source and submit a matching sample for approval.
    - **Scope is scope** — If something was agreed excluded from a package, state it clearly with reference to the agreed scope document.

## Worked Example: Arch Viz CG Response (17-Jun-2026)

**Submittal:** MOC-MUS-ASE-1A0-ZD-0060 — Arch Visualization 3D Shots (Package 01)
**CG Status:** C — Revise and Resubmit
**CG Reviewer:** Mansour Alrezeni (via Hossam Mabrouk)

| Comment | Classification | Resolution |
|---------|---------------|------------|
| All MEP/systems shall be reflected | ❌ Illogical — viz renders ≠ shop drawings | Push back |
| Missing material board + FF&E | ⚠️ Spec issue — hotspot platform exists | Provide CG access to hotspot |
| Gallery-by-gallery | ❌ Illogical — agreed floor-by-floor | Inform CG, suggest submission plan amendment |
| G7/G10/G13 missing | ❌ Illogical — excluded per scope | Push back with NRS confirmation |
| Tile pattern wrong | ✅ Fair — accept | Action NRS (awaiting CG clarification on movement joints) |
| Annotations G5 missing | ❓ Needs clarification — NRS doesn't know what's missing | Ask CG to specify |
| View 6 improve | ❓ Needs clarification — no detail provided | Ask CG to specify |
| Brass finish revert (FI_ME_01) | ⚠️ Spec issue — supplier TBC, no RAL/sample | Source sample first, submit for approval, then render once |

**Odoo:** Task #3292 under Procurement pkg 3146
**Submittals Log:** Row 18 — status corrected to C
