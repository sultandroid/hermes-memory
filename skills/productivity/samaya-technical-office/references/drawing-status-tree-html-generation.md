# Drawing Status Tree HTML — Regeneration from Register + Filesystem Scan

## When to Use

You have an existing HTML drawing status tree file (e.g., `Aseer_Drawing_Status_Tree.html`) that compares a drawing register against actual files on disk. You need to rescan the filesystem and regenerate it with updated statuses, counters, and A4 pagination.

## Workflow

### Phase 1: Extract Register Entries from HTML

The HTML has entries in `<pre class="tree-box">` sections with this format:
```html
<span class="mk pn">[&gt;&gt;]</span> A2742-1200     Rev C      Proposed Basement Plan - General Arrangement
```

Key parsing rules:
- **HTML entity decoding:** `&gt;&gt;` = `>>`, `&amp;` = `&`. Always decode before regex matching.
- **Regex pattern:** `r'<span class="mk (ok|pn|xx)">\[(OK|>>|XX)\]</span>\s+([A-Z0-9\-]+)\s+Rev\s+([\w\-]+)\s+(.+)'`
- **Expected count:** 243 entries (Aseer DIS_022 register). Verify against section summary counters in the HTML.

### Phase 2: Scan Filesystem for Actual Files

Scan three locations:

| Location | Path | What to find | Status if found |
|----------|------|-------------|-----------------|
| Source folders | `06_Drawing_Source_Folders/` | PDF files named `A2742-XXXX*.pdf` | `>>` Pending |
| Stamped packages | `02_Approved_Stamped_Packages/` | PDFs named `*_NRS_stamped.pdf` | `OK` Stamped |
| CAD source | `06_Drawing_Source_Folders/00_Stamped_CAD_Source/` | DWG files named `A2742-XXXX*.dwg` | `>>` Pending |

**Priority for status determination:** Stamped PDF > Source PDF > DWG > Missing.

**Drawing number normalization for matching:**
```python
def normalize(dn):
    """Remove revision suffix for matching"""
    return re.sub(r'[A-Z]$', '', dn) if not dn.startswith("A2742-A-") else dn
```

Stamped file names may use revision in their name: `A2742-1700B_NRS_stamped.pdf` matches base `A2742-1700`.

### Phase 3: Edge Cases — Drawings in Archives

Some drawings exist only in `05_Correspondence_Archive/` (old revisions, incoming drafts). These should be marked as `XX` Missing from active source — do not upgrade them to `>>` just because a file exists somewhere in the archive.

Categories of archive-only files:
1. **1570-1574 External Benches** — only in `Unstamped_and_Old_Revisions/` and `Incoming_Drawings_Archive/` → stay `XX`
2. **1711 Counter** — only in correspondence, DWG not in Stamped_CAD_Source → stay `XX`
3. **1104 Existing 2nd Floor** — no file anywhere → stay `XX`

### Phase 4: Discover New Drawings Not in Register

Files may exist on disk that aren't in the register at all. Example: A2742-1575 to A2742-1578 were found as PDFs in `06_Drawing_Source_Folders/1570_External_Details/` but not in DIS_022. **Add them as new entries** with inferred titles based on their drawing number range and section context.

### Phase 5: Regenerate HTML

#### Structure
- **Sheet 1:** Title page with logo strip, meta-grid, counter tiles (OK/>>/XX/Rev Gap), and 2-column discipline summary grid
- **Sheets 2-N:** Tree pages — `<pre class="tree-box">` with section headers showing TOTAL section counts (not per-sheet subtotals)
- **Final sheet:** Legend & notes

#### Counter Consistency Rules
- Section headers on every tree sheet must show the **total** count for that section, not the count of items appearing on that sheet only
- Precompute section totals ONCE before any sheet generation
- The summary discipline grid on Sheet 1 must match the tree section headers exactly

#### Section Header Format
```html
<span class="grp">├── 1720 — Setworks Details   <span class="mk pn">[&gt;&gt;]</span>78</span>
```
Where `78` is the total count for the entire 1720 section across all sheets.

#### A4 Pagination
- ~28 entries per A4 sheet including section headers
- Each section header consumes 1 line
- Connector characters: `├──` for non-last items, `└──` for the last item on each sheet
- Entry format: `    ├── <span class="mk pn">[&gt;&gt;]</span> A2742-1720      Rev A      Title`

#### CSS & Template
- Use the Samaya A4 template: Carlito/Calibri font, 9.75pt base, 210mm × 297mm sheets, 14mm 18mm padding
- Logo paths relative to NRS package root: `../Docs/09_Registers/Key_Personnel_Register/CVs/_assets/logos/<logo>.png`
- Document code: `ASR-SAM-DWG-TREE-001`
- Status colors: OK `#0f7a2e`, >> `#a16207`, XX `#b91c1c`
- No `@page { margin }` beyond `0` — let `.sheet` padding handle spacing

### Phase 6: Version Metadata

| Field | Old value | New value |
|-------|-----------|-----------|
| Revision | Rev 01 | Rev 02 |
| Document strip | old date | current date |
| Meta-grid revision | old date | current date |
| Footer | old rev | new rev |
| Notes sheet | — | Add summary of changes: count upgraded, added, still missing |

### Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| HTML entities in `>>` | Regex misses entries | Decode `&gt;` to `>` before matching |
| Drawing number with A-prefix (`A2742-A-1100`) | Not matched by `A2742-\d+` pattern | Add separate pattern: `(A2742-A-\d+)` |
| Section counts per-sheet instead of total | Different counts for same section on different sheets | Precompute section totals across ALL entries, not per-sheet slice |
| 1570-series split across old/new revisions | Old 1570-1574 marked as found because files exist in archive | Check active source folders specifically, not entire package |
| Filesystem files not in register (1575-1578) | Missing from output | Scan all source PDFs and compare against register stems |
| `├──` vs `└──` per sheet | Last item on each sheet shows `├` instead of `└` | Track `is_last_in_sheet` per entry |
| Stamped filename with merged prefix (`A2742-1230A-1900A Merged_NRS_stamped.pdf`) | Not matched by simple `*_NRS_stamped.pdf` pattern | Add separate regex for merged pattern, extract both base numbers |
