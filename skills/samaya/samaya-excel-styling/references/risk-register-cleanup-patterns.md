# Risk Register Cleanup Patterns — Aseer Museum

## Removing AI/Repo/Automation References from Excel

When cleaning a risk register xlsx for CG submission:

### Cover Sheet Notes
Replace automation references with clean project notes:
- Remove: "Source of truth: 06_Risk_System/risks.json", "Auto-synced by risk_sync.py", "01_Registers/risk_register.md"
- Replace with: "RMP (PL-02.17 REV00) submitted to CG [date]. This register is the live project file."
- Keep: handover date, append-only rule, PM instructions

### Register Control — Author Column
Replace all AI model names with role titles:
- Hermes, Claude, Grok, Kimi, OpenCode → Technical Office
- risk_sync.py → Technical Office
- BIM Unit → Technical Office

### Register Control — Sources
Replace repo/automation sources with actual project documents:
- Remove: GitHub repo URLs, JSON SoT references, sync script mentions
- Replace with: RMP doc number, RBS appendix, MoM references, CG correspondence, NCR register, DRR

### RBS Sheet
After copying data from another workbook, check for duplicate rows (same code appearing twice). Clear the duplicate.

### Dashboard
Dashboard should reflect only the master project risk register (PRR). DRR and HSE are working registers with different scoring scales — keep them in separate sheets, not mixed into dashboard charts.

## Scoring Scale Separation

| Register | Scale | Range | Severity Bands |
|----------|-------|-------|----------------|
| PRR (Master) | P×S 1-4 | 1-16 | Critical ≥12, High 8-11, Medium 4-7, Low ≤3 |
| DRR (Design) | P×S 1-5 | 1-25 | Critical ≥16, High 10-15, Medium 5-9, Low ≤4 |
| HSE | C×L 1-5 | 1-25 | Critical ≥16, High 10-15, Medium 5-9, Low ≤4 |

Never merge registers with different scoring scales into one sheet. Use separate sheets with their own scoring headers.

## Dynamic Formulas — Never Hardcode

### RBS COUNTIF
```python
PRR_SHEET = "'Risk Register'"
ws.cell(row=r, column=3).value = f'=COUNTIF({PRR_SHEET}!C{DS}:C{DE},"{code}")'
```

### Dashboard COUNTIF
```python
ws.cell(row=row, column=2).value = f'=COUNTIF({PRR_SHEET}!J{DS}:J{DE},"{sev}")'
ws.cell(row=r, column=5).value = f'=COUNTIF({PRR_SHEET}!C{DS}:C{DE},"{code}")'
```

### Scoring Matrix with Hidden Reference Cells
```python
# Row 4: hidden S values (1,2,3,4 in B4:E4)
ws.cell(row=4, column=2, value=1).font = Font(size=1, color=WHITE)
# Column F: hidden P values (4,3,2,1 in F6:F9)
ws.cell(row=r, column=6, value=p_val).font = Font(size=1, color=WHITE)
# Formula: =F{r}*{col_letter}$4
cell.value = f'=F{r}*{col_letter}$4'
```

## Dropdowns on All Controlled Columns

Clear old validations first, then add DataValidation for each controlled column.

### Risk Register Dropdowns
- Category (C): APP,AV,CNS,COM,CON,DES,FLS,HSE,LOG,MEP,OPS,PRC,QLT,SCH,SEC,SIT,STK,TCH
- Probability P (G): 1,2,3,4
- Severity S (H): 1,2,3,4
- Response Strategy (K): Avoid,Transfer,Mitigate,Accept (Active),Accept (Passive),SOW-Protect
- Status (M): Open,Watch,Mitigated,Closed,Superseded

### DRR Dropdowns
- RBS Category (C): SCH,TEC,PRO,EXT,QA,COM
- Prob (G): 1,2,3,4,5
- Impact (H): 1,2,3,4,5
- Response Strategy (K): same 6 options
- Status (N): Open,Watch,Mitigated,Closed,Superseded

### HSE Dropdowns
- Consequence C (E): 1,2,3,4,5
- Likelihood L (F): 1,2,3,4,5
- Residual C (H): 1,2,3,4,5
- Residual L (I): 1,2,3,4,5
- Status (M): Ongoing,Completed,Pending,Not Required

## HSE Severity Coloring

Both Init Score (col 7) and Res Score (col 10) need severity colors using HSE scale:

```python
def hse_severity(score):
    if score is None: return None
    try: s = int(score)
    except: return None
    if s >= 16: return 'critical'
    if s >= 10: return 'high'
    if s >= 5: return 'medium'
    return 'low'
```

## Sheet Ordering

Always order: Cover → Dashboard → Scoring Matrix → RBS → Risk Register → DRR → HSE

```python
desired = ['Cover', 'Dashboard', 'Scoring Matrix', 'RBS', 'Risk Register', 
           'Designer Risk Register (DRR)', 'HSE Risk Register (Fit-Out)']
for i, name in enumerate(desired):
    if name in wb.sheetnames:
        idx = wb.sheetnames.index(name)
        if idx != i:
            wb.move_sheet(name, offset=i - idx)
```

## Remove Register Control Sheet

The user does not want a revision history sheet. Delete it from the final file.

```python
if 'Register Control' in wb.sheetnames:
    del wb['Register Control']
```

## Construction Stage Register — Separate Sheet, RMP-Compliant

When the old consolidated register has a Construction Stage sheet with site-level operational risks (C-001 to C-040):

1. **Add as a separate sheet** — do NOT merge into the master register. Construction risks are site-level operational items (labor, equipment, weather, theft, scaffolding) — different audience and review frequency from strategic master risks.
2. **Place between DRR and HSE** in the sheet order.
3. **Convert to RMP-compliant scoring** — the old sheet uses text labels only (High/Medium/Low/Very High). Convert to numeric P(1-4) x S(1-4) with formula-driven PxI and Severity per RMP bands.
4. **Add Source and Linked PRR columns** — every Aseer-specific risk must reference its source document (SI, NCR, MOM) and linked PRR.
5. **Style consistently** — navy headers, severity colors, freeze panes, auto-filter.

### Text-to-numeric mapping

```python
text_to_num = {'low': 1, 'medium': 2, 'high': 3, 'very high': 4}
```

### Aseer-specific risks

Replace generic template risks with real project risks sourced from SIs, NCRs, and MOMs. Each Aseer-specific risk must have:
- Source document reference (e.g. SI-14, NC-1F0-007)
- Linked PRR cross-reference
- Numeric P and S scores based on actual project conditions

## Date Identified and Last Review Columns

The Risk Register must include Date Identified and Last Review columns. Best practice:

| Column | Placement | Content |
|--------|:---------:|---------|
| Date Identified | After Risk ID (col C) | When the risk first became apparent, not when formally added |
| Last Review | After Status (col O) | Updated to current date on every review cycle |

### Date mapping logic

For a project at day 189, risks should date back to the period when they first emerged, not just the current revision:

```python
# Feb 2026 — early project risks (mobilisation, permits, programme, commercial)
feb_risks = ['PRR-APP-01', 'PRR-APP-02', 'PRR-COM-01', 'PRR-SCH-01', ...]
# Mar 2026 — design risks, EOT claim
mar_risks = ['PRR-DES-01', 'PRR-FLS-01', 'PRR-MEP-01', 'PRR-COM-05', ...]
# Apr 2026 — procurement risks
apr_risks = ['PRR-PRC-01', 'PRR-PRC-02', 'PRR-AV-01', ...]
```

## OneDrive Write Pattern — /tmp First, Then Copy

OneDrive **reverts direct writes** to files inside the sync folder. If you write to a OneDrive path with openpyxl and immediately re-read it, the old version may still be there. This causes the user to see the old file even though your script reported success.

### Correct write pattern

```python
import shutil

# Step 1: Copy the original to /tmp
shutil.copy(onedrive_path, '/tmp/workbook_backup.xlsx')

# Step 2: Open and modify the /tmp copy
wb = openpyxl.load_workbook('/tmp/workbook_backup.xlsx')
# ... make all changes ...
wb.save('/tmp/workbook_backup.xlsx')

# Step 3: Copy back to OneDrive
shutil.copy('/tmp/workbook_backup.xlsx', onedrive_path)

# Step 4: Verify
wb2 = openpyxl.load_workbook(onedrive_path)
assert 'NewSheet' in wb2.sheetnames  # confirm write took
```

### Wrong write pattern (causes silent reverts)

```python
# NEVER do this — OneDrive may revert the file
wb = openpyxl.load_workbook(onedrive_path)
# ... make changes ...
wb.save(onedrive_path)  # May appear to succeed but OneDrive reverts
```

**Pitfall:** The revert is silent. Your script exits with code 0, the user opens the file, and the changes aren't there. Always verify by re-reading the OneDrive path after writing.

## Risk Review Workflow — Present One by One, Grouped by Phase

When the user asks to review risks, do NOT dump them all at once. Present them one by one grouped by phase, and let the user discuss each risk before moving to the next.

### Phases (for DRR / design risks)

1. **Mobilisation & Contract Basis** — risks 1-9 (kick-off, liability, personnel, PTW)
2. **Existing Records & Surveys** — risks 10-18 (as-built, heritage, structural, MEP, electrical, FLS, IT, NRS stamping)
3. **DD Technical Design & Coordination** — risks 19-42 (Stramp, AV mounting, phase balance, smoke control, cooling, ceiling coordination, humidity, drainage, power, security, harmonics, graphics, lighting, WiFi, BIM, projection, light box)
4. **Critical Design Items** — risks 43-46 (MoC object list, conservation lighting, stamp compliance, NRS comments)
5. **Authority Approvals** — risks 47-53 (statutory review, Stramp rejection, stairs, SEC transformer, MOI security, FLS, CITC)
6. **Design Gates** — risks 54-59 (50% gate, 90% gate, PMC review, statutory float, BIM readiness, revision rounds)
7. **Procurement, Specialist & Mock-ups** — risks 60-71 (MoC vision alignment, interactive safety, showcase capability, model rejection, lighting fixture, AV lead time, Arabic text, patinated brass Oddy, finish matching, material Oddy, mock-up rejection, product compliance)
8. **Construction, Handover & Commercial** — risks 72-79 (catwalk coordination, dust/noise, as-built capture, ITCP failure, scope vs tender, variation dispute, statutory fees, design budget)

### Display format per risk

```
**N. RISK-ID** — Risk event summary
Score: P×I = Score (Severity)
Status: [Open/Watch/Mitigated/Closed]
What it means: [1-2 sentence plain-English explanation]
Linked to: [PRR references]
```

After each risk, wait for the user to respond before showing the next one. Do not auto-advance.

## Audit Checklist Before Finalizing

1. All AI model names removed from Author column → use role titles
2. No repo/JSON/automation references in notes or sources
3. RBS and Dashboard use COUNTIF formulas, not hardcoded numbers
4. Scoring Matrix uses =F{r}*B$4 formulas with hidden reference cells
5. All controlled columns have dropdowns (no free-text)
6. HSE score columns colored by severity
7. Register Control sheet removed
8. Sheets in correct order
9. Samaya logo on Cover
10. Navy headers, striped rows, severity colors on all data sheets
11. Risk IDs are immutable — never change them
12. Severity and PxI are formula-based, never hardcoded
13. Status column color-coded (Red/Orange/Yellow/Green/Grey)
14. Date Identified and Last Review columns present
15. Construction Stage sheet added as separate sheet with RMP-compliant scoring
16. OneDrive writes go through /tmp first, then copy back
17. Every folder audited — at least one document read before deciding to skip
