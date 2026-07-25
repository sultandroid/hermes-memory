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
├── build_risk.py     # PRR — reads 06_Risk_System/risks.json         -> src/index.html
├── build_ddr.py      # DDR — reads 06_Risk_System/generated/drr_risks.json -> src/DDR/index.html
├── build_hse.py      # future
├── build_av.py       # future
├── deploy.sh         # runs all build_* then rsyncs src/ to hostinger
├── template.html     # shared (slightly extended with "Viewing:" nav hook)
├── src/
│   ├── index.html          (PRR)
│   ├── .htaccess
│   ├── Aseer_Museum_Risk_Register_C11_2026-07-19.xlsx   (master download, same for all)
│   └── DDR/
│       └── index.html     (DDR)
```

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

Add a "Viewing:" line under the title that switches based on `RISK.is_ddr`:

```javascript
function renderFooter(){
  // ... existing brandSub + foot ...
  const regName = RISK.is_ddr ? 'Design Discipline Register (DDR)' : 'Master Risk Register (PRR)';
  const other = RISK.is_ddr ? {url: '../', label: 'Master Risk Register (PRR)'} : {url: 'DDR/', label: 'Design Discipline Register (DDR)'};
  $('#registerNav').innerHTML = `Viewing: <b>${esc(regName)}</b> · <a href="${esc(other.url)}">→ ${esc(other.label)}</a>`;
}
```

The build script sets `"is_ddr": true` in the DDR's data payload, and the template reads `RISK.is_ddr` to pick the right name + link. Default false (PRR) when key absent.

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
- **The DDR xlsx is the same as the PRR xlsx** (the C11 master workbook contains both sheets — "Risk Register" + "Designer Risk Register (DRR)"). Don't create a separate DDR xlsx; the deploy script copies the same file once.
