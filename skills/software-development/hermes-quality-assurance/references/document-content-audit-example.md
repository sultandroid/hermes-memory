# Document Content Audit — Worked Example

## Session: QA Audit of Rev 03 Stakeholder Management Plan (2026-07-13)

This reference captures the concrete findings from a real QA audit of a project management plan HTML. Use as a pattern for future document-content audits.

## Source Files Consulted

| File | Path | What It Provided |
|------|------|------------------|
| SMP HTML | `03_Plans/02_Stakeholder/MOC-ASEER-SIC-1K0-PL-0020_Rev03_Stakeholder_Management_Plan.html` | The document under audit |
| Specialist Register | `Technical_Office/Specialist_Management/specialist_register.md` | Tier 1-3 personnel with roles, status, MoC approval |
| Resource Management Plan | `03_Plans/10_Resource/resource_management_plan.md` | Key Personnel table with names and roles |
| PROJECT_MEMORY.md | `99_Archive/00_Project_Overview/PROJECT_MEMORY.md` | Org chart, latest updates, critical issues |

## Audit Techniques Used

### Extracting Personnel Names from HTML

The HTML was too large (294KB, 2511 lines) for a single `read_file()`. Used `search_files()` with targeted regex patterns:

```python
# Pattern 1: All named individuals
grep -E 'Eng\. |Dr\. |Muhammad |Hani |Maged |Mohamed |Mansour |Sundus |Yasser |Anwar |Hossam |Jim |Francesco |Joshua |Robin |Katica |Emmy |Julie |Al Zeeny|Shehab|Mutai|Rashad|Maher|Fida|Samir'

# Pattern 2: Specific known personnel
grep -E 'Sultan Issa|Mohamed Samir|Ahmed Salah|Hesham Abdel|Mohamed M\. Ibrahim|Ahmed Gad|Salah Eldin|Asad Ullah|Mohamed Farouk|Mohamed Elbaz|Maged Zamzam|Mansour|Sundus|Yasser|Anwar|Hossam'
```

### Checking Forbidden References

```python
# Zero-tolerance check
for ref in ['Adel Darwish', 'Sustainability Manager', 'Abdelmohaimen Medhat', 'Ahmed Albahrawi']:
    count = grep -c ref in HTML
    # Zero = pass. Non-zero = flag with line number.
```

### Verifying Page Count Consistency

```python
# Extract all page number markers
grep -o 'PAGE [0-9]* / [0-9]*' file.html
# Check: do all footers use the same denominator?
# Check: does TOC header match footer denominator?
```

### Checking Revision Number Consistency

```python
# Check cover page
grep 'REV 03\|Rev 03' file.html
# Check for wrong revision artifacts
grep 'REV 04\|Rev 04' file.html
```

## Findings Summary

| Category | Issues Found |
|----------|-------------|
| Broken assets | 5 logo PNGs missing, 28 broken references |
| Revision mismatch | "REV 04" in 2 places (should be Rev 03) |
| Page count | TOC says 24, document has 23 |
| Personnel mislabel | Eng. Mohamed Sultan called "Project Manager" — is Technical Office Manager |
| Missing roles | Project Manager and Technical Office Manager absent from T1 register |
| Ambiguous approver | "Darwish" used — conflicts with Waris Sultan as PD |
| Internal note leak | "Medhat left 15-Jun" visible to CG |
| Tracking labels | "Gap (Rev 00)" / "Closure (Rev 02)" in SVG diagram |

## Key Regex Patterns for Future Audits

```python
# Find all image references
r'src="([^"]+\.(png|jpg|jpeg|svg|gif))"'

# Find all page footers
r'PAGE \d+ / \d+'

# Find revision mentions
r'REV \d+|Rev \d+'

# Find named individuals
r'(Eng\.|Dr\.|Mr\.|Mrs\.|Ms\.) [A-Z][a-z]+ [A-Z][a-z]+'

# Find internal tracking artifacts
r'Gap \(Rev \d+\)|Closure \(Rev \d+\)|TODO|FIXME|NOTE:'
```
