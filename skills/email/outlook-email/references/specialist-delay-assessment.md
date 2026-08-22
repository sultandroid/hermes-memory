# Identifying Delayed Design Specialists — Cross-Reference Workflow

When the user asks "who is late / who is the critical path" for the Aseer design phase, do NOT answer from repo registers alone — they lag the live contract/email state and were wrong twice in one session (2026-08-18).

## Three sources, in order of authority

1. **Live vendor-domain emails** (Outlook SQLite) — the CONTRACTED specialist's own mail. This is the only source that shows a contract got signed, an invoice was sent, or a submission plan was (not) provided. Search `Message_SenderAddressList LIKE '%@<vendor>.com'` and read full bodies via AppleScript.
2. **Design Phase Deliverables Tracker xlsx** — per-discipline 50/90/IFC progress%, forecast finish dates, lead name, delay-days. This is the most current structured snapshot (user uploads it directly). Parse with openpyxl.
3. **Repo registers** (`submission_tracker.md`, `submittal_register.md`) — useful for CG codes/dates but **frequently stale on contracting status**.

## The two classic false claims (both happened 2026-08-18)

- **"Landscape — no designer appointed"** was WRONG: the tracker showed `Engr. Yahya` as Design Lead and Evergreen was PQ-0122 Code B (approved 28-Jul). The correct statement: *identified but not yet appointed; no 50% schedule or progress*. Check the lead-name column AND the prequal code before claiming "not appointed".
- **"Acoustic — PQs under CG review, can't secure resource"** was WRONG: the contract was already SIGNED (17-Aug) with TransOrient and the 50% advance invoice (SAR 86,250) sent 18-Aug. The PQs (STUMIX/ACOUSTIEG/AME/JOCAVI) were competitor candidates, not the designated resource. Always check the vendor's OWN emails for "Signed Contract" / "Invoice" before reporting procurement status.

## Variant: writing an email to the PM listing design risks (2026-08-21)

The same rule governs drafting a risk email to the project manager. The user's stated risks can be stale because PROJECT_MEMORY.md (and the whole `Aseer-emails-md-only-2026-05-22` folder tree) lags the live contract state — most MD files there are OneDrive placeholders (`Resource deadlock avoided`); PROJECT_MEMORY.md was last updated 19-May and is NOT authoritative for contracting. Before drafting the risk list, run the live Outlook sweep below; it re-confirmed and corrected every item:

- **Acoustic → resolved**: contract signed 17-18 Aug (TransOrient), vendor invoice in process. NOT still a risk.
- **Landscape (TLC, not "TSC")** — correct specialist name is **TLC** (The Landscape Company), the user's memory "TSC" was wrong. Status: TLC approved as specialist, kick-off held 13-Aug, but final contract UNSIGNED with an open Revit-model-scope discrepancy + missing docs. This is a genuine open risk.
- **ICT/System Integrator (SPS)** — contract signed 17-Aug, after two prior CG NCRs on the scope (NC-1E0-0010, NC-1E0-0016). Closing out.
- **MEP execution contractor — the TRUE critical gap**: the MEP *design* is well advanced (HVAC 50% Gateways Pkg-01/02 submitted Aug, mechanical BOQ approved), but NO *execution contractor* appointed (offers still "under review in 08_Offers" since early June). Electrical could be re-tendered later, but the mechanical execution contractor must be secured now because the next phase (Workshop Drawings + Material/Sample submittals) needs contractor input.

Key sweep queries to run before drafting:
- `Message_NormalizedSubject LIKE '%Signed Contract%'` / `'%Contract Agreement%'` — flags contracts just signed (acoustic, ICT/SPS, AD Eng, TLC pending).
- `'%Contractor%'` / `'%Landscape%'` / `'%NCR%contracting%'` — flags open contractor appointments and CG non-conformance reports on procurement delay.
- `'%MEP%'` / `'%HVAC%'` / `'%Mechanical%'` — shows design is advancing (50% Gateways, BOQ approval) vs execution still unawarded.
- Design recovery deadline: `'%Design Progress Meeting%'` / `'%Recovery Plan%'` — consultant planner requires a Design Recovery Plan for the 30-Sep design-completion date; that is itself an email to flag.

## Distinguish delay TYPE — it determines the remedy

## Distinguish delay TYPE — it determines the remedy

- **Technical delay** (submitted but Code C/D, or slow progress): resolve in a design-coordination meeting with the discipline lead.
- **Procurement/administrative delay** (contract unsigned, no advance payment, PO not raised, designer not appointed): NOT solvable by a technical meeting — needs an admin decision (sign contract, appoint, chase CG). Flag these separately to the PM.
- **Blocked by client content** (e.g. Graphics awaiting MoC content): needs a client-side unblock, not design work.

## Quick evidence for each discipline
- CG rejection reasons: extract the response PDF via AppleScript from Hossam Mabrouk's email, `pdftotext -layout`, read the CG Comments block (often shows a numbered required-sequence checklist, e.g. core test: PQ → MS → SNA → execute → IR → report).
- Contract/invoice status: search vendor domain emails; read body for "Signed Contract" / "draft invoice / tax invoice".
- CG pending deliverables: search CG senders (`@cg.com.sa`) for "Follow-up" / "Reminder" naming the three items (SOW, Understanding Report, Contact Data etc.).
