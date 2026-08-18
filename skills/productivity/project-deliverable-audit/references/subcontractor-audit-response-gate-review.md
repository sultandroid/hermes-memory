# Subcontractor Audit-Response Gate Review (Pre-CG-Submission)

## Pattern

A specialist/subcontractor (e.g. Rawasin, the AV/IT/interactives sub) responds to
CG audit comments on a DD/design package (e.g. "AV Package Part II Rev.001") with an
`Audit Response.xlsx` (multiple sheets, one per submittal round). Before sending that
package to CG, the contractor (Samaya Technical Office) must gate-review the responses
to confirm they actually RESOLVE the CG comments — not defer or hand-wave them.

**This is distinct from writing the response.** It is the QC pass that decides
"submission-ready" vs "return to sub first."

## The blocker taxonomy (reusable categories)

When reviewing each CG comment's response, classify it:

| Category | Response tells | Gate action |
|----------|---------------|-------------|
| ✅ Answered | Concrete doc uploaded / device named | OK |
| 🟡 Terse/partial | Answer given but thin, asks CG to "specify what's needed" | Ask sub to complete |
| 🔴 Deferred | "Rawasin Engineer needs to provide this" | **Not gate-passable** — return to sub |
| 🔴 Missing | "I didn't work on commissioning" / "this is new work we didn't work on" | **Not gate-passable** — required deliverable |
| 🔴 Scope gap | "Not included in our scope per BOQ" but ER requires it | Settle interface / VO with CG |
| 🟡 Deviation | "We recommend iPad + local panels" vs BOQ has 1 touch panel | Formal compliance statement + approval |
| 🟡 Vague accountability | "'Our team' will program DALI/DMX" — who exactly? | Name the responsible party |

## Gate rule

**A gate submittal cannot go to CG while it carries deferred ("X Engineer needs to
provide"), missing ("didn't work on it"), or scope-gap (admitted non-compliance) items.**
Deferred work pushed onto "the engineer" is not a response. Each blocker must be:
resolved by the sub, formally scoped via interface clarification/VO with CG, or the
deviation formally approved.

## Produce: "Items to [Sub]" action matrix

Group blockers into clean sections so the sub knows exactly what to fix:

1. **Scope gaps** — must be settled with CG / interface owners (never submit with
   known non-compliance).
2. **Missing deliverables** — commissioning approach, labelling scheme, etc.
3. **Deferred items** — "Engineer needs to provide" list.
4. **Deviations** — needing formal approval (e.g. iPad/local panels vs single touch
   panel in BOQ).
5. **Unclear accountability** — name the party (e.g. DALI/DMX integration).

Then a "Good responses (no further action)" section — acknowledge what is already
correct (e.g. committed control processor model + network switch), so the sub isn't
pestered to redo completed work.

## Source of truth: read the actual response file

Do not trust the review matrix alone — open the raw `Audit Response.xlsx`
(`openpyxl`, `data_only=True`) and read every response verbatim. The matrix is derived;
the sub's exact wording ("I didn't work on the commissioning documents please let me
know if I need to work on it") is what tells you whether an item is deferred vs missing
vs a genuine scope claim. Worked example: AV Package Part II Rev.001 produced a 5-section
"Items to Rawasin" matrix and a "NOT submission-ready" verdict.

## Output location (Aseer repo)

Place the action matrix beside the review matrix in
`aseer-museum-pm/04_Docs/02_Plans_and_Procedures/02.1_DMP/02_CG_Responses/`
e.g. `AV_Package_PartII_Items_To_Rawasin.md` alongside
`AV_Package_PartII_Audit_Response_Review.md`. Commit to git.
