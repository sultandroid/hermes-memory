# Identifying Delayed Design Specialists — Cross-Reference Workflow

When the user asks "who is late / who is the critical path" for the Aseer design phase, do NOT answer from repo registers alone — they lag the live contract/email state and were wrong twice in one session (2026-08-18).

## Three sources, in order of authority

1. **Live vendor-domain emails** (Outlook SQLite) — the CONTRACTED specialist's own mail. This is the only source that shows a contract got signed, an invoice was sent, or a submission plan was (not) provided. Search `Message_SenderAddressList LIKE '%@<vendor>.com'` and read full bodies via AppleScript.
2. **Design Phase Deliverables Tracker xlsx** — per-discipline 50/90/IFC progress%, forecast finish dates, lead name, delay-days. This is the most current structured snapshot (user uploads it directly). Parse with openpyxl.
3. **Repo registers** (`submission_tracker.md`, `submittal_register.md`) — useful for CG codes/dates but **frequently stale on contracting status**.

## The two classic false claims (both happened 2026-08-18)

- **"Landscape — no designer appointed"** was WRONG: the tracker showed `Engr. Yahya` as Design Lead and Evergreen was PQ-0122 Code B (approved 28-Jul). The correct statement: *identified but not yet appointed; no 50% schedule or progress*. Check the lead-name column AND the prequal code before claiming "not appointed".
- **"Acoustic — PQs under CG review, can't secure resource"** was WRONG: the contract was already SIGNED (17-Aug) with TransOrient and the 50% advance invoice (SAR 86,250) sent 18-Aug. The PQs (STUMIX/ACOUSTIEG/AME/JOCAVI) were competitor candidates, not the contracted resource. Always check the vendor's OWN emails for "Signed Contract" / "Invoice" before reporting procurement status.

## Distinguish delay TYPE — it determines the remedy

- **Technical delay** (submitted but Code C/D, or slow progress): resolve in a design-coordination meeting with the discipline lead.
- **Procurement/administrative delay** (contract unsigned, no advance payment, PO not raised, designer not appointed): NOT solvable by a technical meeting — needs an admin decision (sign contract, appoint, chase CG). Flag these separately to the PM.
- **Blocked by client content** (e.g. Graphics awaiting MoC content): needs a client-side unblock, not design work.

## Quick evidence for each discipline
- CG rejection reasons: extract the response PDF via AppleScript from Hossam Mabrouk's email, `pdftotext -layout`, read the CG Comments block (often shows a numbered required-sequence checklist, e.g. core test: PQ → MS → SNA → execute → IR → report).
- Contract/invoice status: search vendor domain emails; read body for "Signed Contract" / "draft invoice / tax invoice".
- CG pending deliverables: search CG senders (`@cg.com.sa`) for "Follow-up" / "Reminder" naming the three items (SOW, Understanding Report, Contact Data etc.).
