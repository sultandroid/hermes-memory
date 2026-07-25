# Multi-Register Webapp Deployment (PRR + DDR + HSE + AV per RMP)

## When this applies

The Samaya Risk Management Plan (RMP) Section 9.1 defines **four linked risk registers** with different scales and audiences:

| Register | Code | Scoring | Count (typical) | Audience |
|----------|------|---------|------------------|----------|
| Master Risk Register | PRR | P×S 1-4 | ~50 | Project team + CG/PMC |
| Design Discipline Register | DDR | P×I 1-5 | ~80 | Technical Office + designers |
| HSE Risk Register | HSE | C×L 1-5 | ~40 | HSE team + site |
| AV Risk Register | AV | P×S 1-4 | ~30 | AV lead + procurement |

**Each register is separate** with its own scoring scale, category codes, ownership, and lifecycle. They must NOT be merged into one page — the scales are incompatible (PRR max 16, DDR max 25) and the categories don't overlap.

## Pattern: separate page per register, cross-linked

Deploy each register as its own subdirectory under the parent `Risk/` folder:

```
samaya-factory.com/aseer/registers/Risk/         -> PRR (master, P x S 1-4)
samaya-factory.com/aseer/registers/Risk/DDR/     -> DDR (design,  P x I 1-5)
samaya-factory.com/aseer/registers/Risk/HSE/     -> HSE (future,  C x L 1-5)
samaya-factory.com/aseer/registers/Risk/AV/      -> AV (future,  P x S 1-4)
```

Each page shows a "Viewing: <register> · <link to other>" nav under the title so users can hop between siblings.

## Build pipeline (parallel scripts per register)

Each register gets its own build script that reads its own JSON and outputs to its own subdir. Shared template.html, shared deploy.sh.

```
06_Risk_System/webapp/
├── build_risk.py     # PRR — reads 06_Risk_System/risks.json         -> src/index.html + src/EXP-RISK-PRR-*.xlsx
├── build_ddr.py      # DDR — reads 06_Risk_System/generated/ddr_risks.json -> src/DDR/index.html + src/DDR/EXP-RISK-DDR-*.xlsx
├── build_hse.py      # HSE — reads HSE JSON -> src/HSE/index.html + src/HSE/EXP-RISK-HSE-*.xlsx
├── build_av.py       # future
├── deploy.sh         # rsyncs src/ to hostinger (per register, never cross)
├── template.html     # shared (slightly extended with "Viewing:" nav hook)
├── src/
│   ├── index.html          (PRR)
│   ├── .htaccess
│   ├── EXP-RISK-PRR-2026-NNN_RevC{REV}_ACTIVE.xlsx   (PRR snapshot, generated)
│   ├── DDR/
│   │   ├── index.html     (DDR)
│   │   └── EXP-RISK-DDR-2026-NNN_RevC{REV}_ACTIVE.xlsx
│   └── HSE/
│       ├── index.html     (HSE)
│       └── EXP-RISK-HSE-2026-NNN_RevC{REV}_ACTIVE.xlsx
```

### Excel snapshot generation is local, not OneDrive-served

**As of 2026-07-25 the PRR xlsx is generated inside `build_risk.py` from `risks.json`** by calling `build_xlsx.build(data, xlsx_path, snapshot_date, revision, total)`. The xlsx is reproducible from the JSON and no longer depends on the OneDrive master workbook path. DDR and HSE follow the same pattern.

**File naming convention** (live on hostinger since 2026-07-24):

```
EXP-RISK-{PLAN}-{YEAR}-{SEQ:03d}_RevC{REV}_ACTIVE.xlsx
```

Where `{PLAN}` is `PRR` | `DDR` | `HSE`, `{YEAR}` is the export year, `{SEQ}` is a 3-digit zero-padded export counter, `{REV}` is the master workbook revision (e.g. `C11`). Example: `EXP-RISK-PRR-2026-003_RevC11_ACTIVE.xlsx`.

**SEQ is auto-incremented** by scanning `src/` for `EXP-RISK-{PLAN}-{YEAR}-(\d{3})_*.xlsx` and taking `max+1`. Never overwrite a prior export — the old file stays in `src/` for traceability and gets rsynced alongside the new one.

**Old legacy filename** `Aseer_Museum_Risk_Register_C11_2026-07-19.xlsx` is removed by the build script (`glob('Aseer_Museum_Risk_Register_*.xlsx').unlink()`). It was the source of a 404 on the live EXCEL button after OneDrive stopped serving it.

**Build script must `chmod 0644` the generated xlsx** — OneDrive's macOS copies arrive as `0640`, and the LiteSpeed web server needs world-read.

## Schema normalisation (DDR → PRR template)

The DDR's Excel sheet uses different field names and categories than the PRR JSON. The `build_ddr.py` script normalises them so the shared `template.html` can render both. Mapping:

| DDR field (Excel/JSON) | PRR field (template) | Notes |
|------------------------|----------------------|-------|
| `id` (e.g. `PR-Q-001`) | `id` | same |
| `category` (TEC/SCH/EXT/PRO/QA/COM) | `category` | same; merge into `rbs_categories` |
| `title` | `title` + `event` | DDR has no separate event; reuse title |
| `cause` | `cause` | same |
| `consequence` | `consequence` | same |
| `probability` | `probability` | same |
| `impact` | `severity` | DDR calls it "impact"; PRR calls it "severity" |
| `score` | `score` | same |
| `rating` | `rating` | same |
| (missing) | `status` | default to `"Open"` |
| (missing) | `owner` | default to `"—"` |
| `response_strategy` | (extra) | preserved, not rendered by template |
| `response_action` | `response_action` | same |
| (missing) | `evidence`, `actions`, `history` | empty arrays |

Bands (Critical/High/Medium/Low) are computed identically: `P × S >= 16 → Critical` for PRR; `P × I >= 16 → Critical` for DDR. The template uses the JSON's `scoring.bands` to colour cells, so the build script sets the bands based on the register's scale.

## Live template hook (shared template.html)

Add a "Viewing:" line under the title that switches based on `RISK.is_ddr` / `RISK.is_hse`:

```javascript
function renderFooter(){
  // ... existing brandSub + foot ...
  const regName = RISK.is_ddr ? 'Design Discipline Register (DDR)'
                 : RISK.is_hse ? 'HSE Risk Register (Fit-Out)'
                 : 'Master Risk Register (PRR)';
  const siblings = [];
  if (!RISK.is_ddr) siblings.push({url: 'DDR/', label: 'Design (DDR)'});
  if (!RISK.is_hse) siblings.push({url: 'HSE/', label: 'HSE'});
  if (RISK.is_ddr || RISK.is_hse) siblings.push({url: '../', label: 'Master (PRR)'});
  const links = siblings.map(s => `<a href="${esc(s.url)}">${esc(s.label)}</a>`).join(' · ');
  $('#registerNav').innerHTML = `Viewing: <b>${esc(regName)}</b> · ${links}`;
}
```

The build script sets `"is_ddr": true` and/or `"is_hse": true` in each register's data payload, and the template reads both flags to pick the right name + link set. Default false (PRR) when both keys absent.

**Template must include the placeholder** in the header for the JS to fill:

```html
<h1>Aseer Regional Museum — Risk Register</h1>
<div class="dcline" id="brandSub"></div>
<div class="dcline"><span id="registerNav"></span></div>
```

Without the `registerNav` span the JS injects into nothing, and the cross-link nav never appears. Symptom: deployed page shows the title and brandSub but no "Viewing: …" line under them.

## Hostinger quirks specific to multi-register deployment

- **Subdirectory case-sensitivity trap**: Hostinger's LiteSpeed caches 404 responses for non-existent paths. A new lowercase subdir like `ddr/` may stay 404-cached even after you create the directory and put `index.html` in it. The fix: **use UPPERCASE directory names** (`DDR/`, not `ddr/`). This bypasses the stale cache because the path never existed as a 404 before. Symptoms: server-side `ls` shows the file, HTTP returns 404 with `last-modified: Tue, 22 Apr 2025` (a cached error page), and the file is on disk with correct permissions (0644, correct owner).
- **`--delete` on rsync is dangerous** when the local source uses a different case from the server-side path. rsync will delete the server's correctly-named dir and re-upload with the local case, then the 404 cache re-activates. Always run rsync with the SAME case as the deployed target. If the local source dir is `DDR/` and server has `ddr/`, fix the local to match before running rsync.
- **OneDrive xlsx for the master register can be empty** when the OneDrive client is in a bad state (stuck "files on demand"). The `deploy.sh` script must fall back to `06_Risk_System/source/C11_reference/` (the repo's staged copy) when the OneDrive path returns 0 bytes. Verify by `shasum -a 256` after copy.

## Verification sequence after deploy

```bash
# 1. Confirm server has the files (case-sensitive)
ssh -p 65002 u517606786@samaya-factory.com \
  "ls -la /home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/Risk/DDR/"

# 2. Confirm HTTP 200 on each page
curl -s -I "https://samaya-factory.com/aseer/registers/Risk/" | head -1
curl -s -I "https://samaya-factory.com/aseer/registers/Risk/DDR/" | head -1

# 3. Confirm xlsx download SHA matches
curl -s -o /tmp/xl.xlsx "https://samaya-factory.com/aseer/registers/Risk/Aseer_Museum_Risk_Register_C11_2026-07-19.xlsx"
shasum -a 256 /tmp/xl.xlsx 06_Risk_System/source/C11_reference/Aseer_Museum_Risk_Register_C11_2026-07-19.xlsx

# 4. Confirm both pages contain the right risk count
curl -s "https://samaya-factory.com/aseer/registers/Risk/" | grep -oE '"id":"PRR-[A-Z]+-[0-9]+"' | sort -u | wc -l
curl -s "https://samaya-factory.com/aseer/registers/Risk/DDR/" | grep -oE '"id":"[A-Z][A-Z0-9-]+"' | sort -u | wc -l
```

Expected: PRR = 52 unique IDs, DDR = 79 unique IDs (all matching DDR prefixes: PR-Q-, DB-*, RE-*, ST-*, CO-*, TE-*, BI-*, DDR-*, QA-*, EX-*, COM-*).

## Pitfalls (multi-register specific)

- **Don't merge DDR into the PRR JSON** even if the user asks. The P×S 1-4 matrix cannot honestly show DDR risks whose P×I score can be 25. Merging breaks the RMP. Always split into separate pages.
- **Don't try to fit DDR into the 4×4 P×S matrix**. The template's matrix is hard-coded P4..P1, S1..S4. Risks with P=5 or S=5 won't render in the matrix but will still appear in the table. Don't try to "fix" the matrix for the DDR page — accept that the matrix is incomplete for DDR and rely on the table + filters.
- **DDR has no `status` field** in the source JSON. Defaulting to "Open" is the honest answer (DDR risks are by definition active work-in-progress items). Don't fabricate other statuses.
- **DDR categories (TEC/SCH/EXT/PRO/QA/COM) overlap with PRR categories** (SCH/COM/etc.) but mean different things. The dropdown filter must show both sets separately, not deduplicate. Use the DDR's own RBS map in the build script.
- **`rsync --delete` will wipe sibling sub-registers.** When deploying the master PRR via `rsync -avz --delete ./src/ server:.../Risk/`, the destination's `DDR/` and `HSE/` subfolders (deployed by their own pipelines) are NOT in the local `src/` and will be deleted. Always use `--exclude='DDR/' --exclude='HSE/'` on every master deploy. Same protection in reverse for the DDR/HSE deploys. Verify the exclusion before rsync: `rsync -avz --delete --dry-run --exclude='DDR/' --exclude='HSE/' ./src/ server:.../Risk/ | grep -E 'deleting|^\*deleting' | head` should show no `deleting DDR/` or `deleting HSE/` lines.
- **Don't reuse the legacy `Aseer_Museum_Risk_Register_C11_2026-07-19.xlsx` filename.** The build script now generates `EXP-RISK-PRR-{YEAR}-{SEQ:03d}_RevC{REV}_ACTIVE.xlsx` and drops the legacy file from `src/` to prevent the 404 the old name caused. If you see a deployed `Aseer_Museum_Risk_Register_*.xlsx`, it predates the fix and the EXCEL button on that page will 404.
- **OneDrive is not authoritative for the served xlsx.** The `MASTER` path in the old `deploy.sh` (`OneDrive-SAMAYAINVESTMENT/.../23_Project_Risk_Register/...`) was unreliable (OneDrive "files on demand" returned 0 bytes when the client was in a bad state). The new pipeline regenerates the xlsx from `risks.json` inside `build_risk.py`. If you find the old `MASTER=` line still in `deploy.sh`, the script is stale — the OneDrive step is no longer needed.
- **The PRR xlsx is no longer the same as the DDR xlsx.** The old reference used a single OneDrive master workbook that contained both PRR and DDR sheets. The new pipeline generates one xlsx per register from its own JSON, with that register's rows only. Don't expect to find a "Designer Risk Register (DRR)" sheet inside the PRR xlsx.
