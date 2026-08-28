# Downloads Cleanup with Quarantine Dedup (2026-08-27)

Worked example: `/Volumes/MIcro/Download` — 9.9 GB, ~1,944 files, 151 loose at root + 256 in `Other/`.

## Outcome
- Root: 151 loose files → 0 (routed into existing category folders).
- `Other/`: 256 loose files → 0.
- 2,153 system-junk files deleted (all `._*` AppleDouble, `.DS_Store`, `desktop.ini`, `.dwl/.dwl2`, `~$*` locks, `plot.log`, `acadlt.fmp`).
- 534 duplicate/older files (633.5 MB) moved to `_Duplicates_To_Review/` — NOT deleted.
- Active tree: 1,437 files, 9.02 GB. Register: `_Download_Register.csv`.

## Key decisions
1. **Quarantine over delete.** User didn't answer the keep-history clarify prompt. Per the "never delete user files without explicit confirmation" rule, moved all redundant copies to `_Duplicates_To_Review/` (paths preserved) instead of hard-deleting. Reported the folder as the only remaining cleanup step.
2. **Version chains = keep newest, quarantine rest.** Risk registers (EXP-RISK-* had 9 copies), Design Trackers, Draft_Bill_proforma, VIOL, جدول مقاسات, Samaya-Factory quotations (S00160/S00161), WhatsApp image chains — all same-name-different-content. Kept newest mtime in place.
3. **Cross-folder same-name files left alone.** `AV_Submittal_Register.xlsx` in Submittals vs Registers, `Register Log` variants, `AV Audit Report` — verified DIFFERENT md5 (distinct revisions), left both.
4. **WhatsApp `(N)` photos are NOT duplicates** — genuinely different images, left untouched.
5. **CAD support files** (`.pat/.shx/.ttf`) duplicated across drawing subfolders are part of the drawing packages — left in place.

## Routing rules used (Aseer-Museum)
- `MOC-*`, `A2742-*`, `MOC-MUS-*` → Submittals
- risk/register/tracker/exportdocs/exportmailall → Registers
- `RE:`/`Re:`/`FW:`/`CG-`/nissenrichardsstudio/wetransfer/OneDrive_* → Correspondence
- invoice/purchase order/quotation/دفعه → Financial
- drawing/layout/fire alarm/power layout/260816/260821/260824/20-08-2026/drive-download/قصر شبرا → Drawings
- scanner/lidar/faro/leica/spider/artec/einscan/3d_/spec sheets → Technical
- `.dmg` → Software; نموذج توظيف/استحداث → HR; id_rsa/twilio/discord → `__SECURE`

## Pitfalls hit
- **Near-dup regex bug**: `re.sub(r'\s*\(\d+\)\s*$','',f)` on full filename fails because `.pdf` follows the `(N)`. Must `os.path.splitext` first, strip suffix from stem, group on `(base, ext)`.
- **Misroute**: `Audinate scope of work.xlsx` matched a broad `scope of work` rule and went to Aseer-Museum/Submittals instead of Audinate/. Fix by checking more specific rules first (project folder match before generic content match).
- **Hardware spec sheets** (Knauf/Mada proposals, Leica, Faro, Spider) initially routed to Financial by a broad `proposal` rule — corrected to Technical. Order rules most-specific-first.
- **`_moved` suffix artifact**: when a file collided with an existing destination, the `_moved` copy itself became a near-dup; quarantine it too.
