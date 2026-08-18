# Duplicate Merge + Action-Plan Progress Pass (Aseer PRR)

Two recurring tasks that keep the live snapshot showing real progress. Both mutate
`06_Risk_System/risks.json` (the source of truth) and require the multi-JSON sync +
rebuild + deploy + OneDrive-copy dance.

## The multi-JSON store (critical — never update only one file)

`risks.json` is NOT the only copy. Three JSON files hold PRR data with **different
subset structures** — sync all three or the dashboard/webapp go stale:

| File | Scope | Wrapper keys | Notes |
|------|-------|--------------|-------|
| `risks.json` | 69 (all PRR) | `project, doc_ref, revision, last_updated, registers, risks, total_risks, merge_note` | **Source of truth** — always edit this first |
| `prr_risks.json` | 66 | adds `contract, scoring, rbs_categories, owners, categories, total` | Feeds dashboard; **may be missing recent risks** (e.g. PRR-AVS-02, PRR-MEP-03, PRR-SHC-02) |
| `dashboards/risks.json` | 32 (curated subset) | `project, contract, ..., scoring, owners, risks, total` | Subset does NOT include every risk (lacks e.g. PRR-LOG-01, PRR-NCR-001) |

**Sync pattern** (after editing risks.json):
```python
src = json.load(open('risks.json'))
srcmap = {r['id']: r for r in src['risks']}
for p in ['prr_risks.json', 'dashboards/risks.json']:
    d = json.load(open(p))
    for i, r in enumerate(d['risks']):
        if r['id'] in srcmap:
            d['risks'][i] = srcmap[r['id']]   # replace object wholesale
    d['last_updated'] = src['last_updated']
    if 'total' in d: d['total'] = len(d['risks'])
    if 'total_risks' in d: d['total_risks'] = len(d['risks'])
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=2)
```
Because dashboards is a subset, a merge script that assumes `by_id[target]` exists for
every survivor will crash (`KeyError: PRR-LOG-01`). Handle subset files by removal, not
merge-in.

## Merging duplicate risks (append-only, follow the survivor pattern)

Precedent commit `47f18ca` (4 dups merged) and this session (4 dups → 3 survivors).

Steps:
1. **Identify true duplicates** — same root cause / same evidence, not just same category.
   E.g. PRR-COM-01+PRR-COM-05 (same EOT dispute), PRR-STK-02+PRR-NCR-001 (**identical**
   NCR count 13/4/3/6), PRR-LOG-01+PRR-LOG-02+PRR-CON-05 (same remote-logistics/materials).
2. **Survivor keeps the live data**; absorbed risk's `evidence`, `actions`, `history`
   are appended (label absorbed actions `[absorbed from PRR-X]`, add a merge history note).
   Bump survivor `last_reviewed`; append `[MERGE <date>: ...]` to `response_action`.
3. **Mark the absorbed treatment file** `status: merged` + `merged_into: <survivor>` with a
   `# MERGED — X → Y` header (see `03_Plans/08_Risk/treatment/PRR-COM-05.md`).
4. **Update code mappings** that reference the absorbed ID — e.g. `scripts/document_intake.py`
   had `"ncr": "PRR-NCR-001"` which must become `PRR-STK-02`, or new NCR intake breaks.
5. Remove the absorbed IDs from the JSON `risks` array; drop total counts accordingly.

## Action-plan progress pass (so each new snapshot shows progress)

The user's explicit goal: **"الهدف من تحديث السنابات هو اظهار التقدم"** — every new snapshot
must show the action-plan advancing, not stale dates.

Pattern:
1. Read all evidence sources: `03_Plans/08_Risk/reviews/email_scan_*.md` (Aug scans),
   `01_Registers/*.md` (submittal, prequalification, ncr, si, rfi, letters, meeting_minutes,
   procurement, material_submittal, specialist_register).
2. Cross-check claims against the authoritative register before applying (subagent
   findings are self-reports — verify, e.g. PEP Code B confirmed in submittal_register
   line `ZD-0086 Rev.02 ... B`).
3. Map each evidence item to a risk + action. Update per-action:
   - `Not Started → In Progress` when work started
   - `→ Done` when the deliverable is approved/closed (with the approval date as `due`)
   - `→ Overdue` when a formal deadline (e.g. LT-003 14-WD) passed without action
   - roll forward `due` dates for In-Progress items so they read as ongoing, not stale
4. **Rating downgrade on root-cause resolution**: if a parent risk's blocking condition is
   approved (e.g. PEP Rev.02 Code B closes SCH-05's root cause), downgrade the rating and
   set status `Mitigated` — but only when the *parent's* blocker clears, not a sub-approval.
   (Sub-approval ≠ parent closure — see email-scan-risk-review.md.)
5. Then: sync the 3 JSONs → `python3 risk_sync.py --json risks.json` (regenerates
   `01_Registers/risk_register.md` — note the markdown table does NOT carry the action plan,
   so it may show no diff; the actions live only in the JSON + xlsx) → rebuild + deploy.

## Deployment path pitfall (why live page looked stale)

Root `.htaccess` rewrites ALL requests to `/build/`:
```
RewriteCond %{REQUEST_URI} !^/build/
RewriteRule ^(.*)$ /build/$1 [L]
```
But `webapp/deploy.sh` rsyncs to `public_html/aseer/registers/Risk/` (non-build).
The post-commit hook (`update-all-registers.sh`) is what deploys to the served `/build/`
path. **Lesson: after editing risks.json, COMMIT to git (triggers the build-path deploy);
don't rely on `bash deploy.sh` alone for the live page.** Verify live with
`curl .../Risk/?cb=NNN` and grep the `const RISK = {...}` JSON for the new count/values.

## OneDrive submission snapshots — corrupt-stub trap

Files in `05_Submittle/REV01/{01_Master..,02_Design..,03_HSE..,04_AV..}` named
`Aseer_Museum_{PRR,DDR,HSE,AVR}_Snapshot_YYYY-MM-DD.xlsx` can be **OneDrive files-on-demand
stubs** — 4,511 bytes of HTML (`"This Page Does Not Exist"`), not real Excel. Symptom: Excel
"file format or extension is not valid". Fix:
1. `file <name>` — if it reports `HTML document`, it's a stub, not a real xlsx.
2. Regenerate from `webapp/src/EXP-RISK-{PRR,DDR,HSE}-latest` and `av/src/EXP-RISK-AV-latest`.
3. Copy over the OneDrive name. Archive (don't delete) the old stub into `_CORRUPT_<date>/`.
   (Never `rm` OneDrive files — see memory.)
4. Verify each copy with `openpyxl.load_workbook` (sheets = Dashboard/Risk Register/Action Plan).
