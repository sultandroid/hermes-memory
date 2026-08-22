# Landscape bid-package readiness — worked example (TLC + second-bidder)

Case: Aseer Regional Museum, landscaping specialist package. TLC (The Landscape
Company, PQ-0127 Code B) is the incumbent; a second landscape engineer
("Nawaf") is being asked for a private comparison quote.

## The dispute that triggered the check

- TLC quoted SAR 175,000 for **design-only** landscape services (Ref E: 26263-26-3304-001 Rev.2, 11-Aug-2026). Scope listed **"Revit model updates (native format)"** as an included deliverable.
- Samaya (Waris, PM) accepted the SOW on 12-Aug-2026 ("as SOW agreed with Samaya's technical engineers") and sent the final contract for signature on 13-Aug-2026.
- TLC then returned **contract comments** (17-Aug) and effectively **withdrew Revit from scope without lowering the fee**.
- PM's own words (19-Aug): *"There is confusion for revit model included in scope and again they exclude from scope. I need clear SOW duly signed by TLC and your end."*
- CG also still needed from TLC: **SOW + Understanding Report + Contact Data + technical specs** (post kick-off, chased repeatedly, never delivered).

## What the SharePoint "supported documents 02" folder actually held

Path: `.../24_Subcontractors/03_Landscaping/`

| Present | Missing |
|---|---|
| PQ-0122 (Evergreen), PQ-0126 (PINE), PQ-0127 (TLC) PDFs | `Employer's Requirements Documents+ SOW/` → empty |
| `Revised_TLC_Landscape_Proposal.docx` (TLC's own bid) | `New Scoping Architectural Drawing/` → empty |
| `جدول الكميات للبنود التفصيلية المعدل...xlsx` (BOQ) | `existing drawing/` → empty |
| | `RVT/` → empty |
| | `Supported Documents 01/` → empty |

So a folder containing the incumbent's proposal + PQs + BOQ, but **no drawings, no ER/SOW, no Revit model**, is NOT sufficient to send a fresh bidder for a real quotation. The bidder would be pricing against the incumbent's claim, not against the project.

**OneDrive note:** the empty subfolders were likely un-hydrated files-on-demand stubs, not genuine empty dirs — and reading the two real files repeatedly hit `Resource deadlock avoided` (persistent EDEADLK; quit/relaunch of OneDrive did NOT clear it; only reboot/route-around would). Do not claim the content is "definitely absent" from a stub; verify via the web UI.

## The commercial risk being worked

"Personal-level" (off-the-books) quotation requests are an administrative/procurement tactic to pressure an incumbent — they do not go through the formal 3-qualified-specialists gate CG enforces. When the user or PM asks for this, flag that swapping the appointed specialist re-opens PQ and the "3 qualified specialists" requirement; a private price-check is fine for leverage but must not be presented as an appointed replacement without CG-aware procurement.

## Reusable takeaway

Before sending ANY subcontractor folder out for quotation:
1. Check the 5-item completeness table (ER/SOW, drawings, RVT, BOQ, PQ) — see the skill body.
2. Pin any ambiguous line-item (Revit/model updates is the recurring one on museum fit-out) explicitly in the SOW before sending, so the bidder can't quote the ambiguity to their own advantage (include fee, exclude scope, no discount).
3. Give a second bidder the SAME explicit SOW as the incumbent for an apples-to-apples comparison.
