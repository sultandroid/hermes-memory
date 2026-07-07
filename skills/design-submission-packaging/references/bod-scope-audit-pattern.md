# BOD Scope Audit Pattern

How to audit a submission plan against a BOD/SOW document before editing.

## Process

1. **Locate the scope document** — BOD (Basis of Design), SOW (Scope of Work), or Design Philosophy report. Each discipline typically has one. Search project folders for `*BOD*`, `*SOW*`, `*Scope*`, `*Design Philosophy*`.

2. **Extract scope items** — Read the document's scope section (often Section 1.2 or similar). List every numbered scope item with its exact wording.

3. **Map to proposed packages** — Create a side-by-side comparison:

   | BOD # | BOD Description | Proposed Package | Match? |
   |-------|----------------|-----------------|--------|
   | 1.2.1 | Review existing drawings | ASE-STR-REV-001 | ✅ |
   | 1.2.2 | ETABS model existing | ASE-STR-MDL-004 | ✅ |
   | ... | ... | ... | ... |

4. **Flag mismatches**:
   - **Extra items** — proposed packages with no BOD basis (e.g., Serviceability checks, Foundation assessment, Stability evaluation)
   - **Missing items** — BOD scope items with no proposed package (e.g., BOD 1.2.1 — drawings review)
   - **Merged items** — BOD items split into multiple packages or vice versa

5. **Present verdict** — Show the comparison to the user. Do NOT edit until user confirms.

## Example: Structural BOD Section 1.2

| BOD # | Description | Package | Verdict |
|-------|-------------|---------|---------|
| 1.2.1 | Review existing structural drawings and as-built conditions | ASE-STR-REV-001 | ✅ |
| 1.2.2 | Establish 3D ETABS model for existing building | ASE-STR-MDL-004 | ✅ |
| 1.2.3 | Analyze existing building under gravity and lateral loads | ASE-STR-CAL-002 | ✅ |
| 1.2.4 | Establish 3D ETABS model for modified building | ASE-STR-MDL-005 | ✅ |
| 1.2.5 | Analyze modified building under gravity and lateral loads | ASE-STR-CAL-004 | ✅ |
| 1.2.6 | Verify capacity of existing members + design strengthening | ASE-STR-CAL-003 | ✅ |
| 1.2.7 | Prepare comprehensive structural engineering report | ASE-STR-REP-006 | ✅ |

**Items removed (not in BOD):** Serviceability checks, Foundation assessment, Stability evaluation, Strengthening design details (merged into #6).

**Items added (missing from original list):** BOD 1.2.1 — drawings review.

## When No BOD/SOW Exists

If no scope document is found for a discipline:
- Use the existing register items as a starting point
- Flag to the user: "No BOD/SOW found for [discipline]. Register based on existing items. Verify with [discipline] engineer."
- Do not fabricate scope items
