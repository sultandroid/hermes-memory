# Drawing Status Tree — Update Workflow

## Task: Rescan drawing register vs filesystem and update HTML status report

When the user asks to "rescan and update" the Aseer_Drawing_Status_Tree.html (or similar HTML register audit):

### 🚨 CRITICAL RULE: Preserve the Original Design

**DO NOT regenerate the HTML from scratch.** The original has specific CSS, layout, 6-sheet structure, and formatting. Use targeted `patch()` calls to update only:
- Status markers (`[XX]` → `[>>]` or `[OK]`)
- Section header counts
- Summary counters
- Revision number and date

### Workflow

1. **Extract register entries** from the HTML
   - Parse all `<span class="mk X">[STATUS]</span> DWG_NO Rev X Title` lines
   - Count per section: OK, >> (pending), XX (missing)
   - Save to JSON for cross-reference

2. **Scan filesystem** for actual files
   - `find` source folders for PDFs (`06_Drawing_Source_Folders`)
   - `find` stamped packages for approved PDFs (`02_Approved_Stamped_Packages`)
   - `find` CAD source for DWGs (`00_Stamped_CAD_Source`)
   - Match by drawing number stem (strip revision suffixes like A/B/C)

3. **Naming variants to handle**
   - `A2742-1200` vs `A2742-1200A.pdf` (revision suffix in filename)
   - `A2742-1100` vs `A2742-A-1100.pdf` (existing/demo prefix)
   - `A2742-1700` vs `A2742-1700B_NRS_stamped.pdf` (stamped naming)
   - `A2742-1233 2.pdf` (duplicate copies with space-number suffix)

4. **Determine status**
   - `[OK]` — stamped PDF found in `02_Approved_Stamped_Packages`
   - `[>>]` — PDF in source folder OR DWG in Stamped CAD Source
   - `[XX]` — no file found in any active source folder (ignore Correspondence Archive)

5. **Apply targeted patches** (NOT regeneration)
   - `patch()` for each changed entry: replace `<span class="mk xx">[XX]</span>` → `<span class="mk pn">[&gt;&gt;]</span>`
   - Update section headers: e.g. `XX:20` → (remove) when all found
   - Update summary counters: `167` → `208`, `43` → `6`
   - Bump revision: `Rev 01` → `Rev 02`
   - Update date: `01 June 2026` → `02 June 2026`
   - Add new entries (discovered on filesystem) at the correct position in the tree

### Pitfalls

- **HTML entities**: `>>` is encoded as `&gt;&gt;` in the HTML — use the encoded form in patches
- **Section headers appear TWICE**: once in the summary disc-grid and once in each tree pre-block. Use `replace_all=True` or target both
- **Counter line is a single long line**: the entire counter-row is one `<div>` — patch the specific `num` value
- **Files in Correspondence Archive don't count**: only files in `06_Drawing_Source_Folders` and `02_Approved_Stamped_Packages` are "active"
- **New drawings may exist on disk but not in register**: e.g., 1575-1578 were found as PDFs but weren't in the original register. Add them as new entries.
- **Register may use A-prefix for existing drawings**: A2742-1104 in register but file is A2742-A-1104.pdf

### Verification

After updating, verify:
- Total entry count (243 original + any new)
- OK/>>/XX counts match filesystem reality
- All section headers updated consistently
- Rev and date updated everywhere
- Open in browser: 6 sheets, proper layout, no broken HTML
