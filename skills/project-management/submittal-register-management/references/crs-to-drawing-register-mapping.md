# CRS-to-Drawing-Register Mapping

When CG returns a CRS (Comments Resolution Sheet) Excel file for a DD Gate package, map the review codes to the drawing register.

## Source Files

- **CRS Excel:** CG returns `.xlsx` with columns: No., Initial (reviewer), Sheet (drawing ref), Reviewer Comment, Code (B/C/D/U.R), etc.
- **Drawing Register:** NRS or contractor drawing list with official drawing numbers.

## Mapping Process

1. **Extract CRS data** — Read the CRS sheet with openpyxl. Each row has a drawing number (Sheet column) and a Code column (B/C/U.R).

2. **Build code dictionary** — Python dict keyed by drawing number:
   ```python
   crs_codes = {
       'MOC-ASE-AR-ARC-BF-DDD-1200': ('B', 'Maged Zamzam', '2026-06-30'),
   }
   ```

3. **Map to register** — For each row in the NRS drawing register, look up the code. Unmapped drawings get `—` (awaiting CG).

4. **Handle ranges** — Stairs (2550→2559), Freestanding Walls (2700→2709), etc. can be bulk-assigned with loops.

5. **Handle mixed results** — A single DD Gate package can have B, C, and U.R codes simultaneously. Record each drawing individually — do NOT summarise the whole package as a single code.

## Code Legend

| Code | Meaning | Action |
|------|---------|--------|
| B | Approved with Comments | Proceed, address comments in next stage |
| C | Revise & Resubmit | Fix and resubmit same drawing |
| U.R | Under Review | Excluded from this review cycle — will be reviewed later |
| — | Awaiting CG | Not yet reviewed |

## Common Patterns

- **General Comments** (row with Sheet="Gen") apply to all drawings in the package — record them as a separate row with no code.
- **Setwork Details** are often excluded from early DD reviews (U.R) due to Look & Feel dependency.
- **Room Elevations** frequently get Code C with comment "not up to standard" — flag these for priority resubmission.
- **Signature block** at bottom of CRS shows reviewer name, position, and date — record this separately.

## Output Format

Generate a markdown table per floor/package:

```markdown
| # | Sheet Ref | Title | Code | Reviewer | CRS Date |
|---|-----------|-------|:----:|----------|:--------:|
| 1 | MOC-ASE-AR-ARC-BF-DDD-1200 | Proposed GA Plans | **B** | Maged Zamzam | 2026-06-30 |
```

Add a summary table:

```markdown
| Floor | DD Gate | CRS Rev | CRS Date | B | C | U.R | Total | Status |
|-------|---------|:-------:|:--------:|:-:|:-:|:---:|:-----:|--------|
| Basement | 1G-0001 | 00 | 2026-06-30 | 10 | 5 | 36 | 51 | **Mixed** |
```

## Pitfalls

- CRS may use internal drawing numbers (e.g. `MOC-ASE-AR-ARC-BF-DDD-1200-00`) while the register uses the same without suffix — strip trailing `-00` or `-01` before matching.
- Some CRS rows have no drawing number (General Comments) — skip them in the code mapping but record them separately.
- The CRS "Code" column may be empty for General Comments rows — these are not "no code" but rather "applies to all".
- Always verify the CRS signature date vs the CRS header date — they may differ by several days.
