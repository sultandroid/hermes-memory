# CRS-to-Drawing-Register Reconciliation

When CG returns a CRS (Comments Resolution Sheet) Excel for a DD Gate submittal, extract per-drawing review codes and update the drawing register.

## Workflow

### 1. Read the CRS Excel

```python
import openpyxl
wb = openpyxl.load_workbook('CRS_FILE.xlsx', data_only=True)
ws = wb['CRS']  # Sheet name is typically 'CRS'
```

### 2. Extract Key Metadata

From the header rows (rows 1-10 typically):

| Field | Where to find |
|-------|---------------|
| CRS Number | `MOC-MUS-ASE-1A0-1G-0001` (row with "CRS NUMBER") |
| Document Title | Row with "DOCUMENT TITLE" |
| CRS Rev | Row with "Rev." near CRS NUMBER |
| CRS Date | Row with "DATE" near CRS NUMBER |
| Floor | Infer from drawing number prefix (BF=Basement, LGF=Lower Ground, GF=Ground Floor) |

### 3. Extract Per-Drawing Codes

Each data row has columns (positions vary — scan headers):

| Column | Content |
|--------|---------|
| No. | Comment number |
| Initial | Reviewer name (e.g. "Eng. Maged Zamzam") |
| Sheet | Drawing sheet reference (e.g. `MOC-ASE-AR-ARC-BF-DDD-1200-00`) |
| Reviewer Comment | The CG comment text |
| Code | Review code: **B** (Approved w/Comments), **C** (Revise & Resubmit), **U.R** (Under Review), blank for General Comments |

**Key patterns:**
- **General Comments** (sheet = "Gen") have no code — they apply to the whole submittal
- **Section headers** (e.g. "1200 - Proposed GA Plans") are category rows, not drawings
- **U.R** = Under Review — CG explicitly excluded these from the review cycle
- **Blank code** = not yet reviewed or general comment

### 4. Map to Drawing Register

The CRS uses NRS drawing numbers (`MOC-ASE-AR-ARC-BF-DDD-1200-00`). The repo's drawing register uses abbreviated codes (`A-D-P-001`). These are **different numbering systems** — do not try to merge them into one table.

Instead, build a **separate DD Gate Review Status section** in the drawing register:

```markdown
## 15. DD Gate Review Status — Architecture

> **Source:** CRS files from CG
> **Legend:** B = Approved with Comments · C = Revise & Resubmit · U.R = Under Review

### 15.1 Basement Floor — 1G-0001 (CRS Rev.00, 2026-06-30)

| # | Sheet Ref | Title | Code | Reviewer | CRS Date |
|---|-----------|-------|:----:|----------|:--------:|
| 1 | Gen | General Comments | — | Maged/Abdrabo | 2026-06-30 |
| 2 | MOC-ASE-AR-ARC-BF-DDD-1100-00 | Existing GA Plans | **B** | Maged Zamzam | 2026-06-30 |
| 3 | MOC-ASE-AR-ARC-BF-DDD-1150-00 | Demolition GA Plans | **B** | Abdrabo Shahin | 2026-06-30 |
```

### 5. Summary Table

Add a floor-by-floor summary:

| Floor | DD Gate | CRS Rev | CRS Date | B | C | U.R | Total | Status |
|-------|---------|:-------:|:--------:|:-:|:-:|:---:|:-----:|--------|
| Basement | 1G-0001 | 00 | 2026-06-30 | 10 | 5 | 36 | 51 | Mixed |
| Lower Ground | 1G-0002 | 00 | 2026-07-02 | 6 | 10 | 0 | 16 | Mixed |

### 6. Update decisions_log.md

The `decisions_log.md` may record the submittal as a single code (e.g. "Code C"). If the CRS shows mixed statuses, **correct the log** — the overall verdict may be misleading.

### Pitfalls

- **CRS covers one floor only** — check drawing number prefixes (BF, LGF, GF, 1F). Do not assume multi-floor coverage.
- **"C overall but mostly B"** — CG may stamp C overall while approving most individual drawings as B. The C is driven by a small number of items. Do not treat the overall C as blanket rejection.
- **Setwork Details often excluded** — CG may defer setwork/joinery details to a later review cycle (U.R). Track separately.
- **Room Elevations may get harsh C ratings** — CG sometimes rates elevations as "not up to standard" (missing dimensions, annotations). These need designer rework.
- **NRS vs repo numbering** — CRS uses `MOC-ASE-AR-ARC-...` format. The repo uses `A-D-P-001`. Keep separate tables — do not try to cross-reference.
- **CRS Excel may have 1000+ rows** — most are empty. Only rows with a drawing number or comment text are actionable.

## NRS Drawing Register Integration

When the designer (NRS) provides their own drawing register Excel (288+ architectural drawings with NRS numbering), **do not merge it into the abbreviated DMP register**. Instead:

### 1. Create a Separate File

`01_Registers/arch_drawing_register.md` — dedicated to NRS-numbered architectural drawings only.

### 2. Columns

| # | Drawing No. | Title | Rev | 1st Sub | 2nd Sub | 3rd Sub | CG Code | Reviewer | CRS Date |

The CG Code/Reviewer/CRS Date columns are populated from the CRS extraction above.

### 3. Cross-Reference in DMP Register

Update the DMP register's frontmatter to point to the NRS file:
```yaml
source: ...; Architecture DD status at `arch_drawing_register.md`
```

### 4. Summary Table

Add a floor-by-DD-gate summary at the bottom:

| Floor | DD Gate | CRS Rev | CRS Date | B | C | U.R | — | Total | Status |
|-------|---------|:-------:|:--------:|:-:|:-:|:---:|:--:|:-----:|--------|
| Basement | 1G-0001 | 00 | 2026-06-30 | 10 | 5 | 36 | 0 | 51 | Mixed |
| Lower Ground | 1G-0002 | 00 | 2026-07-02 | 6 | 10 | 0 | 0 | 16 | Mixed |
| Ground Floor | 1G-0005/1G-0006 | — | 2026-07-18 | — | — | — | ~80 | ~80 | Awaiting CG |

### 5. Code Mapping from CRS

Build a Python dict mapping NRS drawing numbers to (code, reviewer, date) tuples. Use the CRS sheet ref column as the key. For drawings not in the CRS, default to `('—', '—', '—')`.

## Drawing Register Audit & Correction Workflow

When reviewing a planning register (DMP-derived, 235+ drawings) against actual data, follow this protocol:

### 1. Check for These Common Issues

| Issue | How to detect | Example |
|-------|---------------|---------|
| **Duplicate numbers** | Same drawing number used for different drawings in different sections | `S-D-D-001` = Stramp (§5) AND Structural Details (§6) |
| **Wrong discipline code** | Code doesn't match the discipline convention | `P-D-P-001` = MEP (should be M, not P=Plumbing) |
| **Duplicate discipline codes** | Same letter used for two different disciplines | `L` = Lighting AND Landscape |
| **Ambiguous phase codes** | Same phase letter used for different meanings | `A` = AFC AND Authority |
| **Wrong project name** | Header doesn't match contract | "Aseer Museum of Art" vs "Aseer Regional Museum" |
| **RACI gaps** | `I: —` with no informed party | Graphics drawings missing MoC |
| **Totals mismatch** | Summary sections disagree | §15.1 says 206, §15.2 says 235 |
| **Duplicate after correction** | Renumbering creates new collisions | `M-D-P-001` used in §6 AND §9 |

### 2. Correction Protocol

1. **Fix the data** — renumber duplicates, fix codes, fill gaps
2. **Document every change** in a §16 Correction Log with:
   - #, Issue, Location, Correction, Rationale
3. **Update frontmatter** — `last_updated`, add `⚠️ CORRECTIONS` banner
4. **Verify no new duplicates** — grep for the new numbers across the whole file
5. **Add new corrections** if the fix created new collisions

### 3. Correction Log Format

```markdown
## 16. Correction Log (YYYY-MM-DD)

| # | Issue | Location | Correction | Rationale |
|---|-------|----------|------------|-----------|
| 1 | Duplicate `S-D-D-001` | §5 (Stramp) + §6 (Structural Details) | §6 → `S-D-D-007` | Stramp kept original; Structural Details renumbered |
| 2 | Duplicate `S-D-D-002` | §5 (Sunshade) + §7 (Structural Details 90%) | §7 → `S-D-D-008` | Sunshade kept original; 90% Structural Details renumbered |
```

### 4. Common Fixes

| Problem | Fix |
|---------|-----|
| Duplicate drawing number | Keep the first occurrence (by section order), renumber the second to next available in sequence |
| Wrong discipline code | Change to correct code per convention (P→M for MEP, L→LS for Landscape) |
| Ambiguous phase | Add new phase code to convention (G for Government/Authority), update affected sections |
| RACI gap | Fill `I: —` with the correct informed party (typically MoC) |
| Totals mismatch | Document the gap — both counts may be valid for different dimensions |
