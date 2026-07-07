# Drawing Review Comment Letter — Samaya → Consultant (CG)

## When to Use

Drafting a formal comment letter from Samaya Technical Office to the design consultant (CG, NRS, ZNA, etc.) reviewing a submitted drawing package (DD, IFC, or other stage). Typically follows PMC/internal review of consultant's drawing submission.

## Workflow

### Step 1 — Inventory the Drawing Package

Browse the submitted drawing folder on OneDrive to catalog actual drawing numbers:

```bash
# Find all PDFs — folder name is the category
ls "<OneDrive>/Arch DD Drawing/<Category>/<Subfolder>/"
```

Key things to note:
- Which categories are present vs missing (e.g., empty `Sections/` folder)
- Drawing number format (old CG numbering vs ISO format)
- Stamped vs unstamped versions
- Title block version used

### Step 2 — Structure the Letter

Opening header:
```
Subject: [Project] – [Stage] Drawing Review – Samaya Technical Office
To: [Contact Name], [Consultant Firm]
Date: [dd Month yyyy]
Deadline: [Concrete date — e.g., Thursday, 25 June 2026]
```

Body structure — numbered items, each a single directive:

| Section | Content |
|---------|---------|
| **Must-Fix items** | Numbered items requiring action in the **next submission**. Lead with: "Address the following items in your next submission. Non-compliant sheets will be returned without review." |
| **Advisory items** | Labelled with **(Advisory)** — deferrable to future versions. Use softer language: "Where possible..." / "If already produced, defer to next version." |

### Step 3 — Item Categorization Rules

| Type | Label | Deadline | Language |
|------|-------|----------|----------|
| Mandatory fix | Numbered item | Next submission | "Must" / "All sheets must" / "Required" |
| Deferrable | Numbered item **(Advisory)** | Next version | "Where possible" / "Defer to next version" |
| Administrative | Numbered item | Next submission | Name the specific document/register to cross-check |

### Step 4 — Drawing Reference

For items about specific drawing issues, reference the actual sheet numbers from the package:
- Use the exact folder structure to confirm what exists
- Call out empty folders explicitly (e.g., "1350_1500_Sections/ is empty — no building sections submitted")
- For missing drawings: name the specific category/sheets

### Step 5 — Tone & Style

- **No fluff** — each item is one sentence or a short bullet list
- **No explanatory paragraphs** — just the directive
- **Concrete deadlines** — specific date, not "soon" or "ASAP"
- **Clear consequence** — "Non-compliant sheets will be returned without review"
- **No excessive politeness** — professional but direct

## Example Structure

```
**Subject:** Aseer Regional Museum of Art – DD Drawing Review – Samaya Technical Office
**To:** Jim, CG
**Date:** 16 June 2026

Dear Jim,

Address the following items in your next submission. Non-compliant sheets
will be returned without review.

---

**1. Title Block & Reference Log**
Use the approved Samaya title block template. Complete all Reference Log tables.

**2. Drawing Numbering**
Reissue all sheet numbers per the ISO coding system in the DMP, BEP, and
contract annexures.

**3. Drawing Quality**

a) Internal Elevations – Include hatch patterns with Type Marks matching
the legend, overall and detail dimensions, and all architectural elements.

b) Floor Finish Plans – Remove floor and construction joints (defer to IFC).

c) Reflected Ceiling Plans – Remove furniture symbols and wall labels.
Show only ceiling and coordinated MEP elements.

**4. Building Sections**
No updated sections in the current set (folder 1350_1500_Sections/ is empty).
Submit a minimum of FOUR (4) main building sections at distinct locations.

**5. 3D Views – Entourage (Advisory)**
Use figures in traditional Saudi national dress (Thobe/Abaya) where
possible. If already produced, defer to next version.

**6. Missing & Unstamped Drawings**
Cross-check against your Drawing List and resubmit a complete, stamped set.

---

Please confirm receipt. Submit the revised set by **Thursday, 25 June 2026**.

Regards,
[Mohamed Essa]
Technical Office Manager
Samaya Factory
```

## Pitfalls

- **Don't mix must-fix and advisory in the same numbered item** — separate clearly. User corrected: "not in next subbmition some point need to revise some sheet is a must shome in next no problem"
- **Don't write paragraphs** — user corrected: "summorized not talk to meach be clear and pointed orinted"
- **Don't speculatively assert issues** — check the actual drawing package first. Empty folders are hard evidence; assumptions without checking get corrected.
- **Don't set relative deadlines** — always use a specific date. User expects concrete deadlines.
- **Don't make advisory items sound like requirements** — label them **(Advisory)** and use softer language ("where possible", "defer to next version").
- **Always pull actual drawing numbers** from the OneDrive folder listing. Don't guess what sheets exist.
