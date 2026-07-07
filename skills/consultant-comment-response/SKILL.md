---
name: consultant-comment-response
description: Handling consultant review comments on submittals.
---

# Consultant Comment Response

## Overview
Handling consultant review comments on submittals: extracting comments from PDFs, mapping to responsible parties via RACI, drafting internal action assignment emails and external reply emails to the consultant. Covers the full workflow from PDF extraction to email composition.

## Workflow
1. **Extract comments** from the PDF using `pdftotext -layout`
2. **Read the RACI matrix** (Excel) to understand party responsibilities
3. **Map each comment** to the responsible party and determine status
4. **Draft internal email** assigning actions to each party with deadlines
5. **Draft external reply** to the consultant with a table of responses

## Extended Workflow: CG Schedule/Register Processing

When CG sends an Excel/PDF schedule (object schedule, drawing register, submission plan):

1. **Extract & map** — Use `openpyxl` for Excel, `pdftotext -layout` for PDFs. Build a clean object-to-showcase mapping table
2. **Version comparison** — Compare against the previous version. Identify new, removed, reassigned, split, and unassigned items
3. **Gap analysis** — Check which galleries/areas have complete mapping vs missing. Flag contradictory notes, missing dimensions, color coding violations
4. **Multi-party routing** — Draft ONE email with a responsibility table (NRS / Glasbau Hahn / Structural Engineer)
5. **Decide whether to query CG** — If entire galleries are missing assignments, query CG before routing. If minor TBCs, proceed and flag
6. **Handle designer pushback** — NRS will flag inconsistencies, request curator meetings, and claim additional fees. Forward to CG, support the fee claim

See `references/cg-schedule-processing.md` for the full workflow with templates and pitfalls.

## Key Files
- `templates/internal-action-email.md` — Template for internal action assignment
- `templates/external-reply-email.md` — Template for external reply to consultant
- `references/comment-extraction-technique.md` — Detailed technique for extracting and mapping comments
- `references/cg-schedule-processing.md` — Processing CG Excel/PDF schedules (object schedules, drawing registers): extraction, version comparison, gap analysis, multi-party routing, handling designer pushback

## Pitfalls
- PDFs can be very large (>100k lines); use `pdftotext -layout` and read in chunks
- Comments may have inline status markers like "OK", "OK - comply with Ad.", "OK - Update in DL" — these need careful parsing
- The RACI matrix defines who is responsible for what; always consult it before assigning actions
- Some comments are duplicates ("Same comment #N") — handle by referencing the original
- Always include a table in the external reply for clarity
- Deadlines should be realistic (typically 5-7 working days for resubmission)

## User Preferences (Mohamed Sultan Abbas)
- Formal, professional tone in both internal and external communications
- Arabic/English bilingual headers in submittal documents (preserve original formatting)
- Prefers detailed action tables with clear party assignments
- Wants "In Progress" vs "Closed" status clearly distinguished
- Expects all comments to be addressed even if just "Noted — no further action"
- Uses specific terminology: "CG" for consultant, "AD" for MEP designer, "DL" for drawing list
- Prefers deadlines to be explicit (date-specific, not relative)
- Attachments should be listed at the end of external replies
- **Single consolidated email** — when routing to multiple parties (NRS, GBH, Structural), send ONE email with a responsibility table, not separate emails per party
- **Check SOW yourself** — before asking a subcontractor if something is in their scope, check their SOW/contract first. Only ask them for timeline/dates, not scope confirmation
- **Don't debate scope in the routing email** — when forwarding CG comments, just state the comment and ask for proposed dates. Don't ask "is this in your scope?" — that's your job to determine from the contract
- **Direct action framing** — emails to subs should say "please review and suggest dates" not "please confirm if this is in your scope"
