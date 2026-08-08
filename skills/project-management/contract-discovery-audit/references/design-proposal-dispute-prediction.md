# Predicting Disputes in a New Design-Services Proposal

When a new specialist/consultant submits a **design-services proposal** (e.g. a landscape design fee), predict the likely disputes BEFORE signing by mining the project's existing consultant contracts, SOW conflict matrix, and lessons-learned register. This turns "review the proposal" into "pre-negotiate the known flashpoints."

## Sources to mine (in order)

1. **Existing consultant contracts** — ZNA (lighting), NRS (design), AD Engineering (MEP). Look for their fee/payment/revision/liability clauses. These are the closest analogues to a new design-services appointment.
2. **SOW_RACI_Conflict_Matrix** — open interface conflicts (SRC-00x) that touch the new discipline. E.g. SRC-005 (Stramp/Terrace boundary between Structural and Landscaping) directly predicts a boundary dispute for a landscape design contract.
3. **Lessons-learned register** — recurring failure patterns (e.g. "PQ submitted without scope definition → Code C", "resubmission without CRS reply").
4. **Invoice log** — which consultants' invoices are overdue/disputed (NRS INV-4863/4883) reveals payment-milestone friction.

## The 6 recurring dispute flashpoints in design-services contracts

| # | Flashpoint | Where it shows up | Pre-negotiation fix |
|---|-----------|-------------------|---------------------|
| 1 | **Payment tied to "submission" vs "approval"** | ZNA G4 (blank payment schedule); NRS overdue invoices | Tie each milestone to CG approval (Code A/B), not delivery. State "submission" vs "approval" in writing. |
| 2 | **Excess review cycles** | ZNA Terms (a): additional fees for post-stage revisions; TLC excludes ">2 review cycles per stage" | Fix the included review-cycle count + the per-cycle price. CG rejects frequently (Code C/D), so cycle 3+ is near-certain. |
| 3 | **Discipline boundary** | SOW_RACI_Conflict_Matrix SRC-005 (Stramp structural vs landscaping) | Close the relevant SRC before signing. E.g. landscape design excludes structural — who owns Stramp strengthening? |
| 4 | **Consultant disclaims delay responsibility** | ZNA Terms (b): "cannot accept responsibility for delays due to lack of written approval" | Set a realistic programme + who bears approval-waiting delay. |
| 5 | **Advance payment recoverability** | NRS invoices; 40% at PO/LOA | If a large advance is paid, define clawback/guarantee if design fails or CG rejects. |
| 6 | **Undefined scope / BOQ ownership** | Lessons #6, #18 (PQ without scope; HUSHA overlap with TransOrient) | State who prepares the construction BOQ/cost estimate — the design consultant often excludes it. |

## Output format

Deliver a table: `# | Predicted dispute | Root cause | Preventive fix`. Then a short "top 3 to lock in writing" list. This is what the user wants — actionable pre-negotiation points, not a generic contract review.

## Pitfalls

- **Design-services fee ≠ construction price.** A proposal for "landscape design SAR 175k" is NOT a construction quotation. Always separate "design fee" from "no priced construction BOQ exists yet."
- **Check exclusions explicitly** — design proposals routinely exclude BOQ prep, cost estimation, construction supervision, shop drawings, as-built, lighting, structural, surveys. Each exclusion is a potential scope gap to assign to someone.
- **Interior vs exterior scope** — a landscape proposal may cover only exterior; interior planters may be unpriced and outside the base contract (optional enhancement item). Verify against the BOQ/contract before claiming coverage.
- **Don't fabricate contract clauses** — quote the actual clause text (e.g. "Clause 18.00 — optional/non-binding") from the extracted source, never invent it.
