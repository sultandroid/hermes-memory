# Multi-Source Risk Register Update

## The Problem

The risk register lives in 4+ places. Changing a single risk (owner, status, date, score) requires updating ALL of them. Missing one creates inconsistency that the user will catch.

## The 4 Sources

| # | Source | Path | Update Method |
|---|--------|------|---------------|
| 1 | Markdown register | `01_Registers/risk_register.md` | `patch` tool |
| 2 | Excel workbook | `06_Risk_System/webapp/src/Aseer_Museum_Risk_Register_C11_*.xlsx` | openpyxl |
| 3 | Webapp HTML | `06_Risk_System/webapp/src/index.html` | Built from Excel via `build_risk.py` |
| 4 | Live site | `https://samaya-factory.com/aseer/registers/Risk/` | Deployed via `deploy.sh` |

## Update Sequence

```
1. Edit MD register (patch tool)
2. Edit Excel (openpyxl — find the risk row, update the cell)
3. Rebuild webapp: cd 06_Risk_System/webapp && python3 build_risk.py
4. Deploy: bash deploy.sh
```

## Risk Classification: Site vs Design

A risk that mentions "DD package" or "design" in its title may still be a **site-work risk** if the mitigation involves site investigations (core testing, rebar scanning, geotechnical boreholes, structural surveys).

**Canonical example — PRR-DES-07:**
- Title says "Structural DD 50% package returned Code C"
- But the mitigation is: core testing, rebar scan, geotechnical borehole — all site execution
- Owner should be **Construction Manager**, not Technical Office Manager

**Rule of thumb:** When in doubt, check whether the primary mitigation is:
- Site execution (core testing, surveys, installation, commissioning) → **Construction Manager**
- Document production (drawings, submittals, reports, specs) → **Technical Office Manager**

## Finding the Right Row in the Excel

The Excel has multiple sheets. PRR-DES-07 appears in:
- **Dashboard** sheet — row 34, col 4 (owner)
- **Risk Register** sheet — row 47, col 14 (owner)
- **Designer Risk Register (DRR)** — referenced in notes column

Search for the risk ID string across all sheets to find every occurrence.

## Finding the Right Entry in index.html

The webapp HTML embeds the full risk data as a JSON object on line 427:
```javascript
const RISK = {"project":"Aseer Regional Museum",...,"risks":[...]}
```

Search for `"PRR-DES-07"` in the file, then find the `"owner"` key within that entry and change its value. The entry looks like:
```json
{"id":"PRR-DES-07",...,"owner":"Technical Office Mgr",...}
```

## Deploy Command

```bash
cd /Users/mohamedessa/aseer-museum-pm/06_Risk_System/webapp
bash deploy.sh
```

This runs `build_risk.py` (rebuilds index.html from Excel), copies the Excel to `src/`, and rsyncs to Hostinger.
