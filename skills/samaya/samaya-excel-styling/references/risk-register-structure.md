# Risk Register Structure — Aseer Museum C11

## Sheet Order (7 sheets)

1. **Cover** — logo, title, doc ref, key metrics (hardcoded), sheet index, notes
2. **Dashboard** — severity distribution (COUNTIF from Risk Register), category distribution (COUNTIF), critical risk watchlist (hardcoded table)
3. **Scoring Matrix** — static P×S 1-4 heat map with severity band legend
4. **RBS** — 18 categories with COUNTIF formulas referencing Risk Register column C
5. **Risk Register** — 54 master risks (PRR), P×S 1-4, formula-driven PxI column, dropdowns on Response Strategy and Status
6. **Designer Risk Register (DRR)** — 79 design risks, P×S 1-5, copied from old consolidated file
7. **HSE Risk Register (Fit-Out)** — 41 task-level HSE controls, C×L 1-5, copied from old consolidated file

## Key Conventions

- **No Register Control sheet** — user removed it. Cover carries doc ref and revision.
- **Authors** always "Technical Office" — never AI model names.
- **No AI/repo/automation language** in notes or metadata.
- **Dropdowns** on Response Strategy (Avoid, Transfer, Mitigate, Accept (Active), Accept (Passive), SOW-Protect) and Status (Open, Watch, Mitigated, Closed, Superseded).
- **Dynamic counts** via COUNTIF formulas referencing the Risk Register sheet — RBS and Dashboard auto-update when risks are added.
- **Scoring Matrix is static** — methodology reference, not data-driven.
- **DRR and HSE keep their own scoring scales** (1-5) — never merged into the PRR 1-4 scale.

## Common Pitfalls

- MergedCell attribute errors when clearing cells in merged ranges — always unmerge first.
- Data validations accumulate on rebuild — clear `ws.data_validations.dataValidation` before adding new ones.
- Formula cells have no cached value when opened with `data_only=True` — use two-pass compute for styling.
