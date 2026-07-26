# Risk ID Conventions — Aseer Museum Registers

## PRR — Master Risk Register (61 risks)

**Pattern:** `{PREFIX}-{RBS_CATEGORY}-{NN}`

| Part | Meaning | Example |
|---|---|---|
| `PRR` | Register prefix — Project Risk Register | `PRR` |
| `{RBS}` | 3-letter RBS category code (18 codes) | `APP`, `COM`, `DES` |
| `{NN}` | Sequential number within that category, 2-digit | `01`, `02`, `03`… |

**18 RBS codes used:**
`APP`, `AV`, `CNS`, `COM`, `CON`, `DES`, `FLS`, `HSE`, `LOG`, `MEP`, `OPS`, `PRC`, `QLT`, `SCH`, `SEC`, `SIT`, `STK`, `TCH`

**Numbering:** sequential per category (2-digit padding). Next COM risk = PRR-COM-09 (current max is COM-08).

## DDR — Design Discipline Register (79 risks)

**Pattern:** `DDR-{RBS_CATEGORY}-{NN}`

Categories and counts:

| Category | Count | Example IDs |
|----------|-------|-------------|
| `TEC` (Technical/design) | 49 | `DDR-TEC-01` … `DDR-TEC-49` |
| `SCH` (Schedule/design) | 8 | `DDR-SCH-01` … `DDR-SCH-08` |
| `EXT` (External/Authority) | 8 | `DDR-EXT-01` … `DDR-EXT-08` |
| `PRO` (Procurement/design) | 5 | `DDR-PRO-01` … `DDR-PRO-05` |
| `QA` (Quality/design) | 5 | `DDR-QA-01` … `DDR-QA-05` |
| `COM` (Commercial/design) | 4 | `DDR-COM-01` … `DDR-COM-04` |

**Old IDs renamed (2026-07-26):** Previous format used sub-category codes (e.g. `PR-Q-001`, `COM-CM-001`, `ST-E-001`, `EX-X-001`). These were all renamed to the standard `DDR-{CAT}-{NN}` format. The sub-category codes (PR, DB, ST, CO, TE, EX, BI, RE, QA) are no longer used.

## AVR — AV & Multimedia Register (12 risks)

**Pattern:** `AVR-{RBS_CATEGORY}-{NN}`

Categories:

| Category | Count | Example IDs |
|----------|-------|-------------|
| `HW` (Hardware & long-lead) | 4 | `AVR-HW-01` … `AVR-HW-04` |
| `IFC` (IFC/Design maturity) | 3 | `AVR-IFC-01` … `AVR-IFC-03` |
| `OPS` (Operations & content) | 2 | `AVR-OPS-01` … `AVR-OPS-02` |
| `LGT` (AV-Lighting interface) | 1 | `AVR-LGT-01` |
| `MEP` (AV-MEP interface) | 1 | `AVR-MEP-01` |
| `STR` (AV-Structure interface) | 1 | `AVR-STR-01` |

**Old IDs renamed:** `PRR-AV-01/02` and `R-AV-08`…`R-AV-17` were all renamed to the standard `AVR-{CAT}-{NN}` format.

## HSE — Health & Safety Register (41 risks)

**Pattern:** `HSE-{NN}` (sequential, no category — only one RBS category: HSE)

| Range | Count |
|-------|-------|
| `HSE-01` … `HSE-41` | 41 |

**Old IDs renamed:** Previous format used `HSE-1.1`, `HSE-2.1`, `HSE-47` etc. (with decimal sub-numbers and gaps). Renamed to sequential `HSE-01`…`HSE-41`.

## Rules

1. Never reuse an ID — retired on close/mitigation.
2. Sequential within category — use 2-digit padding (`01`–`99`).
3. Prefix matches register (PRR/DDR/AVR/HSE).
4. Category codes are fixed — do not invent new RBS codes without updating the `rbs_categories` map.
5. Risk ID is the primary key — used in deep-links and cross-refs from other registers.

## Data integrity checks

### Zero-padding consistency
All sequential numbers use **2-digit padding** (`01`–`99`). Never use 3-digit (`001`).

```python
bad = [r['id'] for r in risks if re.search(r'-\d{3}$', r['id'])]
if bad: print(f"NON-STANDARD PADDING: {bad}")
```

### Category match between ID and field
The category segment in the risk ID must match the `category` field value. A risk with ID `PRR-SMP-001` but `"category": "COM"` is inconsistent.

### CR-sheet import pitfalls
Risks imported from CG Comment Response (CR) sheets often arrive with non-standard IDs:
- **Wrong prefix**: uses the plan code (`SMP`) instead of the register prefix (`PRR`).
- **Non-RBS category code**: `SMP` is not a valid RBS code.
- **Wrong zero-padding**: 3-digit `001`.
- **Action IDs prefixed with old code**: `SMP-001-A1` instead of plain `A1`.

Fix procedure:
1. Check the `category` field to determine the correct RBS code.
2. Find the current max sequential number for that category.
3. Rename to `{REGISTER}-{RBS}-{next NN}` with 2-digit padding.
4. Normalize action IDs to the register's convention (`A1`, `A2` — no prefix).
5. Update `last_updated`. Verify the renamed ID does not conflict. Deploy.

## Renaming bulk risk IDs — procedure

When renaming all risks in a register (e.g. during format standardization):

1. **Identify source data files** — each register has its own:
   - PRR: `06_Risk_System/risks.json`
   - DDR: `06_Risk_System/generated/drr_risks.json`
   - HSE: `06_Risk_System/generated/hse_risks.json`
   - AVR: `webapp/av/risks_av.json`

2. **Load JSON, rename by category** — group risks by `category` field, sort by old ID within each group, assign new sequential numbers:
   ```python
   from collections import defaultdict
   by_cat = defaultdict(list)
   for r in risks:
       by_cat[r['category']].append(r)
   rename_map = {}
   for cat in sorted(by_cat.keys()):
       items = sorted(by_cat[cat], key=lambda x: x['id'])
       for i, r in enumerate(items, 1):
           rename_map[r['id']] = f"{prefix}-{cat}-{i:02d}"
   ```

3. **Update references** — search `evidence` arrays and `history` notes for old IDs and replace with new ones.

4. **Rebuild and deploy** — run the register's build script:
   ```bash
   cd 06_Risk_System/webapp && python3 build_{register}.py
   ```
   The build script injects data into `template.html` and runs `fix_cards_static.py` as post-processor.

5. **Deploy to server** — commit and push. The auto-deploy cron (15-min cycle) will deploy. Do NOT SCP directly — it gets overwritten.

6. **Verify** — check that the live page loads all risks with correct IDs, and no old IDs remain:
   ```bash
   curl -s URL | grep -c 'OLD-ID-PATTERN'  # should be 0
   ```
