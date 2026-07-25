# RMP ↔ Excel Sync Cycle (the 4-file reconciliation)

> Reference for `risk-register-management`. After ANY change to the live Excel register, four files in the repo must be reconciled in the same commit, plus the OneDrive DOCX/PDF mirror needs a manual Word edit.

## The four repo files (always in the same commit)

1. **`03_Plans/08_Risk/risk_management_plan.md`** — the plan markdown
   - Frontmatter: bump `last_updated: YYYY-MM-DD` and `revision: REVxx`
   - Section 2.1: Current Risk Snapshot table (Total / Critical / High / Medium / Low)
   - Section 4.2: Current Risk Distribution table (per RBS category)
   - Section 9.1: Register Structure table (4-register architecture)
   - Section 13: Register Status Summary table (C-number, count, status)
   - Section 7.3: Quantitative Metrics (3 EMV rows cite C-number)
   - Document Control table at the end: add new REV row describing what changed
2. **`06_Risk_System/risks.json`** — master register JSON
   - Bump `last_updated: YYYY-MM-DD` (and `revision: Cxx` if the workbook revision changed)
   - Risk count and contents should match Excel
3. **`06_Risk_System/dashboards/risks.json`** — usually a Critical+High subset
   - Bump `revision` and `last_updated`
   - Regenerate from the master JSON (filter to `rating in ("Critical", "High")`)
   - Back up the previous version to `dashboards/risks.json.bak` first
4. **`01_Registers/risk_register.md`** — the rendered register
   - Regenerate via `python3 06_Risk_System/risk_sync.py` (one-way sync: JSON → MD)
   - The script auto-handles frontmatter and table formatting

## The optional 5th file: generated/ outputs

If the workbook now contains new DDR risks, also produce:

- `06_Risk_System/generated/drr_risks.json` (full DDR JSON)
- `06_Risk_System/generated/drr_register_C<rev>.csv` (DDR CSV)
- `06_Risk_System/generated/master_register_C<rev>.csv` (master CSV)
- `06_Risk_System/generated/README.md` (index file)
- `06_Risk_System/source/C<rev>_reference/Aseer_Museum_Risk_Register_C<rev>_<date>.xlsx` (staged source)
- `06_Risk_System/source/README.md` (index file)

## The 6th file: OneDrive DOCX/PDF mirror (manual)

The user must open the OneDrive DOCX (`MOC-MUS-ASE-1KH-PL-02.17_Risk_Management_Plan.docx`) in Microsoft Word and apply the same edits the agent made in MD. Then re-render the PDF (File → Save As → PDF) and save both back to OneDrive.

**The agent cannot do this step.** Reasons:

- The DOCX is usually OneDrive-locked (see `references/onedrive-locked-excel-recovery.md`).
- Even if `python-docx` can read the file, write-back triggers a new deadlock.
- Word's "Save As PDF" is the canonical way to regenerate the PDF; the agent's PDF tools can't reproduce Word's layout.

**Tell the user the exact 4-section diff to apply.** A useful format:

> Apply these edits in Word:
>
> | Section | Before | After |
> |---------|--------|-------|
> | Frontmatter | `revision: REV00` | `revision: REV01` |
> | Frontmatter | `last_updated: 2026-07-18` | `last_updated: 2026-07-24` |
> | Section 2.1 | C05, 29/10/10/7/2 | C11, 51/11/8/17/15 |
> | Section 9.1 (PRR) | 29 risks | 51 risks |
> | Section 9.1 (DDR) | 77 risks | 79 risks |
> | Section 13 | C05 / 29 / 77 | C11 / 51 / 79 |
> | Doc Control | ends at REV00 | add REV01 row |

## Git commit and push

After all repo files are updated:

```bash
cd ~/projects/<project>-pm   # or whichever repo
git add -A
git commit -m "RMP REV<n> sync: register counts to C<m> (count1 + count2 DDR)"
```

**Before pushing**, check for unpulled remote commits:

```bash
git fetch origin
git log --oneline origin/main ^main
```

If the remote has unpulled commits (almost always the case on a multi-agent setup), try:

```bash
git stash -u
git pull --rebase origin main
git stash pop
```

If `git pull --rebase` produces a conflict in real content (e.g. `01_Registers/risk_register.md`), **abort** and report:

```bash
git rebase --abort
```

**Never `git push --force` on real content.** `--force` is only safe for auto-generated files like `06_Risk_System/webapp/src/index.html` (when a post-commit hook regenerates it). For everything else, the conflict is real and needs user judgment.

## Cross-check after commit (sanity)

```bash
# 1. Repo JSON count matches Excel
python3 -c "import json; print(len(json.load(open('06_Risk_System/risks.json'))['risks']))"

# 2. RMP MD cites same C-number
grep -E "C[0-9]{2}|live register" 03_Plans/08_Risk/risk_management_plan.md | head

# 3. risk_register.md count
grep -c "^| PRR-" 01_Registers/risk_register.md
```

All three must agree.
