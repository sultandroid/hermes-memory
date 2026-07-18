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
