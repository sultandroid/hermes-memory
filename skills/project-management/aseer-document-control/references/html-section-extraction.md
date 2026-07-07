# Extracting One-Page Section Summaries from HTML MOS/Plan Documents

Use this when a user asks for a specific section (or a few sections) from a large HTML Method of Statement, Plan, or Report pulled into a single printable page.

Example trigger: *"ok 3.2 Support Equipment and 4. Survey of Surrounding Area / Neighbors in one page"*

## Workflow

### 1. Locate the source HTML

The source is usually a print-formatted HTML export of a Word/PDF document in the project folder, e.g.:

```text
Samaya/Technical Office/Bim Unit/Aseer-Museum/Lidar_Scanning_Services/MOS/MOC-ASEER-SIC-1K0-MOS-001_Rev00_MOS_LiDAR_Survey.html
```

### 2. Find the section boundaries

Use `search_files` with the section heading text. HTML exports often have one `<div class="sheet">` per page, so sections may start mid-page and continue onto the next.

```bash
# Example: search for the target headings
search_files --path "...MOS_LiDAR_Survey.html" --pattern "3\.2 Support Equipment|Survey of Surrounding Area"
```

Read around the match lines with `read_file --offset <start> --limit <lines>` to capture:
- Section heading
- Intro paragraphs
- Tables
- Methodology paragraphs
- Page footer context (doc ref, rev, page number)

### 3. Build a single-page HTML summary

Create a new HTML file with:
- A4 `@page` sizing and print-safe margins
- Samaya header with doc ID and rev chip
- One `<h2>` per extracted section
- Tables copied as-is (cleaned of inline widths if they break layout)
- Footer with project name and "Page 1 of 1"

Keep the language client-facing and aligned with the original document — do not rephrase technical values (resolutions, distances, quantities).

### 4. Name and save

Use the original doc number plus the extracted section numbers:

```text
MOC-ASEER-SIC-1K0-MOS-001_Rev00_Sections_3.2_and_4.html
```

Save it alongside the source MOS in the same folder so folder navigation stays coherent.

### 5. Open for review

Open the file in the browser so the user can view/print/PDF it:

```bash
open MOC-ASEER-SIC-1K0-MOS-001_Rev00_Sections_3.2_and_4.html
```

Or use the browser tool:

```text
browser_navigate file:///Users/.../MOC-ASEER-SIC-1K0-MOS-001_Rev00_Sections_3.2_and_4.html
```

## CSS pattern for a one-page A4 sheet

```css
@page { size: A4; margin: 12mm; }
.page {
  width: 210mm;
  min-height: 277mm;
  max-height: 277mm;
  padding: 12mm;
  margin: 0 auto;
  overflow: hidden;
}
```

Use compact tables and small font sizes (8.5–9.5 pt) so two sections fit on one sheet.

## Pitfalls

- **Large HTML files may fail `read_file`.** If the full read is interrupted, fall back to `search_files` to find headings, then `read_file` with a tight offset/limit.
- **Section spans multiple pages.** Read far enough past the heading to capture continuation tables/paragraphs on the next "sheet" div.
- **Preserve units and tolerances.** Do not round or reformat values like "1/4 (6.1 mm @ 10 m)" or "8–12 m intervals".
- **Keep doc number conventions.** If the source uses `— · Rev 00` because the DC has not assigned a number yet, keep the em dash; do not invent a doc number.
- **One-page means one physical page.** If the content overflows, split into two pages or ask the user which section to drop — do not silently shrink text to illegibility.
