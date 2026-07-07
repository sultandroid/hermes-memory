# Subcontractor Payment & EV Analysis

## When to use

A subcontractor (designer or supply/install) has been paid against their contract but you need to:
- Verify whether payments align with the contract's payment terms
- Compute Earned Value (EV) against Actual Cost (AC)
- Identify overpayment/underpayment positions
- Cross-reference the sub's cash-flow claims against what the contract actually says
- Formulate a negotiation or dispute position

## Source documents to collect

| Document | Where to find | Purpose |
|----------|--------------|---------|
| **Signed contract** | `Contracts/02_<Party>_Contract/01_Signed_Agreements/` | Payment milestone table (Art. X), invoicing schedule terms |
| **Contract comments/markup** | Same folder, look for `*with comments*` or NRS-side markup docx | Shows disputed/negotiated clauses before signing |
| **Fee proposal / resource schedule** | `Contracts/02_<Party>_Contract/02_Proposals_and_Quotes/` | Contains the detailed payment breakdown (may differ from contract summary table) |
| **Invoices** | `Contracts/02_<Party>_Contract/04_Invoices/` or `Invoices/` | Actual amounts invoiced, dates, and descriptions |
| **Payment proof** | Invoices folder or `_attachments/` of email archive | Bank transfer confirmations, exchange rates |
| **EV snapshot / report** | `07_Reports/07.5 Audit Report/<Party>/` or `03_Analysis_Reports/` | Earned value computation vs actual payments |
| **Email archive** | `Email_Archive/_attachments/` | Correspondence about payment terms, disputes, hold reasons |

## Extraction workflow

### 1. Extract payment terms from signed contract

Use `pymupdf` (`fitz`) to extract text, then locate **Art. 11 (Terms of Payment)** or equivalent:

```python
import fitz
doc = fitz.open("/path/to/contract.pdf")
for i, page in enumerate(doc):
    text = page.get_text()
    if "Art. 11" in text or "Terms of Payment" in text or "due and payable" in text.lower():
        print(f"--- Page {i+1} ---")
        print(text)
```

**Look for the payment milestone table structure.** The table may span multiple pages. Common patterns:

| Pattern | Meaning |
|---------|---------|
| "Advance Payment (upon signing) — 10%" | Upfront mobilization payment |
| "Monthly Instalments — Per agreed invoicing schedule" | Time-based, not milestone-gated — the sub's argument |
| "Balance of X" | Remaining after advance deduction |
| "Per agreed invoicing schedule that the parties shall agree in advance" | Art. 11.2 — invoicing schedule may NOT have been formally agreed for later stages |

### 2. Compare contract terms against invoice register

Map each invoice to the contract milestone it claims:

| Contract milestone | Amount | Invoice(s) | Paid? | EV at time of payment |
|---|---|---|---|---|
| Advance (10%) | SAR 120,900 | INV-4755 | Yes | SAR 0 (advance) |
| Stage 4 1/2 (50% of balance) | SAR 345,600 | INV-4781 | Yes | ~SAR 200K |
| Stage 4 2/2 (remaining balance) | SAR 345,600 | INV-4805 | Yes | ~SAR 400K |
| Stage 5 1/3 | SAR 90,000 | INV-4825 | Hold | ~SAR 47K |

### 3. Compute EV vs AC gap

Simple EVM calculation:
```
Overpayment = Actual Cost (AC) - Earned Value (EV)
CPI = EV / AC   (below 1.0 = overpaid)
```

### 4. Identify the sub's argument and its contract basis

The sub will likely point to:
- **"Monthly Instalments"** language in the contract (if present)
- **Customer-caused delays** (Art. X — exceptions to penalty clauses)
- **"Per agreed invoicing schedule"** — claiming the schedule was implicitly agreed by past payment patterns

**Counter-arguments to check:**
- Was the Stage 5/6 invoicing schedule **formally agreed** per Art. 11.2? If not, it's still open for negotiation.
- Does the next stage's work **depend on completion** of a prior blocked stage? (e.g., Stage 5 off-site fab review requires IFC)
- Does the contract have a **penalty/deduction clause** with exceptions for customer-caused delays?

### 5. Check the contract amendment requirement

Most contracts have a **written form clause** (e.g., Art. 18):
> "Any alterations of and additions to this Contract must be made in writing to become effective."

This means any revised payment plan **must be a formal contract amendment**, not a handshake deal.

## Common negotiation structures

| Structure | Good for Samaya? | When to use |
|-----------|-----------------|-------------|
| Equal monthly instalments (sub's proposal) | **No** — decouples payment from performance | Only if EV is already tracking or ahead of AC |
| Milestone-gated tranches | **Yes** — keeps payment linked to value | Standard position when overpayment exists |
| Small monthly retainer + milestone lumps | **Compromise** — addresses sub's cash flow while protecting Samaya | When sub proves genuine cash-flow distress and remaining work is substantial |
| Hold all further invoices | **Leverage tool** — use before agreeing to any plan | When overpayment exceeds 30% and sub is not delivering |

## Output

1. **Contract vs Reality comparison table** — milestones as written vs what was actually paid vs EV
2. **Contract analysis** — what the sub's claim is based on (verbatim clause) vs what counter-argument is available
3. **Recommended negotiation position** — specific numbers, walk-away lines, what to offer

## Pitfalls

- **Scanned/Image PDFs cannot be extracted via pdftotext** — the signed contract may be a scanned image with no text layer. In that case, check for a *with comments* docx version (which often has full text even if the signed one is scanned). Use the docx version for extraction, then verify against the scanned PDF visually.
- **The "Monthly Instalments" language may be in the contract table but incomplete** — sometimes the actual invoicing amounts were never specified in the table itself, only referenced as "Per agreed invoicing schedule" to be confirmed later. This is a key ambiguity to exploit.
- **Advance payment deduction from Stage 4** — Verify how the 10% advance was allocated across stages. The contract table may show "Balance of X" after advance, where X = Stage amount - (10% prorated share of that stage).
- **Multiple contract PDF versions** — in the Contracts folder, you may find 3+ PDFs (signed by NRS only, signed by both, stamped versions, with-comments markups). Use the **fully signed & stamped** version as canonical. Use the **with-comments** version to understand what NRS pushed back on before signing.
- **The sub may be technically correct about the contract language** — "Monthly Instalments" may literally be what the contract says. Do not argue the language. Argue that (a) the invoicing schedule for the next stage was never agreed, and (b) the underlying assumption (prior stage complete) is broken, making the contract's implicit schedule inapplicable.
- **Currency conversion rates in payment proof** — NRS invoices were in EUR but contract in SAR. Check the exchange rate applied. Discrepancies could be a minor negotiation point.
- **Always document everything via a contract amendment (written form clause)** — Art. 18 or equivalent requires written agreements. Verbal agreements to revise payment plans are unenforceable.

## Example: NRS Aseer Museum Payment Analysis

See conversation session 2026-06-06 for the full analysis. Key findings:

- **Contract**: Art. 11 shows "Monthly Instalments" for all stages
- **Paid**: SAR 812,100 (67%) vs EV SAR 483K (40%) → **SAR 329K overpaid** (CPI=0.59)
- **NRS's claim**: "The contract says monthly instalments" — technically correct
- **Counter**: Stage 5 invoicing schedule never formally agreed (Art. 11.2), Stage 5 depends on IFC which is blocked by SI007
- **Recommendation**: Offer time extension + small monthly retainer (SAR 20-30K) + milestone lumps for specialist packages
