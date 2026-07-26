# Risk ID Conventions — Aseer Museum Registers

## PRR (Master Risk Register)

**Format:** `PRR-{RBS}-{NN}`

| Part | Meaning | Values |
|------|---------|--------|
| `PRR` | Register prefix | PRR |
| `{RBS}` | RBS category code | APP, AV, CNS, COM, CON, DES, FLS, HSE, LOG, MEP, OPS, PRC, QLT, SCH, SEC, SIT, STK, TCH |
| `{NN}` | Sequential number (01–99) | 01, 02, ... |

**Example:** `PRR-COM-08` (8th Commercial & Contractual risk)

**Rules:**
- 2-digit zero-padded sequence (`01` not `1`)
- RBS codes match the `rbs_categories` in the JSON exactly
- Unused RBS codes (`SMP`, etc.) must NOT appear as ID prefix — renumber into the correct RBS category

## DDR (Design Discipline Register)

**Format:** `DDR-{RBS}-{NN}`

**RBS categories:** COM, EXT, PRO, QA, SCH, TEC

**Migration:** Renamed from sub-category codes (`PR-Q-001`, `RE-Q-001`, `ST-E-001`, `DB-M-001`, `CO-X-001`, etc.) to flat `DDR-{RBS}-{NN}` format (79 risks).

## AVR (AV & Multimedia Register)

**Format:** `AVR-{RBS}-{NN}`

**RBS categories:** HW, IFC, LGT, MEP, OPS, STR

**Migration:** Renamed from mixed format (`PRR-AV-01`, `PRR-AV-02`, `R-AV-08` through `R-AV-17`) to `AVR-{RBS}-{NN}` format (12 risks).

## HSE (HSE Risk Register)

**Format:** `HSE-{NN}` (flat sequential, single category — no RBS code in ID)

**Migration:** Renamed from sub-group format (`HSE-1.1`, `HSE-2.1`, `HSE-5`, etc.) to flat `HSE-{NN}` (41 risks).
