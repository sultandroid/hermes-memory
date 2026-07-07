# Market Audit Workflow — Exhibition / Fit-Out BoQ Pricing

## Pattern: Parallel Market Rate Verification

After documenting the BoQ, run a parallel market audit to verify every unit rate.

### When to Run
- After creating the full documentation set (01-09)
- Before submitting a tender price
- When the BoQ is >6 months old and market rates may have shifted

### Setup

Create a structured item list for each category. Extract from the BoQ:
- Item description
- Unit of measure
- BoQ unit rate (in original currency)
- Quantity
- Brand / model (if specified)
- Application context (museum-grade, commercial, luxury)

### Parallel Execution (3 Concurrent)

Launch 3 sub-agents simultaneously, each with `toolsets=["web"]`:

```
Task A: AV Equipment
- Projectors (Epson PQ2008B, PU1007B, PU1006B) + lenses
- Audio (QSC ceiling speakers + subwoofers)
- LED walls (LOPU, Muxwave — transparent, floor, fine-pitch)
- Sensors & controllers (Nexmosphere, Iiyama, Binepad)
- AV control (Visual Production: CueCore, Kiosc Touch, B Station)
- Installation (% of equipment — is 37% reasonable for museum AV?)

Task B: Lighting Fixtures
- DGA downlights (Ariel AF, Ariel MR, Tono Super AM)
- DGA linear fixtures (Armonia Opal Cover, Armonia 8x14, Armonia Wall Washer)
- FLOS decorative pendants (Seki Han)
- Showcase spots (LUXAM L-MTSP 02)
- Drivers & control (LTECH, Eldoled, Enttec, Visual Production)
- Lighting installation (% of equipment — verify against market)

Task C: Furniture + Construction Fit-Out
- Italian furniture: Calligaris, B&B Italia, Poltrona Frau, Molteni&C, LAGO, etc.
- European: Draenert (DE), NORR11 (DK), BK CONTRACT (ES), Laskasas (PT)
- Import mark-up structure (list → FOB → CIF → installed in KSA)
- Fit-out: stone cladding, marble, carpet, drywall, paint, ceiling
- Riyadh 2025-2026 market rates for museum-grade fit-out
```

### What Each Sub-Agent Reports

```
For each item:
| Item | BoQ Rate | Market Range | Verdict | Variance |
|------|----------|--------------|---------|----------|
| Epson PQ2008B | $20,334 | $19k-$21k | FAIR | 0-5% |
| Armonia linear | $264/m | $220-$260/m | FAIR | 0-5% |
| ...            | ...      | ...          | ...     | ...     |
```

Verdict should be one of: **Fair** (0-10%), **Slightly Over** (10-20%), **Overpriced** (20%+), **Underpriced** (< 0%), **Cannot Assess** (no market data).

### Compilation Report

After all 3 sub-agents return, compile into `11_MARKET_AUDIT_REPORT.md` with:

1. **Category summaries** — total over/under per category
2. **Biggest flags** — top 5 items with highest variance
3. **Installation margins** — are the %-of-equipment rates reasonable?
4. **Currency checks** — EUR/USD, USD/SAR conversion rate consistency
5. **Priority action items** — which rates need supplier quotes vs can be taken at face value
6. **Overall verdict** — short paragraph per category

### Known Market Ranges (Riyadh 2025-2026, Museum-Grade)

| Category | Typical Range | Notes |
|----------|--------------|-------|
| Italian furniture import markup | 1.5-3.0x European retail (installed KSA) | Higher for B&B, Poltrona Frau; lower for Calligaris |
| AV installation | 25-40% of equipment | 30-32% typical; 37% at high end |
| Lighting installation (DMX) | 35-45% of equipment | Includes programming, commissioning |
| Drywall partitions | $70-95/sqm sound-rated | $115/sqm is high |
| Airport carpet + levelling | $150-200/sqm | $280/sqm is high |
| Marble floor (premium Italian) | $350-500/sqm | $520/sqm is high-end |
| Paint (multi-coat museum) | $18-25/sqm | $30/sqm is high |
| Riyadh yellow stone cladding | $120-180/sqm | $200/sqm acceptable for premium |
| Custom metal panels (bronze) | $3,000-5,500/unit | Complex designs can hit $7,000+ |

### EUR/USD Rate Handling

European suppliers (DGA, FLOS, Epson) often quote in EUR. The BoQ may have:
- Lighting: EUR with a specific conversion date rate (e.g., 1 EUR = 1.1585 USD)
- AV consultant: EUR at their own rate (e.g., 1 EUR = 1.18 USD)
- Main BoQ summary: USD at 3.75 SAR peg

**Check:** Do the EUR→USD→SAR conversions reconcile? If not, flag for the procurement team.

### Common Pitfalls

- **Sub-agent content filters:** Web research sub-agents may fail with "inappropriate content" errors when searching for prices. This is unpredictable. Retry failed tasks individually.
- **Sub-agent hallucinated prices:** Sub-agents may return prices from training data rather than current market. The auditors' knowledge cutoff varies. Cross-reference against known ranges.
- **Sub-agent doesn't actually search web:** If a sub-agent returns a plan without executing web_search, the result is from training data, not current market. Verify that the sub-agent actually called web_search/terminal tools during its run.
- **AV installation bundling:** The AV installation line may be bundled with control equipment (AV Control & Installation). Disentangle the pure installation cost and the control system hardware before comparing installation %.