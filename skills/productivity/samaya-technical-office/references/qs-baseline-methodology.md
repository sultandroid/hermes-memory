# Quantity Surveying Baseline — 7-Register Methodology

## When to Use
Building a scope baseline and quantity register for a tender/pricing study from a design package (PDF + Excel + RFQ drafts + site reports + existing BoQ).

## The 7 Registers (mandatory order)
1. **Document Register (A)** — every input document: code, title, rev, date, format, description
2. **Discrepancy Log (B)** — cross-compare parallel docs. Every discrepancy has: severity, action, affected docs
3. **WBS Register (C)** — GROUP-ZONE-PACKAGE-SEQ. Every zone × package; mark scope Y/N
4. **Quantity Register (D)** — code, description, qty, unit, quantity-class (area|count|system), source_doc, source_ref, method (measured|scheduled|assumed)
5. **Open-Items / RFI List (E)** — every unresolved item with action, source, priority, deadline
6. **Scope-Gap & Risk Register (F)** — every risk: severity, P×I, pricing treatment, affected lines, owning RFI
7. **RFI Register (G)** — every RFI: subject, status, findings, risks, questions, next step

## Guardrails
- Never invent a quantity. If a value isn't in source documents → method=assumed, flag in Open-Items
- Never resolve a discrepancy silently → log with recommended action
- Every quantity row has a source_doc and source_ref
- Every risk has a pricing treatment and an owning RFI
- Quantities only — no rates, no prices

## Inputs to Hunt For
- Design PDFs (scenographic, detailed, interior, material/furniture schedules)
- Excel data files (material schedules, furniture schedules, AV BoQ, lighting schedules)
- BoQ (latest version, both XLSX and PDF)
- RFQ drafts with confirmed equipment quantities
- Site inspection reports
- RFI packages
- Drawing registers
- MEP/ELV gap analyses

## Cross-Comparison Checklist
- Furniture PDF vs Excel completeness
- Area-code keys across all documents (single-letter codes often conflict)
- Material code ranges (CL/FL/WL/DR/SP counts) — PDF vs Excel
- Drawing-only content that can't be quantified from text
- BoQ ballpark items vs design document detail
- BoQ line items vs RFQ confirmed quantities

## System-Package Seeding
When RFQ drafts exist with confirmed equipment quantities, seed these into the Quantity Register directly:
- AV: LED cabinets, projectors, speakers, sensors, controllers, mounts
- Furniture: chairs, tables, sofas per supplier RFQ
- Lighting: fixtures per lighting schedule

## Classification Codes
- quantity-class: area (m², LM) | count (unit) | system (LS, package)
- method: measured (from BoQ/drawings) | scheduled (from RFQ/vendor spec) | assumed (ballpark, flagged)

## Risk Rating
- P (probability): 1-Rare · 2-Unlikely · 3-Possible · 4-Probable · 5-Almost Certain
- I (impact): 1-Negligible · 2-Minor · 3-Moderate · 4-Major · 5-Critical
- Rating: P×I. 1-4 Low · 5-9 Medium · 10-20 High

## Delivery Format
- Structured markdown with all 7 parts in one file
- Companion Excel for the full Quantity Register (197+ lines impractical in markdown)
- Named: `{Project}_Quantity_Surveying_Baseline_{Date}.md`

## Pitfalls
- **Sub-agent timeout on large files:** Don't delegate the entire redesign of a 200KB+ HTML file in one sub-agent goal. Break into verify→targeted-patch cycles. After timeout, check what was done (file size growth, grep for key terms) and complete remaining work with targeted fixes.
- **Area-code disambiguation is CRITICAL:** Single-letter codes (CF, CA, FL) mean different things in different documents. Must confirm with designer before take-off.
- **Material schedule authority:** PDF and Excel often have different code ranges. Determine which is contract baseline.
- **HVAC is the #1 gap in exhibition fit-out:** Scenographic designers don't design AC. Always flag HVAC as a scope gap and add provisional sum.
- **ELV ballpark items are dangerous:** Civil Defence mandatory systems (fire alarm, PAVA, emergency lighting) often appear as ballpark estimates with no design basis. Provisional sums only — never convert to firm rates without detailed design.