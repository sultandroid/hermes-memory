# Aseer Museum `24_Subcontractors` — Duplicate Folder Merge Audit (2026-08)

Worked example of the dedup consolidation workflow (SKILL.md §6b). The folder had
drifted into 40+ top-level entries under conflicting numbering schemes (README
canonical list vs actual on-disk state). **EXECUTED 2026-08-27**: 8 redundant
folders moved to `_Deprecated_Duplicates/` (see Execution section below).

## Canonical keeper detection rule
The keeper folder for each discipline has ALL of:
- `_MANAGER_DASHBOARD/` with `SCOPE_REQUEST.md`, `SITUATION_REPORT.md`, `SPEC.md`,
  `Master_Submittal_Register.xlsx`
- `<Discipline>_Submittal_Register/` subfolder
- per-vendor prequalification subfolders (e.g. `09_Prequalification/ACOUSTIEG/`)
Stub folders have only 1–2 loose PQ PDFs.

## Merge matrix (keep / merge / delete)

| Cluster | Duplicate folders | Verdict |
|---|---|---|
| Acoustic | `01_Acoustic` (2 f), `03_Acoustic_Specialist` (2 f) | Both stubs → merge into `18_Acoustic_Specialist` (61 f, full), delete stubs |
| Interactive | `19_Interactive_Design_Contractor` (8 f) | Exact MD5 dup of `09`'s `08_Quotations/` → keep `09_Interactive_Design_Contractor` (43 f), delete 19 |
| AV/IT | `06_AV_IT_Rawasin` (10 f) | Rawasin files already inside `04_AV_IT_Contractor` (367 f, full), MD5-identical → merge 06→04, delete 06 |
| Rigging | `06_Rigging` (3 f), `10_Rigging` (7 f) | Both subsets of `06_Rigging_Contractor` (35 f, full) → merge, delete both |
| Landscaping | `02_Landscaping` (2 f), `03_Landscaping` (147 f, 682 MB) | `21_Landscaping_Specialist` (187 f, 682 MB) is strict superset → keep 21, delete 02+03 |
| Setwork/vendor stubs | `Furniture_Anaroque`, `Setwork_BTT`, `Setwork_Saudi_Emaar` (1 f each) | MD5-identical to files already in `04_Setwork` → delete all 3 |

## Flagged as "needs user decision" (do NOT auto-merge)
- `14_MEP_Contractor` (14 f) — **mislabeled**: holds StudioZNA lighting fee/scope PDFs,
  `Dogan Kozan_CV` (ZNA design contact), AV BTU/power per-zone workbooks, ICT & BMS
  scope docs, `SI-CG-ASEER-007`. Not MEP contractor content. Candidate re-file:
  ZNA items → `02_Lighting_Designer`; ICT/BMS scope → `14_CITC_Telecom_Engineer` or
  own folder. User decides.
- `09_General` — holds an Archaeological Museums commercial/technical proposal
  (likely a different procurement) + `MOC-MUS-ASE-1K0-ZD-0095`. Not a discipline sub.
  Keep, relocate, or archive — user decides.
- `04_Setwork` is an empty-shell name but actually holds 8 PQ files (PQ-0130…0139,
  multi-trade) — keep as-is, don't touch.

## Exact commands that worked
```bash
# sizes
du -sh */ | sort -t$'\t' -k2
# per-folder file counts (excl .DS_Store)
for d in <folders>; do n=$(find "$d" -type f ! -name ".DS_Store" | wc -l | tr -d ' '); echo "$d : $n"; done
# superset/subset file-name diff
diff <(cd A && find . -type f ! -name ".DS_Store" | sort) \
     <(cd B && find . -type f ! -name ".DS_Store" | sort)
# content diff
diff -rq A B 2>&1 | head
# MD5 proof of duplicate
a=$(md5 -q "A/path/file"); b=$(md5 -q "B/path/file"); [ "$a" = "$b" ] && echo IDENTICAL
```
macOS: `md5 -q <file>` (not `md5sum`). `.DS_Store` must be excluded from every
count/diff or it masks real deltas.

## Execution rule (not yet run)
OneDrive moves are destructive — no `rm -rf`/`mv`. Present the table, get keeper +
mislabeled-folder sign-off, THEN merge via safe rename and update `README.md`
register table + status reports.

## Execution (run 2026-08-27) — resolved
Moved into `24_Subcontractors/_Deprecated_Duplicates/` (all `mv`, nothing deleted):
`01_Acoustic`, `03_Acoustic_Specialist` (→ keep 18), `02_Landscaping`, `03_Landscaping`
(→ keep 21), `06_Rigging` (→ keep 06_Rigging_Contractor), `19_Interactive_Design_Contractor`
(→ keep 09), `06_AV_IT_Rawasin` (→ keep 04), and `10_Rigging` (nested redundant
re-nest inside `06_Rigging_Contractor`, md5-identical to the folder's own
top-level `01_Prequalification/`).

Also quarantined the byte-identical `_dup` copies: AV `PQ-0133/0134_dup` + Molitor
scope/zip `_dup`, Acoustic `PQ-0124 Rev.01_dup`.

**Still KEPT (different md5 = distinct revision, not a dup):**
- `06_Rigging_Contractor/01_Prequalification/MOC-MUS-ASE-1C0-PQ-0131_dup.pdf`
  (3.4 MB vs 1.2 MB orig) and `PQ-0132_dup` (14 MB vs 1.2 MB) — larger scans.
- `21_Landscaping_Specialist/01_Prequalification/MOC-MUS-ASE-1L0-PQ-0122 Rev.01_dup.pdf`
  (15.9 MB vs 15.5 MB orig).
- Root `SCOPE OF WORK_dup.pdf` — different content.

**Still awaiting user decision:** `14_MEP_Contractor` (mislabeled grab-bag, NOT
duplicated MEP content) — see "Flagged" above. Unchanged this session.
