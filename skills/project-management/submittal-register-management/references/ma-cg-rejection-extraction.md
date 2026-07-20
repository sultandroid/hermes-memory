# Material Submittal (MA) Register — CG Rejection Reason Extraction

When a material submittal shows Code C or D without the rejection reason, extract the verbatim CG comment from the Approval PDF.

## Workflow

1. **Locate the PDF** — in Adel Darwish's OneDrive:
   ```
   /Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Adel  Darwish's files - 01- Execution Documents/08- Material Submittal MA/{Discipline}/{MA-Ref}/Approval/
   ```
   Note: the path has a **double space** in "Adel  Darwish's" — use quotes.

2. **Extract text**:
   ```bash
   pdftotext "/path/to/Approval/001.pdf" - 2>/dev/null
   ```

3. **Record for each submittal:**
   - Submittal ref (MA-XXXX)
   - CG reviewer name (from signature block)
   - Date of response
   - Verbatim CG comment text
   - Code assigned (A/B/C/D)

4. **Cross-reference the underlying PQ** — the same CG comment often applies to both the MA and its underlying prequalification (PQ). Check if the PQ was also rejected for the same reason.

5. **Update:**
   - Material submittal register (`01_Registers/material_submittal_register.md`) — add verbatim comment to reconciliation notes
   - Risk register (`01_Registers/risk_register.md`) — update cause and evidence columns
   - Compliance gaps (`Technical_Office/Compliance_System/compliance_gaps.md`) — update notes

## Common CG Rejection Reasons for MA Submittals

| Reason | Example | CG Verbatim |
|--------|---------|-------------|
| Single supplier (CG requires 3 options) | MA-0001 (Porcelain Tiles), MA-0006 (Showcases) | "Rejected — submit 3 options for porcelain" |
| Missing test reports (Oddy, fire, VOC, MSDS) | MA-0007 (Patinated Brass) | Required: manufacturer info, certificates, MSDS, fire-rated report, Oddy test, VOC test, off-gassing test, chemical composition |
| Non-compliant material spec | MA-0006 (anti-reflective glass) | "The submitted anti-reflective glass is not in compliance with the specified material descriptions" |
| Incomplete technical data | MA-0006, MA-0007 | "Submission found incomplete. Code C. The submitted materials do not comply with the provided specifications and lack the required technical information." |

## Known CG Reviewers for MA Submittals

| Reviewer | Submittals Reviewed | Tendency |
|----------|-------------------|----------|
| Haitham Elhussein | MA-0001 (Code D), PQ-0026 (Code D), PQ-0063 (Code B) | Approval-oriented with conditions. Rejects single-source submissions. |
| Mansour Alrezeni | MA-0006 (Code C), MA-0007 (Code C) | Strictest material reviewer. Requires full technical data + alternative suppliers. |

## See Also

- `cg-analysis-and-lessons` skill — full CG rejection pattern analysis system
- `cg-response-protocol` skill — CR sheet response framing for material resubmissions
