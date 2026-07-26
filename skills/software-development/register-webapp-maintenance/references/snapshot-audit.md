# Excel Snapshot Audit Checklist

Use after generating or receiving an Excel snapshot from `build_snapshots.py --bump`.

## Dashboard Sheet

- [ ] Header shows correct register name (PRR/DDR/HSE)
- [ ] Doc ref matches format `EXP-RISK-{REG}-{YEAR}-{SEQ}`
- [ ] Rev matches current data (C12 for PRR, C11 for others)
- [ ] Snapshot date is today (not stale)
- [ ] Source URL points to correct register page
- [ ] KPI counts match webapp (PRR=61, DDR=79, HSE=41)
- [ ] Rating split matches webapp
- [ ] Risk Matrix populated with correct counts
- [ ] **Exposure by Category matches register RBS codes**

## CRITICAL: Category Check

The Exposure by Category table **must** show the correct RBS codes for that register, NOT PRR codes:

| Register | Expected categories |
|----------|-------------------|
| PRR | PRC, COM, DES, APP, CON, SCH, CNS, FLS, LOG, MEP, SIT, STK, HSE, OPS, SEC, AV, QLT, TCH |
| DDR | TEC, SCH, EXT, PRO, QA, COM |
| HSE | HSE (only one) |
| AVR | HW, IFC, LGT, MEP, OPS, STR |

If the DDR dashboard shows PRC=0, COM=4, SCH=8 (only 12 of 79 risks), the data source is wrong — DDR should show TEC=49, EXT=8, etc.

## Risk Register Sheet

- [ ] Has 3 sheets: Dashboard, Risk Register, Action Plan
- [ ] Column headers present: ID, CAT, RATING, SCORE, STATUS, OWNER, TARGET, TITLE, CAUSE, CONSEQUENCE, RESPONSE, EVIDENCE
- [ ] **Risk IDs use current format** (DDR-{CAT}-{NN}, not old PR-Q-001)
- [ ] No SMP-prefixed IDs (PRR-SMP-001/002 should be COM-08/PRC-13)
- [ ] All risks present (count matches header)
- [ ] No blank rows in data

## Action Plan Sheet

- [ ] Actions listed per risk ID
- [ ] Due dates present
- [ ] Owners assigned

## Filename Convention

Format: `EXP-RISK-{REG}-{YEAR}-{SEQ}_Rev{REV}_{STATUS}.xlsx`

Examples:
- `EXP-RISK-PRR-2026-004_RevC12_ACTIVE.xlsx`
- `EXP-RISK-DDR-2026-004_RevC11_ACTIVE.xlsx`
- `EXP-RISK-HSE-2026-003_RevC11_ACTIVE.xlsx`

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Old risk IDs (PR-Q-001 instead of DDR-SCH-01) | Source JSON has old IDs | Run rename on source JSON, rebuild |
| Wrong dashboard categories | Snapshot built from wrong data file | Check `build_snapshots.py` reads correct JSON |
| Stale date | Snapshot not regenerated | Run `build_snapshots.py --bump` |
| Risk count off | Source JSON contaminated with cross-register risks | Clean `risks.json` to PRR-only |
| File not found by webapp | Old higher-numbered file still exists | Delete old files after --bump |
