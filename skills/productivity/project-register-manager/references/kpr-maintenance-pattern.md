# KPR Maintenance Pattern — Aseer Museum (June 2026)

## End-to-End Workflow

### Trigger
User asks to "update registers", "check stakeholders from emails", "update KPR", or "map Appendix B".

### Phase 1: Email Sweep
1. Search Outlook SQLite for all relevant emails by:
   - Role titles (Project Director, QA/QC, MEP, etc.)
   - Company names (ZNA, Rawasen, AD Engineering, Lumotion, etc.)
   - Document codes (PQ-0097, ZD-0056, ZD-0058, etc.)
   - Keywords (appointed, nominated, CV, prequal, Code B, Code C, rejected, left, resigned)
2. Cross-reference with Email_Archive markdown files for already-processed summaries
3. Extract: appointment status, approval date, CG code (A/B/C/D), contact details

### Phase 2: Read Current Registers
1. Read KPR Excel (all 3 sheets: Cover, Key Personnel, Summary)
2. Read Stakeholder Register Excel (if exists)
3. Read PROJECT_MEMORY.md stakeholder section
4. Note: Do NOT trust CV filenames as proof of appointment

### Phase 3: Cross-Reference & Classify
For each Appendix B requirement, classify as:

| Category | KPR Placement | Examples |
|----------|--------------|----------|
| Samaya internal | Main section, Tier 1 | PM, BIM Manager, QA/QC, HSSE, Site Manager, Factory staff |
| Samaya hires | Main section, Tier 2 | Structural, MEP, AV, Lighting, FLS, Showcases, Landscaping, Acoustic |
| Samaya must appoint | Main section with note | ITCA (independent agent per ER) |
| Authority / Statutory | **Separate section** | SEC, MOI, CITC, Municipality — not Samaya hires |

### Phase 4: Determine Designer vs Contractor/Installer Split
For each package, ask or check meeting records:

| Pattern | Meaning | Example |
|---------|---------|---------|
| **Combined** | One entity does design + supply + install | Samaya Graphit, Glasbau Hahn, Samaya Factory Rep. Dept |
| **Split** | Designer different from installer | ZNA (lighting design) vs M&E Contractor (fixture install) |

Never assume — the user will correct if wrong.

### Phase 5: Update Registers (Ordered)
1. **KPR** — Update names, statuses, dates, notes, tier classifications
2. **Cover sheet** — Bump revision, update date
3. **Summary sheet** — Verify formulas match current status granularity
4. **Stakeholder Register** — If it has project role/contact columns, update those
5. **PROJECT_MEMORY.md** — Add departure/appointment notes
6. **Odoo Task 3211** — Update description with classification map

### Phase 6: Formatting Preservation (CRITICAL)
- NEVER rebuild an Excel file from scratch
- Always copy values into the existing formatted template
- Check for images/logos (.images attribute) before and after
- Verify Cover sheet merge cells are intact

## Known Status Categories for KPR Summary

| Summary Row | Formula Pattern |
|-------------|----------------|
| Approved | `COUNTIF(StatusRange, "*Approved*") + COUNTIF(StatusRange, "*Code B*")` |
| Pending / Not Yet Approved | `COUNTIF(StatusRange, "*Pending*") + COUNTIF(StatusRange, "*prequal*") + COUNTIF(StatusRange, "*nominated*")` |
| Not Yet Appointed / Vacant | `COUNTIF(StatusRange, "*Not yet*") + COUNTIF(StatusRange, "*Vacant*")` |
| Code C - Needs Revision | `COUNTIF(StatusRange, "*C -*") + COUNTIF(StatusRange, "*Revise*")` |
| Statutory / Authority | `COUNTA(NameRange)` for separate section |

## Verification Checklist
- [ ] All names backed by email evidence (not CV filenames)
- [ ] Approval dates from actual CG response emails
- [ ] No authority rows mixed in main section
- [ ] Designer/Installer split documented in Notes column
- [ ] Summary formulas match current statuses
- [ ] Cover revision bumped
- [ ] Odoo task description updated
- [ ] PROJECT_MEMORY.md updated

## Pitfalls Specific to KPR Work
- **Excel row deletion**: Delete in REVERSE order (highest row number first) when deleting multiple rows
- **OneDrive stubs**: Check file is valid ZIP before openpyxl.load_workbook()
- **File open in Excel**: Ask user to close before writing, or verify after write by re-reading
- **Subagent rebuilds**: Subagents will rebuild from scratch and destroy formatting — do NOT delegate full Excel rebuilds
