# Meeting-Brief Verification — don't cite stale registers

When asked to brief management / synthesize current project status for a meeting
("what do I raise", "why isn't X done", "what's the status of Y"), the register file
is a STARTING POINT, not the answer. Registers routinely lag reality.

## The two verified traps

**1. Register claims can be stale / superseded by a corrected attachment.**
Example (Aseer 2026-08-30): `submittal_register.md` ZD-0116 said the concrete core
test "FAILED 59% (avg 20.7 MPa vs 35 MPa)". The actual corrected report (SE-KH-CC-26-177-0001)
showed the *design strength in the report was itself a misinterpretation* — corrected
35 MPa → 28 MPa. Re-read against 28 MPa, the average is 74% (still NOT COMPLY per
ASTM C42/ACI-318 ≥85%, and one core at 56% < 75% floor). The 59% figure was the OLD
misinterpretation. In the meeting, state 74% + the one weak core, NOT 59%.

Rule: **before citing any register's code/percentage/status in a meeting brief, pull
the latest primary source** — the most recent Outlook email on that doc ref and its
attachment. Registers are append-logs; a later "correct version / disregard previous"
email wins.

**2. Same-name submittals are NOT one document.**
A phrase like "the demolition plan" hides several separate submittals with different
owners, approval codes and restrictions. Always enumerate + disambiguate by ref:
- `ARM-GN-SD-0001` — demolition drawings, **Code B approved** (CG, 07-Jan).
- `ZD-0106` — Interior Dismantling & Demolition **for Cloud Survey** — Code B (25-Aug),
  but text says **NO demolition**; only dismantle+reinstall, 20×20 cm floor samples,
  reinstatement at contractor's cost, not a financial item. Permits breaking cladding
  to measure columns for the laser/point-cloud survey; **ZD-0032 does NOT block it**.
- `ZD-0032` — "Demolition routing plans" — Rev.01 submitted 25-Aug, **still under review**
  (NOT approved). A common mistake is claiming "we have an approved demolition plan"
  meaning this one.
- `SE-022` — this is a **Site Instruction on C&D waste-management non-compliance**, NOT
  a demolition plan, and was NOT APPROVED.
If asked "can we start the demolition/removal?", answer depends on WHICH scope: cladding
removal for laser survey = yes (ZD-0106 is sufficient); permanent column demolition = not
yet (needs a different approval, pending the still-weak core strength).

## Workflow for a defensible brief

1. Read the register (submittal / action-items / status) for the area in question.
2. For each number or code you will state, open the **latest** Outlook email on that
   doc ref; if it says "disregard previous / correct version", read the NEWEST attachment.
   Decode + read the attachment (outlook-data-extraction skill: magic-bytes base64, pdftotext).
3. Classify approval honestly — a 74% non-comply result is NOT fixed by correcting the
   report; the underlying weak core remains. Don't declare victory; state the residual risk.
4. Enumerate same-family docs explicitly so you don't over-claim approval.

## Aseer data notes (this brief)
- Core locations: Core-01 Ground C4 = 15.8 MPa (56%) ← critical; Core-02 Basement C6 = 23.1;
  Core-03 Basement C5 = 23.3. Avg 20.7 = 74%.
- CG's reply 30-Aug asked to attach the "updated columns layout" to close ZD-0116.
- Deliverables tracker (Excel, per-discipline sheets): STR weakest (BOD+loading approved,
  everything else 23-Aug → IFC pushed to 27-Sep); Elect ~11.6% with two recent groups
  submitted (Fire Alarm 17-Aug, Small/AV Power outlets 24-Aug, all still under review);
  Mech strong (~51%, mostly Code B); Life-Safety 0%; FLS/Glasbau showcases half Code C.
