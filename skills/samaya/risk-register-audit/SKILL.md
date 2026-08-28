---
name: risk-register-audit
description: "Audit Aseer Museum risk register entries against real evidence from repo + Adel Darwish bank. Verify owners, dates, evidence, status, PxS, and factual claims before updating."
---

# Risk Register Audit Workflow

## Purpose
Verify all risk register entries against real evidence before updating. Every claim must be traceable to a real file or record.

> **Recurring task — "check all email scans, any risks to update/close?":** see `references/email-scan-risk-review.md` for the full workflow (scan locations, cross-reference pattern, update pattern). It also covers the **Action-Plan Progress Pass** (user requires every snapshot to show progress — update `actions[]` status/due from evidence, roll forward In-Progress past-due dates, sync all mirrors, report the KPI delta) and two hard user rules: **(1) a risk whose core is "plan stays rejected (Code C/D)" is CLOSED once that plan reaches Code B** (actions stay in the action plan); **(2) never embed internal reasoning/justification in `response_action`/`title`** — keep it factual.

> **Merging duplicate risks / OneDrive snapshot stubs:** see `references/merge-duplicate-risks.md` — de-dup groups, the full merge workflow (SoT `risks.json` → all mirrors → rebuild → deploy → verify), and the pitfall where `05_Submittle/REV01/` submission snapshots are 4.5KB HTML "This Page Does Not Exist" stubs that Excel rejects (fix: detect via `file` magic bytes, regenerate from `webapp/src/EXP-RISK-*_ACTIVE.xlsx`, move stubs to `_CORRUPT_/` not delete).

> **Risk webapp UI (Recent Updates block, per-page header, multi-page rebuild, Rescheduled field):** see `references/risk-webapp-ui.md` — the Recent Updates block reads `history[]` (not `last_reviewed`) and shows the change note above the table, how to filter internal-noise history rows, the header `last_updated` source-of-truth per page (DDR/HSE/AV read their own JSON, not `risks.json`), that a `template.html` edit must be rebuilt into all four pages before deploy, and how to record a `target_close` move via the `rescheduled` object shown in the Ownership & Tracking drawer.

> **HARD RULE — `risks.json` is the PRR source of truth, NOT the markdown register.** The sync direction is **JSON → MD**: `python3 risk_sync.py` regenerates `01_Registers/risk_register.md` FROM `06_Risk_System/risks.json`. NEVER edit the `.md` register directly for PRR changes — it is a generated artifact and will be overwritten on the next sync. To update a PRR risk: edit `risks.json` (mutate the risk object, bump `revision`, set `last_updated`, append a `history[]` row), then run `risk_sync.py`, then `webapp/build_risk.py`. DDR/HSE/AV have their own JSONs/embedded HTML + their own rebuild commands. Excel snapshots: `webapp/build_snapshots.py --bump`, and the `.xlsx` files are **gitignored** (binaries stay in OneDrive) — `build_risk.py` auto-discovers the latest `src/EXP-RISK-PRR-2026-*_ACTIVE.xlsx` for the webapp download button.

## GitHub risk-tracker issue lifecycle — do NOT manually close auto-synced risk issues

The `aseer-museum-pm` repo has ~188 **open risk-tracker GitHub issues** (titles `Risk — <ID>`, labels `risk-tracker,risk-daily,{PRR|DDR|HSE|AV}`). These are **auto-generated and auto-synced** by `scripts/risk_issue_daily.py`, which reads the current state of every risk from `06_Risk_System/{prr,ddr,hse,av}_risks.json` and posts a dated status comment ONLY when the risk's state changes. The script **closes an issue automatically** when its underlying risk's `status` becomes `closed` or `mitigated` in the JSON.

**When the user asks to "close the open issues" (or "شوف المشاكل واقفلها"):**
1. **Distinguish the two classes.** Risk-tracker issues (188) are NOT manual work — closing them by hand is wrong and is overridden by the next cron sync. The non-risk issues (known-issue, question, commercial, discussion, bug) ARE real triage targets.
2. **Find the real ones:** `gh issue list -R sultandroid/aseer-museum-pm --state open --limit 300 --json number,title,labels -q '.[] | select(([.labels[].name] | join(",")) | test("risk-tracker") | not) | "\(.number)\t\([.labels[].name]|join(","))\t\(.title)"'`
3. **To see which risk issues are closable per the SoT, run the sync in dry-run:** `python3 scripts/risk_issue_daily.py --dry-run` → `Closed=N`. If N=0, ALL risk issues are genuinely still open per the JSON — there is nothing to close, and closing them manually would be a false closure.
4. **Only a risk whose status turns `closed`/`mitigated` in `*_risks.json` becomes closable** — the daily cron (`risk_issue_daily.py`, job `204dc4f6de92`) does it. Your job is to find *evidence* that a risk's premise is now false (e.g. the "specialist not appointed" risk is void because the specialist was folded into an internal scope — Rawasin for interactives, Samaya in-house for structural) and propose the JSON status change to the user for approval (hard rule: NEVER modify a risk without prior user approval). Once approved, edit the JSON, run `risk_sync.py` + rebuild + `--bump` snapshots, and the next sync closes the issue.

**Pitfall — don't waste effort re-closing resolved non-risk issues.** Prior sessions frequently close Open Questions / known-issues with evidence. Before chasing any open issue, run the filter above and check each one's `state` — many are already CLOSED. For a "what's still open?" review, the honest answer is often: all non-risk issues are closed, only the 188 risk-tracker auto-issues remain open (legitimately, per SoT).

> **Risk closure candidate review** (when the user asks "شوف دلائل لقفلها" / "find evidence to close the open issues"): see `references/risk-closure-evidence-review.md` — how to distinguish the ~188 auto-synced risk-tracker issues (closable ONLY by changing the risk's JSON status, not by hand) from real triage issues, and how to gather falsifying evidence (specialist register appointments, Code B = approved rule, in-house/folded specialist decisions, closed sibling DDR risks). Strong candidates + not-yet-closable list as of 2026-08-28.

## Evidence Sources (in priority order)

| Source | Path | What to Check |
|--------|------|---------------|
| Submittal register | `01_Registers/submittal_register.md` | Real submission/approval dates, CG codes |
| NCR register | `01_Registers/ncr_register.md` | Open NCR count, specific NCR references |
| RFI register | `01_Registers/rfi_register.md` | TQ/RFI status |
| Drawing register | `01_Registers/drawing_register.md` | Drawing status, phase |
| Prequalification log | `Technical_Office/Specialist_Management/prequalification_log.md` | PQ status, CG codes |
| Master programme | `02_Schedule/master_programme.md` | Schedule dates, milestones |
| Submission plan | `02_Schedule/submission_plan_risk_assessment.md` | Submission forecast dates |
| Treatment files | `03_Plans/08_Risk/treatment/` | Risk-specific response plans |
| Adel Darwish bank | `OneDrive/Adel Darwish's files - 01- Execution Documents/` | Physical file existence |

## Adel Darwish Bank Structure

```
Adel Darwish's files - 01- Execution Documents/
├── 01- Letters/           (LT-0027 EOT, etc.)
├── 02. DOC/               (Document submittals)
├── 03. SD/                (Shop drawings — SDW prefix)
├── 04- Daily Report/
├── 05- RFI/               (TQ-001 through TQ-022+)
├── 06- MOM/               (MoM-14, MoM-15, etc.)
├── 07- PQ/                (PQ-0007 through PQ-0125+)
├── 08- Material Submittal MA/  (MA-0001 through MA-0007)
├── 09- MS/                (Method statements)
├── 10- SI/                (SI-01 through SI-20)
├── 11- IFC/               (IFC-0003, IFC-0004, etc.)
├── 12- NCR/               (NC-001 through NC-1KN-SE-021)
├── 13- Weekly Report/
├── 14- IR/
├── 15- SNA/
├── 16- Safety/
├── 17- SOR/
├── 18- MIR/
├── 19- HSE/
├── 20- DDD/
```

## Audit Checklist (per risk)

| Check | What to Verify | Source |
|-------|---------------|--------|
| Owner | Site/construction risks -> Construction Manager, not Technical Office Mgr | Risk register + treatment file |
| Dates | target_close must be realistic, not past due without status update | Submittal register |
| Evidence | References must point to real files in repo or Adel bank | search_files + ls on OneDrive |
| Status | Open/Watch/Mitigated/Closed must match current reality | NCR register, submittal register |
| PxS | Must be consistent with actual severity (>=12=Critical, 8-11=High, 4-7=Medium, <=3=Low) | Calculate from P and S |
| Factual claims | Every claim (e.g. "IFC-0004 Rev.01 Code C") must be traceable | Cross-reference submittal register |

## Common Discrepancies Found

| Issue | Frequency | Fix |
|-------|-----------|-----|
| Owner = Technical Office Mgr for site risks | 2 instances (PRR-FLS-01, PRR-DES-07) | Change to Construction Manager |
| Evidence references to non-existent files (DDR-*, GAP-*) | 12+ instances | These exist in OneDrive/Aconex, not repo |
| NCR count understated | 2 instances (PRR-QLT-01, PRR-STK-02) | Update to actual count from ncr_register.md |
| SI count understated | 1 instance (PRR-QLT-01: "15 SIs" -> 20) | Update to actual count from Adel bank |
| Unverifiable evidence references (ZD-0076, ZD-0082) | 2 instances | Add to submittal register or correct reference |
| Blank target_close on High/Critical risks | 9 instances | Add realistic target dates |
| Target_close = today with Open status | 3 instances | Review for closure or extension |

## Structural Completeness Check

Beyond verifying claims, audit every risk for **required field presence** across all 5 registers.

### Data Sources & Action Plan Fields

| Register | Source File | Action Plan Field | # Risks |
|----------|------------|-------------------|---------|
| PRR | `06_Risk_System/risks.json` | `response_action` | ~109 |
| DDR/DRR | `06_Risk_System/generated/drr_risks.json` | `response_action` | ~79 |
| DDR (MD) | `01_Registers/design_discipline_risk_register.md` | `Immediate Control Action` (col 9) | ~122 |
| HSE | `06_Risk_System/generated/hse_risks.json` | `controls` | ~41 |
| AVR | `06_Risk_System/webapp/av/src/index.html` (embedded RISK JSON) | `response_action` | ~12 |
| Construction (project-specific) | `01_Registers/construction_risk_register.md` | `Mitigation` column | 20 |
| Construction (generic) | `01_Registers/construction_risk_register.md` | **NONE** — no action column | 40 |

### Audit Script Pattern

Use python3 to iterate risks and flag missing fields:

```python
import json
with open('path/to/risks.json') as f:
    data = json.load(f)
risks = data.get('risks', [])
missing = [r['id'] for r in risks
           if not r.get('response_action') or r['response_action'].strip() in ('', '—', '-')]
print(f'{len(risks)} risks, {len(missing)} missing')
for rid in missing:
    print(f'  {rid}')
```

For AVR (embedded in HTML), extract the RISK JSON:
```python
import re
with open('webapp/av/src/index.html') as f:
    content = f.read()
m = re.search(r'const RISK = (\{.+?\});', content, re.DOTALL)
if m:
    avr = json.loads(m.group(1))
```

### Known Structural Gaps (as of Jul 2026)

- **Construction C-001 to C-040**: 40 generic risks lack any action/mitigation column in the table format. If still active, add a Mitigation column.
- **HSE**: Uses `controls` field as the action plan (not `response_action`) — the field mapping differs from PRR/DDR/AVR.

## Deploy After Fixes

```bash
cd /Users/mohamedessa/aseer-museum-pm/06_Risk_System/webapp
bash deploy.sh
# Publishes to https://samaya-factory.com/aseer/registers/Risk/
```

The deploy script:
1. Reads `../risks.json` (source of truth)
2. Builds `src/index.html` (self-contained, 163KB)
3. Copies master Excel workbook to `src/`
4. Rsyncs to Hostinger `/build/aseer/registers/Risk/`

## OneDrive Deadlock Workaround

When reading files from Adel Darwish's bank, OneDrive may return "Resource deadlock avoided":
1. Quit OneDrive: `osascript -e 'tell application "Microsoft OneDrive" to quit'`
2. Wait 3-5 seconds
3. Retry the read
4. If still failing, use `strings` command instead of `pdftotext` for PDFs
5. Restart OneDrive after done
