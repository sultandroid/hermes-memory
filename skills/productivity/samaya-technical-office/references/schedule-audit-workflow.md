# Schedule Audit Workflow — Primavera P6 Programme Review

When the Technical Office receives a contractor Primavera P6 schedule (XER/PDF export) for review, follow this progressive deep-dive audit pattern.

## 1. Intake & Extraction

```bash
# PDF export (Gantt chart)
pdfinfo "schedule.pdf"                     # pages, size, rotation
pdftotext -layout "schedule.pdf" "/tmp/sched.txt"

# XER native — requires P6 or a viewer
# XML export can be parsed with xml.etree.ElementTree
```

Key metadata to capture: title, author, creation date, page count, page size (A3 = Primavera default), total duration, start/finish dates.

## 2. Rapid WBS Scan

Read first 50-100 lines to establish:
- Project title and start date
- Top-level WBS structure (Milestones, Preliminaries, Engineering, Procurement, Construction, T&C)
- Contract milestone dates (MS1000 signature, MS1010 design complete, MS1020 project completion)
- Total float range — identify 0-float (critical path) items

## 3. Progressive Deep-Dive Audit Pattern

Do NOT dump every finding at once. Follow the user's iterative pattern:

### Pass 1 — Overall Schedule Health
- Structure, logic, completeness, calendar, total duration
- Flag: unapproved start date, missing milestones, unrealistic day-1 starts
- Output: structured findings with severity (HIGH/MEDIUM/LOW) + recommendation

### Pass 2 — Targeted Phase (user directs focus)
- Extract activities for one WBS branch (e.g., Design, Procurement, Construction, Handover)
- Analyze float distribution, dependencies, resource concurrency
- Flag: parallel phases without reviews, client-dependent activities on day 1, compressed durations

### Pass 3 — Specific Package Table (e.g., Stage 3 Materials)
- List all items with activity IDs, durations, float
- Cross-reference against project BOQ, Materials Register, Floor Finishing Detail

## 4. Cross-Reference Project Data Sources

| Source | Location | What It Has |
|--------|----------|-------------|
| Materials & Subcontractor Register | `B.O.Q/Materials & Subcontractor Register (Master).xlsx` | Material descriptions, categories, specs |
| Floor Finishing Material Detail | `B.O.Q/Floor-Finishing-Material-Detail.xlsx` | Supplier/brand names for all floor/wall finishes |
| Procurement Tracker | `B.O.Q/Copy of Procurement Tracker.xlsx` | Pre-qual status, AV items, subcontractor list |
| NRS Exhibition Schedules | `Design Files/Package_Part 2/.../Xcel/` | 21 schedule files with named suppliers (Ceramiche Piemme, Concept Tiles, Domus, Tarkett, etc.) |

Workflow for brand-name extraction:
1. Read schedule Stage 3 materials table → extract generic material names
2. Open Floor Finishing Detail → match by description → extract supplier
3. Open Materials Register → search for matching material → extract spec/brand
4. Open Procurement Tracker → search AV rows → extract equipment details
5. Compile into single table with columns: ID, Discipline, Material, Design Spec, **Supplier/Brand**, Source, Dates, Float, Critical

## 5. Output Formats

### HTML Review Report (preferred for formal issue)
- Cover page: dark navy, project info, doc ref, revision
- Executive summary with severity count cards
- Findings table with ref/severity/title/observation/requirement/reference
- Recommendation box (qualified acceptance / reject / conditional)
- Distribution list

### Excel Extraction (for detailed tabulation)
- Discipline-organized sheets
- Column widths: Material (45), Supplier (35), Source (28)
- Critical-path items highlighted in red (`#FEF2F2`)
- Auto-filter enabled
- Freeze header row

## 6. Finding Taxonomy

| Severity | Label | When to Use |
|----------|-------|-------------|
| HIGH | Requires resolution before baseline approval | Unapproved start date, client dependency on day 1, zero-float handover, no supply chain buffer |
| MEDIUM | Requires response in next revision | Resource loading missing, concurrent trades not justified, late-start COBie |
| LOW | Informational / minor gap | Missing milestone date, calendar not verified, no testing activity for a system |
| INFO | Observation, no action required | Significant float on non-critical path, well-structured section |

## 7. Typical Findings for Museum Fit-Out Schedules

- **Day-1 start assumption** — surveys, 3D shot, design all start on contract date. Client content (text, imagery, copyrights) assumed available day 1. Flag as HIGH.
- **50/90 design overlap** — standard fast-track but rework risk if 50% review generates major comments.
- **Overseas supply chain** — manufacturing + shipping + customs with no buffer. Add minimum 2-week buffer before installation.
- **Four-floor concurrency** — all levels start within 14 days. Request resource-loaded programme.
- **Zero-float handover** — TOC the day after final acceptance. Request 10-day minimum buffer.
- **COBie/BIM late start** — progressive submissions during construction, not 10-day window at end.
- **Missing system testing** — IT/Network/AV often lack explicit testing activities.

## Pitfalls

- **Schedule activity names are generic** — P6 Primavera exports use material category names, not supplier brands. Cross-reference against BOQ/Finishing Detail/Materials Register to find actual brands.
- **PDF extraction loses P6 logic** — `pdftotext -layout` preserves tabular structure but loses predecessor/successor relationships. For dependency analysis, request native XER or XLSX export.
- **Header repeats every page** — when searching for a specific activity, skip the repeated header rows (every 30-50 lines) by filtering out lines starting with "Actual Level" or "Oracle Corporation".
- **Page rotation** — A3 landscape PDFs are rotated 90°. pdftotext handles this automatically.
- **Calendar not visible in export** — P6 PDF exports don't show the calendar configuration. Always ask separately: working days, holidays, Saudi weekends (Fri-Sat).
- **Don't auto-open files after edits** — user refreshes manually.
