# Contract Claim Audit — NRS Mr. Jim Meeting (2026-06-06)

## Trigger

Meeting with Mr. Jim (NRS Director). He articulated 4 claims about payment and EV for the Aseer Regional Museum NRS subcontract.

## The 4 Claims

| # | Claim | Verbatim |
|---|-------|----------|
| 1 | DD = 90% of IFC package | "DD drawings can be calculated as 90% of the IFC package" |
| 2 | Pay INV-4825 in full | "I want to pay the pending invoice" (SAR 90K) |
| 3 | Equal instalments to project end | "Split the remaining payments in equal instalments" |
| 4 | Blocked/delayed not NRS's problem | "It sounds like it's not my problem if the project is blocked or delayed" |

## Contract Article Mapping

| Claim | Article | Verbatim Text | Analysis |
|-------|---------|---------------|----------|
| 1. DD=90% | Art. 4.1 | "IFC (Issued for Construction) CAD package for RIBA Stage 4" | No DD/IFC split defined in contract. 75/25 was analytical convention. **Negotiable** |
| 2. Pay INV-4825 | Art. 5 | "Review for conformity with the design documentation issued under Stage 4" | Stage 5 **depends on IFC** completion. Work cannot materially proceed. NRS has ~SAR 47K verified Stage 5 work done. |
| 2. Pay INV-4825 | Art. 11.2 | "Invoicing schedule that the parties shall agree in advance" | Stage 5 invoicing schedule never formally agreed |
| 3. Equal instalments | Art. 18 | "Alterations must be made in writing" | Any payment restructuring needs written amendment |
| 4a. Not NRS's fault | Art. 3.2 | "Designer shall not be responsible for delays caused by others" | ✅ Correct — no performance liability for Samaya-side delays |
| 4b. Payment unaffected | Art. 11 | Payment tied to services rendered (implied by context) | ❌ Not correct — contract ties payment to work, not time |
| 4c. No penalties | Art. 21.2 | "No penalty for delays caused by: Customer or Government Entity instructions" | ✅ Correct — SI007 is Samaya-side |

## Audit Verdict Per Claim

| Claim | Verdict | Supported By |
|-------|---------|-------------|
| 1. DD=90% | **Negotiable** — not in contract but not contradicted | Art. 4.1 undefined on milestone split |
| 2. Pay INV-4825 | **Partial** — pay SAR 47K (EV of actual work), HOLD SAR 43K balance | Art. 5 dependency on IFC |
| 3. Equal instalments | **Reject unconditional** — requires Art. 18 amendment with safeguards | Art. 18 written-form requirement |
| 4. Not NRS's problem | **Partially correct** — no penalties, but payment ≠ time | Art. 3.2/21.2 vs Art. 11 payment = f(services) |

## Recommended Position

| Component | Action | Rationale |
|-----------|--------|-----------|
| DD=90% | **Concede** | Contract undefined; aligns EV with physical progress (251/~279 drawings). EV +SAR 270K. IFC 10% (SAR 77K) still blocked by SI007 |
| INV-4825 | **Pay SAR 47K, HOLD SAR 43K** | SAR 47K = verified Stage 5 work (showcase + AV reviews). Balance payable on IFC approval |
| Equal instalments | **Reject unconditional** | Decouples pay from performance. If needed: cap at 4-5 months, tied to progress, with Art. 18 amendment |
| "Not my problem" | **Acknowledge limits** | "No penalties. But payment is for deliverables, not time. Let's align payments to a revised delivery schedule." |

## 3-Scenario Financial Model

| Metric | Baseline (Rev 02) | A — Full Acceptance | B — Recommended | C — Conservative |
|--------|-------------------|--------------------|-----------------|-----------------|
| Total EV | SAR 483K | SAR 753K | SAR 753K | SAR 483K |
| Paid | SAR 812K | SAR 902K | SAR 859K | SAR 812K |
| CV | -SAR 329K (CPI=0.59) | -SAR 149K (CPI=0.83) | -SAR 106K (CPI=0.88) | -SAR 329K (CPI=0.59) |
| Remaining at Risk | SAR 397K | SAR 307K | SAR 350K | SAR 397K |
| Overpayment Ratio | 1.68x EV | 1.20x EV | 1.14x EV | 1.68x EV |

**Scenario B rationale:** Concede DD=90% (cost concession, improves relationship). Partial pay INV-4825 at EV. Reject equal instalments. CPI improves 0.59→0.88. Near parity on overpayment.

## Key Contractual Constraints

| Constraint | Impact |
|------------|--------|
| Art. 5: Stage 5 needs IFC | Stage 5 payments are premature until IFC is approved |
| Art. 11.2: No agreed Stage 5 schedule | NRS cannot unilaterally determine Stage 5 invoicing |
| Art. 18: Written amendments | Any restructuring needs formal written amendment |
| Art. 6.1: Project schedule Feb-Oct 2026 | Original end was October 2026 — reference point for instalment cap |

## Response Document

The formal response was produced as:
`Aseer_NRS_EV_Snapshot_Audit_Rev03.docx`
at `Contracts/02_NRS_Contract/03_Analysis_Reports/`

Contains: 7 sections, 6 data tables, 3 financial scenarios, contract cross-references for all 4 claims, 5 numbered recommendations.

## Pitfalls Encountered

- **Contract structure confusion**: The contract (docx with tracked changes) had NRS's proposed amendments inline alongside original text. Always distinguish original article text from designer's proposed markups. The final signed version overrides comments.
- **Fee breakdown vs payment schedule mismatch**: The fee proposal's stage breakdown percentages (63.5% / 22.3% / 14.2%) don't perfectly match how invoices were actually raised (advance + 2 equal Stage 4 payments). The contract says "monthly instalments" but the actual payment pattern was different. Document both.
- **Art. 11.2 ambiguity**: "Invoicing schedule agreed in advance" — the advance and Stage 4 were agreed, but Stage 5 was never formalized. This is a strong counter-argument against NRS claiming Stage 5 is due.
- **"Monthly Instalments" ≠ carte blanche**: The contract says monthly instalments for all stages, but this doesn't override the dependency in Art. 5. Stage 5 instalments for work that can't be performed are premature regardless of the payment article.
