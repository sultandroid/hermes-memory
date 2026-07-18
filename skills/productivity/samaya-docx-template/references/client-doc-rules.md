# Client-Facing Document Rules

## § symbol — banned everywhere
Never use § in any format (DOCX, Excel, HTML, MD). Write "Section 2.1" or "Sec. 2.1".

## Internal references — strip from client docs
- No file paths (OneDrive, repo paths, `01_Registers/...`)
- No markdown references (`.md` file names)
- No repository references ("project repo", "github")
- No internal tracking artifacts ("format revision" in revision history, "agent SoT")

Replace with client-appropriate descriptions:
- "Project Risk Register (PRR)" not "01_Registers/risk_register.md"
- "Project Document Control" not "OneDrive - 04_Docs/..."

## Revision history — client language only
Describe what changed from the client's perspective:
- ✅ "REV00 - First issue for CG review"
- ✅ "Updated risk counts from design, procurement, site, and HSE departments"
- ❌ "Format revision — unified table styles, halftone remarks, page breaks, removed internal references"

## Table uniformity
ALL tables in a document must have the SAME style: navy header, alternating rows, cantSplit on every row, proportional column widths.

## Excel registers
Must be formula-based with dropdowns, not hardcoded values. Score = P×S formula, Rating = IF formula, Response Strategy = dropdown list.

## Fix existing files
When the user asks to fix formatting, edit the existing file — do not recreate from scratch. This preserves manual edits the user made in Word/Excel.
