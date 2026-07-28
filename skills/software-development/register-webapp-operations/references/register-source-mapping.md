# Register Source File Mapping — Aseer PM Repo

**CRITICAL: There are TWO lessons-learned files in the repo — the webapp reads from only one.**

## Lessons Learned
| File | Purpose |
|------|---------|
| `03_Plans/11_Quality/lessons_learned_register.md` | **Webapp source** — parsed by `update-all-registers.sh`. Must use `LL-` prefix in IDs. |
| `01_Registers/lessons_learned_register.md` | Standalone simplified register. **NOT read by the webapp.** |

**Before editing any register, verify which file feeds the target webapp.**

## Webapp → Source mapping

| Webapp | Source File | ID Format Required |
|--------|------------|-------------------|
| LN | `03_Plans/11_Quality/lessons_learned_register.md` | `LL-NNN` (e.g. `LL-018`) |
| Risk (PRR) | `06_Risk_System/risks.json` | `PRR-{RBS}-{NN}` |
| DDR | `06_Risk_System/ddr_risks.json` | `DDR-{RBS}-{NN}` |
| HSE | `06_Risk_System/hse_risks.json` | `HSE-{NN}` |
| AVR | `06_Risk_System/av_risks.json` | `AVR-{RBS}-{NN}` |

## LN webapp ID format requirement

The parser in `update-all-registers.sh` (Python inline) scans pipe-delimited markdown rows and **skips any row whose ID does not contain `LL-`**. This means:
- `14 | ...` → **skipped** (no `LL-` prefix)
- `18 | LL-018 | ...` → **parsed** correctly

Always use the `LL-` prefix when adding lessons to the webapp source file.
