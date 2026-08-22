# TLC Landscaping SOW Dispute — Worked Case (Aug 2026)

Aseer Museum landscape specialist contracting case. Demonstrates how a scope contradiction
between the quoted SOW and the contract, plus an un-signed internal Draft SOW, blocks the
appointment and gets chased by CG.

## Sequence of events (chronological)

| Date | Event |
|------|-------|
| 23-Jul | RFI C-05 "Find & Engage Landscaping Specialist". CG issues PQ-0127 **TLC → Code B** (approved w/ comments). PINE PQ-0126 and Evergreen PQ-0122 both rejected (Code C). |
| 03/08-Aug | Landscape & Irrigation Design Package submitted to CG (Ahmed Yehia). CG returns design comments. |
| 06-09 Aug | Samaya (Ali) requests a revised quote on a **reduced scope**. |
| 11-Aug | TLC sends **final quote Rev.2** (SAR **120,000**, design-only), Ref E: 26263-26-3304-001-Rev2, valid 15 days. |
| 12-Aug | Waris (PM) **accepts TLC's SOW** "as agreed with Samaya's technical engineers" — before contract signature. |
| 13-Aug | Kick-off meeting. Waris sends **Final Contract Agreement + SOW** to TLC for signature (50833). |
| 16-Aug | CG (Ahmed Yehia) requests from TLC: **SOW + Understanding Report + Contact Data + tech specs** — never delivered. CG chases ×5 (2 were recalls). |
| 17-Aug | TLC (Abid) replies with **comments on the draft contract** instead of signing. |
| 19-Aug | Waris: "TLC sent comments... they **disagree**." He flags to Technical Office: "confusion for **Revit model** included in scope and again they exclude from scope... **I need clear SOW duly signed by TLC and your end... Nothing received.**" |

## Root causes / lessons

1. **Internal draft SOW never approved for execution.** The only repo SOW was `21_Landscaping_Specialist_SOW_RACI_Draft.md` (14-Jul) — header stated `Status: Draft... Do not issue until Appendix A, Appendix B, package evidence, and manager review are complete.` RACI all TBC, open items open. Yet a contract bundle citing it was sent for signature 13-Aug.
2. **Contract ↔ quoted-SOW scope contradiction.** The contract listed **"Revit model updates (native format)"** in scope; TLC's own quoted SOW excluded it. The PM "accepted TLC's SOW" (which excludes) while sending a contract that includes it. Result: dispute at signature.
3. **"SOW accepted" ≠ "SOW signed."** Waris confirmed acceptance of the TLC-submitted SOW verbally, but no executed copy existed — neither TLC nor Samaya side returned a signed version. CG's requested deliverables (SOW/Understanding Report/Contact Data) never existed as clean, signed outputs.
4. **CG double-gate.** CG separately demands the specialist's SOW/Understanding Report/Contact Data after kick-off — meaning even a signed contract does not satisfy CG; the specialist must produce its own scope/understanding docs.
5. **ALWAYS verify the actual bid figure — the repo summary was WRONG and the naive "exclusion without price change" argument collapses.** The repo README/register said SAR **175,000** (that was the ORIGINAL 04-Aug offer WITH Revit in scope). The actual final **Rev.2 (11-Aug) was SAR 120,000** — TLC cut the price 55k and EXCLUDED Revit in the same revision. So Revit was removed *in exchange for* a 55k price reduction, NOT "removed without changing the price." The user's client-protective claim "they excluded Revit without dropping the price, so it should stay included" does NOT hold against the real Rev.2 offer — the client who wants Revit in scope must go back to the ~175k original offer, OR price Revit as an option on the 120k base. **Lesson: before deciding whether a bidder's exclusion is "free" or "paid," read the ACTUAL final offer PDF (extract from the email attachment), not the repo summary — price and exclusions travel together across revisions.** The actual Rev.2 PDF (`E 26263-26-3304-001-Rev2 dated 11 Aug 2026_Samaya Investment_Design_TLC_Offer.pdf`, attached to email 50632) is a scanned 3-page PDF: page 1 lists Revit IN SCOPE + "Updated Revit Model (Native Format)" in deliverables; page 2 (fee table) says "Revit/BIM authoring and updates are excluded" with fee 120,000 SAR, 20 days, 10/30/30/30 on APPROVAL; page 3 = validity 15 days + variation clause. Same document contradicts itself page-to-page (Revit in scope p1, excluded p2) — that internal contradiction is the crux, not a clean "they took it out without pay."

## Check for these before contracting a specialist

- Is the SOW signed by **both** parties (or explicitly a binding exhibit of the contract)? A "Draft" or "accepted verbally" SOW is not contractually locked.
- Does the **contract scope match the quoted/exhibit SOW line-by-line**? Cross-check every Deliverables row (esp. model updates, Revit, BOQ, review cycles, exclusions).
- Is each disputed deliverable **explicitly in OR out** — never implied? (Revit was the flashpoint here.)
- Has the specialist issued its **Understanding Report + Contact Data** (CG requirement) as a standalone deliverable, separate from the SOW/contract?

## Repo artifacts
- SOW status: `03_Scope/TLC_Landscaping/README.md` (offer/fee/payment/exclusions)
- Specialist register rows for Landscaping (PQ-0127 Code B / Evergreen C / PINE C)
- Draft SOW: `03_Plans/15_Subcontractor_Deliverables/Draft_SOW_RACI/21_Landscaping_Specialist_SOW_RACI_Draft.md`
- Contract bundle email IDs: 50833 (13-Aug, Samaya→TLC), 51254/51255 (TLC comments), 51253 (Waris→Sultan dispute summary)
