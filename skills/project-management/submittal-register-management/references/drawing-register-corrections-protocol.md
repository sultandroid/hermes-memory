# Drawing Register Corrections Protocol

When a register audit finds issues (duplicate numbers, wrong discipline codes, RACI gaps, naming errors, total mismatches), follow this protocol.

## Correction Workflow

1. **Apply corrections directly** to the markdown register (append-only — never delete rows).
2. **Update the numbering convention** (§1) if the audit reveals gaps (e.g. duplicate discipline codes like `L` for both Lighting and Landscape, missing phase codes like Government/Authority).
3. **Add a §N Correction Log** at the end of the register documenting every change: issue number, location, correction, rationale.
4. **Update frontmatter** (`last_updated`, add `⚠️ CORRECTIONS applied YYYY-MM-DD: See §N for correction log` pointer in the header block).
5. **Fix derived totals** (dashboard counts, summary tables by discipline/phase) to match corrected counts.
6. **Commit with descriptive message** listing all fixes.

## Common Issues Found in Audits

| Issue | Example | Fix |
|-------|---------|-----|
| Duplicate drawing number | `S-D-D-001` used for both Stramp and Structural Details | Renumber one: `S-D-D-007` |
| Wrong discipline code | `P-D-P-001` titled "MEP Design" but `P` = Plumbing | Change to `M-D-P-001` |
| Duplicate discipline code | `L` = Lighting AND Landscape | Add new code `LS` for Landscape |
| Ambiguous phase code | `A` = AFC AND Authority | Add `G` for Government/Authority |
| Wrong project name | "Aseer Museum of Art" vs "Aseer Regional Museum" | Fix header |
| RACI gap | `I: —` for Graphics | Fill with `I: MoC` |
| Total mismatch | 235 vs 206 | Document the gap: 206 = discipline count (excludes cross-cutting), 235 = phase count (all inclusive) |
| Duplicate after rename | `M-D-P-001` used for both MEP Design and HVAC Upgrade | Renumber HVAC: `M-D-P-003` |

## Correction Log Format

```markdown
## 16. Correction Log (YYYY-MM-DD)

| # | Issue | Location | Correction | Rationale |
|---|-------|----------|------------|-----------|
| 1 | Duplicate `S-D-D-001` | §5 (Stramp) + §6 (Structural Details) | §6 → `S-D-D-007` | Stramp kept original; Structural Details renumbered |
```

The correction log is append-only — new corrections add rows; old rows are never removed.

## Verification

After all corrections, grep for the old values to confirm no stale references remain:

```bash
grep -n 'OLD-VALUE' path/to/register.md
```

Also verify no new duplicates were introduced by the renumbering.
