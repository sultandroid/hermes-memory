# Evidence-First Contractor / Vendor Correspondence Triage

**User rule (2026-08-23): "اهم حاجه ردودك تكون بادله" — answers must be evidence-based, backed by actual sources (repo registers / Outlook / approved design), never inferred or asserted from memory.**

When a contractor/vendor raises an info-request list or a "concern", resist the reflex to label items "obstruction / delay tactic / trying to cut cost" from the question alone. Several questions that *look* like negotiation plays are actually legitimate and have answers already sitting in the repo. Asserting otherwise, or inventing a design constraint, produces a wrong reply and destroys trust.

## Worked example (Aseer, 2026-08-23) — MEP contractor info request

Contractor asked: "Cable trunking vs screed <15cm, use PVC conduits? / Only AV drawings received / NAMA fire-alarm comments affect whole FA design."

- **Cable trunking vs PVC** → jumped to "do NOT let installer substitute PVC" without checking. The repo shows PVC is **already approved**: `MOC-Asser-SIC-1E0-MS-0005` (Embedded PVC Conduits & Fittings) Code B, and PQ-0086/0087 (PVC Conduits — KHERIJI/BAHRA) Code B. The honest answer: it's a legitimate execution query in specific zones → route to AD Engineering to define where trunking vs PVC applies. Not a blanket "PVC forbidden".
- **"Only AV drawings received"** → the old repo files said "ICT not appointed" (`specialist_sign_offs.md` still shows SBS "in agreement"). But **Outlook shows SPS returned the signed & stamped ICT contract on 2026-08-18 (email 51183)**, after Waris sent it 17-Aug (51108). So ICT/ELV designer **was appointed as of 18-Aug** — the contractor's "not appointed" excuse expired. The real remaining gap is **BMS design (Jadco)**.
- **NAMA fire comments** → legitimate, already tracked (9 comments, reply 11-Aug; FA ZD-0067 Rev.03 Code B 06-Aug). Not obstruction.

## Pitfalls.

1. **Check the register for the exact subject before asserting a design constraint.** A design element the contractor questions may already be approved (in `method_statement_register.md`, `prequalification_register.md`, `submittal_register.md`). Grep the repo first.
2. **Recheck specialist appointment status live in Outlook, not in a stale repo summary.** Multiple files in `Technical_Office/Specialist_Management/` can lag reality (they still said "SBS / in agreement"). The signed-contract email (sender → recipient, date) is authoritative for "appointed" claims. If the vendor's own reply email carries the signed/ stamped agreement, that settles it.
3. **Distinguish "obstruction" from "legitimate question whose answer exists".** Blocking questions usually (a) ask you to decide something already decided, or (b) use a *now-outdated* gap as a reason to suspend all work. Legitimate ones (a) reference an approved document, or (b) surface a genuine still-open gap (e.g. BMS design).
4. **Separate the workable scope from the flagged gap.** When a vendor cites a missing input (ICT/AV), don't let that halt unrelated trades — state that the available scope (mechanical/electrical/plumbing) is not held hostage by the gap, and document the gap as an external delay for the EOT file.
5. **When the user says "نرجع بالدليل" / "ردودك بادله" (evidence-based), that is a hard instruction** to back every claim with a repo path, register row, doc ref, or Outlook message ID before answering. Lead with what the evidence shows, not with a narrative read of the contractor's intent.
