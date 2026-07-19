# Client-Facing Document Rules

## No Internal References

The client cannot access your repo, OneDrive paths, or markdown files. Never reference:
- File paths (`01_Registers/risk_register.md`, `03_Plans/08_Risk/`)
- "project repo" or "repository"
- Markdown format
- Internal tooling or agent references

Replace with generic descriptions: "Project Risk Register (PRR)", "Risk Management System", "Project Document Control".

## Revision History — Client-Appropriate Language

The revision history table is for the client, not for internal notes. Never include:
- "Format revision — unified table styles, halftone remarks, page breaks, removed internal references"
- Any description of formatting changes, tooling, or internal process

Instead write:
- "REV00 - First issue for CG review"
- "Updated risk counts from design, procurement, site, and HSE departments"
- "Revised scoring methodology per project requirements"

## No AI Symbols

Replace all typographic symbols with plain ASCII:
- Em dash (—) and en dash (–) -> hyphen (-)
- Section symbol (§) -> "Section" or just section number
- Middle dot (·) -> bullet or hyphen
- Curly quotes -> straight quotes

**The user will call you out on § symbols specifically.** Scan every document before delivery.

## Write Like an Engineer

Bad (verbose AI tone):
"This Risk Management Plan defines the systematic framework for identifying, analysing, responding to, monitoring, and controlling risks throughout the project lifecycle."

Good (direct human tone):
"This Risk Management Plan defines how risks are identified, assessed, and managed on the project."

Principles:
- Cut filler words: "systematic framework", "robust", "proactive", "comprehensive", "streamline", "leverage", "facilitate"
- One sentence per idea. Two max.
- Use active voice
- Start sections with the point, not a throat-clearing intro
- Every claim must trace to an approved project source (ER/SoW/CG comment/submittal) - never cite external standards

## DC Block — First Page

Place after cover metadata, before revision table:
- QC table with columns: (blank) | Prepared by | Reviewed by | Approved by
- Use actual names (Eng. Mohamed Sultan, Eng. Waris Sultan, Eng. Adel Darwish), not role titles
- Navy header row, alternating body rows

## Revision Table — First Page

Place after DC block:
- Columns: Version | Date | Author | Changes
- REV00 entry: "REV00 - First issue for CG review" (no internal formatting details)

## Live Register Notes

After any table showing register data, add halftone (9pt #64748B):
"Data shown is a snapshot from the live Project Risk Register, which is the authoritative source and updated weekly."

## Severity Schedule Thresholds

Align to project remaining duration. For ~10-week project:
- Low: <1 week
- Medium: 1-2 weeks
- High: 2-4 weeks
- Very High: >4 weeks

## Excel Register Template

All register sheets must share IDENTICAL template:
- 14 columns: ID, Category/Discipline, Risk Event, Cause/Hazard, Impact/Consequence, Probability, Severity, Score (formula), Rating (formula), Response Strategy (dropdown), Mitigation/Controls, Risk Owner, Target Close, Status
- Same column widths, same header style (navy), same body font (Calibri 9pt)
- Score = P x S formula
- Rating = IF(score>=threshold, "Critical", ...) formula
- Response Strategy = dropdown: Avoid, Transfer, Mitigate, Accept (Active), Accept (Passive), SOW-Protect
- Auto-filter on all columns, frozen header row
- Dashboard with formula-linked metrics (COUNTA/COUNTIF to PRR sheet)
