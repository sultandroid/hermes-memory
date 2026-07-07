# DOCX→HTML Sync Workflow (Master-DOCX → HTML catch-up)

## When to use

The DOCX is the master (e.g. RevC03 from Word) and the existing HTML (e.g. RevC01 DRAFT) must be updated to match. This is the reverse of the "generate both from a single source" pattern — here the DOCX was already updated and the HTML is stale.

## Workflow

### Step 1: Extract DOCX structure for diff

```bash
python3 << 'PYEOF'
from docx import Document
doc = Document("/path/to/RevC03.docx")
for i, para in enumerate(doc.paragraphs):
    if para.text.strip():
        print(f"[{i}] {para.style.name}: {para.text[:200]}")
PYEOF
```

This shows all paragraphs with style names — key for spotting:
- NEW sections (paragraphs with no corresponding HTML section)
- REMOVED content
- Updated references (doc codes, dates, names)
- Changed heading text

### Step 2: Map differences

Create a change list by section:

| Section | Old HTML | New DOCX | Action |
|---------|----------|----------|--------|
| Cover | DRAFT, old date, old rev | CG REVIEW, new date, new rev | Update version/status/date |
| §1.1 Log | 3 rows (C00-C01) | 4+ rows (C00-C03) | Add new revision rows |
| §3 Org | Has Tech Director row | Removed Tech Director | Delete that row |
| §N | — | NEW section | Add full new page |
| ... | ... | ... | ... |

### Step 3: Delegate HTML rebuild to subagent

Do NOT rebuild the HTML yourself — it's too large. Delegate with:

**Goal:** "Rebuild [Plan Name] HTML from [Old Rev] → [New Rev]. Use the existing [Old Rev] HTML as base and update it to incorporate all [New Rev] DOCX changes."

**Context** must include:
1. The extracted paragraph list from Step 1
2. The section-by-section change map from Step 2
3. The EXACT CSS design system used in the existing HTML (colors, pill classes, page-header/footer, font stacks, section-header patterns)
4. The complete content of every new section (extracted from DOCX)
5. Output path for the new HTML file
6. Document numbering conventions (doc ref pattern, page count)

**Critical instructions in the delegation prompt:**
- "Keep ALL existing content not explicitly changed"
- "Use the same CSS classes and design system — do not redesign"
- "Do NOT overwrite the existing file — create a new [New Rev] file"
- List every section that must exist and its correct content
- Specify the footer text for every page
- Specify the page number counter update

### Step 4: Create register starter files (in parallel)

While the subagent builds the HTML, create starter registers:

**Physical Resource Register** — equipment, IT, vehicles, safety gear
- Columns: #, Resource ID, Category, Item, Spec, Qty, Unit, Location, Status, Assigned To, PO Ref, Delivery Date, Maintenance Due, Remarks
- Use openpyxl with navy headers, alternating gray rows, Calibri font

**Personnel Deployment Register** — names per SMP/KPR
- Columns: #, Name, Role, Tier, Organization, Start, End, Phase, Location, FTE, Status, Authority Reg., Training, Remarks
- Source personnel from SMP Rev03 / KPR

**Resource Risk Register** — detailed L×I risk scoring
- Columns: #, Risk Description, Category, Phase, Likelihood, Impact, RPN, Mitigation, Contingency, Owner, Status, Last Review

### Step 5: Create compliance audit files

Two files in `05_Compliance_Audit/`:

**PMBOK Structure Audit** — maps each PMBOK §9 process to the plan sections, plus 7th Ed. domain alignment. Tracks coverage (Full / Partial / Missing) and gaps.

**CG Compliance Checklist** — maps CG directives from companion plans to plan sections. Checklist format with Compliant/Partial/Non-Compliant status.

### Step 6: Update CG_STATUS.md

After the HTML is built, update `02_CG_Responses/CG_STATUS.md`:
- Bump `Last Updated` date
- Change status from "No CG response found" to "Ready for submission"
- Add revision and submission detail row
- Update action to "Submit via Hesham on Aconex"

### Verified working example

Aseer Museum Resource Management Plan C01→C03:
- 707 lines → 1,030 lines
- 9 pages → 13 pages
- 6 new sections added in a single delegation call
- 3 Excel registers created
- 2 compliance audit files created
- CG status updated
