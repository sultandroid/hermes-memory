# ExportMailIn Attachment Routing — Aseer Museum

Workflow for routing attachments extracted by ExportMailIn (staged in `/tmp/email_attachments/`) to the correct Aseer Museum project folders and updating repo registers.

## Source

ExportMailIn extracts email attachments to `/tmp/email_attachments/` with filenames in the format:
```
{email_id}_{original_filename}
```
e.g. `48614_MOC-MUS-CG-ASE-1KN-SE-021.pdf`

## Destination Structure

The Aseer Museum OneDrive lives at `/Volumes/MIcro/Work/Aseer-Museum/`. Key subdirectories:

| Destination | Contents |
|-------------|----------|
| `00_Contracts/Invoices/` | Invoices (INV-*) |
| `00_Status/` | Daily reports, weekly dashboards |
| `02_Submittals/01_DD_Gate/{Discipline}/` | Design Gateway submittals (1G-*) |
| `04_Docs/02_Plans_and_Procedures/{Category}/` | Plans, procedures, ZD documents |
| `24_Subcontractors/00_Prequalification/{Specialty}/` | Prequalification docs (PQ-*) |
| `24_Subcontractors/{Specialty}/08_RFP_and_Proposals/` | Proposals, RAR archives |

## Routing Logic

Parse the document ref from the filename to determine destination:

| Ref Pattern | Discipline | Destination |
|-------------|------------|-------------|
| `-1A0-` | Architecture | Architecture/ |
| `-1C0-` | Structural/Civil | Structural/ or Laboratory/ |
| `-1E0-` | Electrical/AV | Electrical/ |
| `-1K0-` | General/Integration | General/ |
| `-1KH-` | HSE | 02.5_HSE_Plan/ |
| `-1L0-` | Landscaping | Landscaping/ |
| `-1M0-` | MEP/Mechanical | MEP/ |
| `-MEP-` | MEP (cross-discipline) | MEP/ |

| Doc Type | Subfolder |
|----------|-----------|
| `-PQ-` | Prequalification → `24_Subcontractors/00_Prequalification/{Specialty}/` |
| `-1G-` | Design Gateway → `02_Submittals/01_DD_Gate/{Discipline}/` |
| `-ZD-` | General Document → `04_Docs/02_Plans_and_Procedures/{Category}/` |
| `-PL-` | Plan → `04_Docs/02_Plans_and_Procedures/{Category}/` |
| `-SE-` | Safety Instruction → `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/` |
| `INV-` | Invoice → `00_Contracts/Invoices/` |
| `Daily_Report` | Status → `00_Status/` |
| `Technology BOQ` | General → `04_Docs/02_Plans_and_Procedures/General/` |
| `.rar` / `.zip` | Proposal archive → `24_Subcontractors/{Specialty}/08_RFP_and_Proposals/` |

## Register Updates

After routing files, update these registers in `~/aseer-museum-pm/01_Registers/`:

| Register | When to Update |
|----------|----------------|
| `prequalification_register.md` | New PQ-* files routed |
| `submittal_register.md` | New 1G-* (DD Gate) or IFC submittals routed |
| `ncr_register.md` | New NCR or SE (Safety Instruction) files — check if already tracked |
| `risk_register.md` | New risk plan documents — auto-generated from `06_Risk_System/risks.json`, do not edit directly |

### Prequalification Register Format

Append rows at the end:
```
|| {seq} | {ref} | {disc} | {scope} | {vendor} | {date} | {status} | {notes} |
```

### Submittal Register Format

Append rows to the "Recent / Active Submittals" table:
```
|| {ref} | {subject} | {discipline} | {date} | {response} | **{code}** | {notes} |
```

## Review Log

After each routing run, create a review log at:
```
~/aseer-museum-pm/03_Plans/08_Risk/reviews/email_scan_{YYYY-MM-DD}.md
```

Include:
- YAML frontmatter (last_updated, owner_agent, status, source)
- Summary of files processed
- File-by-file routing table
- .eml files (forwarded emails not routed as documents)
- Register update notes
- Any flagged items

## .eml Files

.eml files are forwarded emails, not documents. Do not route them to project folders. Flag them in the review log for manual review — the actual attachment may be embedded inside the .eml and needs Outlook to extract.

## Pitfalls

- **Sibling agent conflicts**: Another agent may have already updated registers between your scan and your write. Re-read before patching.
- **Duplicate files**: Many files may already exist in the destination (same size). Skip them — don't overwrite.
- **replace_all in patch**: Using `replace_all=True` on a table row that appears multiple times (e.g. acoustic entries) will duplicate content. Use unique context strings instead.
- **OneDrive macOS metadata**: `.` prefixed files (e.g. `._48530_INV-4863.pdf`) are macOS resource fork artifacts — ignore them.
- **Risk register**: Do NOT edit `risk_register.md` directly. It is auto-generated from `06_Risk_System/risks.json`. Update the JSON instead.
