# Consultant Offer Evaluation — Payment Milestones & RACI Alignment

## Workflow

When a consultant/subcontractor submits a final fee proposal for MEP/design services:

1. **Extract the offer** — OCR the PDF, extract scope items, exclusions, fee, timeline, payment milestones
2. **Compare against RACI** — map every scope item to the approved RACI matrix. Classify as:
   - ✅ Correctly assigned (matches RACI)
   - ❌ Overreaching (claims scope that belongs to another party per RACI)
   - ❌ Under-scoped (excludes items they should be R for)
3. **Annotate the PDF** — add highlight annotations + text notes on each issue directly on the original pages. Save as `[OriginalName]_Reviewed.pdf` alongside the original.
4. **Produce summary verdict** — table with: Aspect | Verdict (color-coded: red=critical, yellow=needs attention, green=acceptable)
5. **Negotiate payment milestones** — see below

## Payment Milestone Pattern for Design Contracts

Standard design contract milestones (NOT Concept/Schematic/Detail — those don't match DMP gates):

| # | Milestone | Trigger | % | Rationale |
|---|-----------|---------|---|-----------|
| 1 | Mobilisation | Upon contract award | 15% | Small down payment — just enough to mobilise |
| 2 | 50% Design | Upon 50% Design Submission accepted by CG | 30% | Tied to first real design gate |
| 3 | 90% Design | Upon 90% Design Submission accepted by CG | 30% | Tied to second design gate |
| 4 | IFC Approval | Upon 100% IFC Approval by CG | 25% | Held until final approval — gives leverage for quality |
| | **Total** | | **100%** | |

### Rules
- **Small down payment** (15% max) — design contracts should not have 30% down payments. User explicitly corrected this.
- **60% tied to design progress** — 50% + 90% gates. This aligns payment with actual work completed.
- **25% held for IFC approval** — gives the client leverage for quality and completeness.
- **Milestones reference DMP gates** (50%/90%/100% IFC), not Concept/Schematic/Detail. The project doesn't have Concept or Schematic stages — it starts at 50% design.

### Common Consultant Pushback
- Consultant proposes: Down 30% → Concept 30% → Schematic 30% → Detail 10%
- Counter: "The project follows DMP gates (50%/90%/100% IFC), not Concept/Schematic phases. Milestones must reflect actual design submissions."

## PDF Annotation Workflow

When reviewing a consultant's PDF offer:

```python
import fitz
doc = fitz.open("offer.pdf")

# Add highlight annotation
page = doc[page_index]
page.add_highlight_annot(Rect(x1, y1, x2, y2))

# Add comment note
page.add_text_annot(Rect(x, y, x+w, y+h), "Comment text", icon="Note")

# Add cover page with summary verdict table
new_page = doc.new_page(-1, width=595, height=842)
new_page.insert_htmlbox(Rect(50, 50, 545, 500), verdict_html)

doc.save("offer_Reviewed.pdf")
```

### Highlight color convention
- Red `#F8D7DA` — critical issues (role mismatch, scope overreach, incompatible timeline)
- Yellow `#FFF3CD` — needs attention (fee increase, misaligned milestones)
- Green `#D4EDDA` — acceptable (correctly aligned with RACI)

## Email Drafting Rules for Consultant Responses

- **No icons/emoji** in email drafts — user explicitly rejected this. Plain text only.
- **Concise summaries** — use short paragraph summaries per party, not detailed tables. User said "write summery for each one" after receiving a detailed table.
- **Be direct about lazy offers** — if the consultant just bumped the fee without addressing scope issues, say so. User said "her just modfy last offer ..its seam like he is lazy."
- **Payment milestones** — always propose DMP-aligned milestones. If consultant uses Concept/Schematic/Detail, flag it as misaligned.
