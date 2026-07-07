# CG Schedule/Register Processing

Used when CG sends an Excel/PDF schedule (object schedule, drawing register, submission plan) that needs to be extracted, analyzed, and routed to the design team.

## Workflow

### 1. Extract & Map
- **Excel schedules**: Use `openpyxl` to read sheets, find header rows by scanning for known column names (`Object ID`, `Showcase ID`, `Showcase needed`, etc.)
- **PDF schedules**: Use `pdftotext -layout` for text extraction; use regex for structured data (e.g. `\bOB\d+(?:_\d+)?\b` for object IDs)
- Build a clean mapping table: object → showcase → gallery → status
- Save as a formal Excel with 3 sheets: (1) full mapping, (2) summary, (3) action items

### 2. Version Comparison
- Compare against the previous version of the same schedule (check file dates, revision numbers in headers)
- Identify:
  - **New objects** (in new, not in old)
  - **Removed objects** (in old, not in new)
  - **Reassigned objects** (different showcase/gallery)
  - **Split objects** (e.g. OB225 → OB225-1, OB225-2)
  - **Unassigned objects** (in schedule but no showcase ID)
- Flag any "CANCELED", "OBJECT CUT", or "TBC" markers

### 3. Gap Analysis
- Check which galleries/areas have complete mapping vs missing
- Check for contradictory notes (e.g. "selected" and "removed" on same object)
- Check for missing dimensions, weights, or images
- Check for color coding violations (revisions not highlighted per schedule's own key)

### 4. Multi-Party Routing (Single Email Pattern)
Draft ONE email addressed to all relevant parties with a responsibility table:

| Party | Action Required |
|-------|----------------|
| **NRS** (Jim/Robin) | Design updates, wall/platform design, installation sequence |
| **Glasbau Hahn** (Yara) | Structural feasibility, base load, dimension confirmation |
| **Structural Engineer** | Load calculations, anchoring, installation logistics |

**Email structure:**
1. Brief intro referencing CG's email
2. What's included (file list)
3. Key changes from previous version (bullet points)
4. Study requests / action items (table per party)
5. Additional requests (e.g. dimension confirmation)

**CRITICAL: Check SOW before asking scope questions.** Before routing CG comments to a subcontractor:
- Read their SOW/contract first to determine what's in their scope
- If the item IS in their scope → ask for timeline/dates only, not scope confirmation
- If the item is NOT in their scope → identify the correct party yourself, don't ask the wrong sub
- Never ask "is this in your scope?" in the routing email — that's your job to determine
- Frame as: "Please review and suggest proposed dates" not "please confirm if this is in your scope"

### 5. Decide Whether to Query CG
Before forwarding to the design team, check if the schedule is complete:
- If entire galleries are missing showcase assignments → **query CG first** before routing
- If minor TBC items exist → proceed and flag in the email
- If contradictory notes exist → query CG for clarification

**Query CG template:**
> Dear [Name],
>
> Thank you for the [schedule name]. We note that [N] objects across [galleries] are listed but have no [Showcase ID / mapping] assigned yet. Only [mapped areas] are complete.
>
> When will the remaining assignments be provided? This will help us proceed with the full design without rework later.
>
> Regards,
> Sultan

### 6. Handle Designer Pushback
When the design team (especially NRS) responds with concerns:

| Concern | Response |
|---------|----------|
| "Too late for changes" | Acknowledge, forward to CG, request additional fees discussion |
| "Schedule is unclear/contradictory" | Arrange curator meeting, ask CG for definitive list |
| "Objects won't fit" | Flag to CG with specific dimensions, request grouping guidance |
| "Additional work required" | Support additional fees claim, document scope changes |
| "Missing information" | Track what's missing, escalate to CG |

**Key NRS pushback patterns (Jim Richards):**
- Will flag every inconsistency in the schedule (color coding, missing IDs, contradictory notes)
- Will request a meeting with curators before proceeding
- Will claim additional fees for scope changes
- Will provide specific dimension/weight data from their analysis
- Expects a "definitive and clear" list before doing design work

## File Organization

**Preferred path** (OneDrive BIM):
```
02_Submittals/01_Shop Drawings/1.01 [Category] Shop Drawings/[Date]_[Description]/
```

**Secondary path** (Document Control):
```
04_Submittals/[Category]/[Date]_[Description]/
```

Always use the OneDrive BIM path as primary. The Document Control folder is a working copy.

## Excel Formatting Standards

Formal Excel output should have:
- **Title row**: Dark blue fill (`1F3864`), white bold Calibri 14pt
- **Subtitle row**: Medium blue fill (`2F5496`), white Calibri 10pt
- **Header row**: Medium blue fill, white bold Calibri 10pt
- **Gallery section dividers**: Light blue fill (`D6E4F0`), dark blue bold text
- **Data rows**: Alternating white/light gray (`F2F2F2`)
- **Status colors**: Green (`548235`) for Available, Amber (`BF8F00`) for TBC/Needs Sourcing
- **Action notes**: Red (`C00000`) for cancellations, Orange (`ED7D31`) for study requests
- **Freeze panes** below header row
- **Auto-filter** on all columns
- **Landscape print layout**, fit to width

## Pitfalls
- CG schedules often have **incomplete mapping** — always check for unassigned objects before routing
- Old schedules may use different object ID formats (OB225 vs OB225-1, OB227 vs OB227_1-17)
- PDF schedules from the old package may have different revision dates than the new Excel — always compare
- The "Showcase Schedule" PDF (dimensions/specs) is a separate document from the "Object Schedule" (object-to-showcase mapping) — don't confuse them
- CG's color coding key (highlights changes, removed items, added items) is often not followed in the actual data — flag this
- NRS will push back on late changes — expect additional fees discussion
- Some objects may be marked "CANCELED" or "OBJECT CUT" in the schedule — these are CG's internal markers, not final decisions
