# PDF Gantt Chart Schedule Audit — Primavera P6 Export

Method for extracting and analyzing project schedules from Primavera P6 PDF exports (multi-page Gantt charts). Complements the XER-based programmatic analysis in `xer-schedule-analysis.md` — use this when the source is a PDF export rather than an XER/XML file.

## When to Use

- User sends a multi-page P6 Gantt chart PDF (37-50 pages typical) and asks "review this schedule", "audit against scope", or "check the programme"
- The PDF contains activity tables + Gantt bars with float values
- Need a schedule health check covering WBS completeness, duration realism, sequencing logic, resource concurrency, procurement buffers, and handover compression
- Cannot get the XER/XML file (common in CG submissions where PDF is the deliverable format)

## Step 1: Extract Text from the PDF

```bash
# -layout preserves column alignment (critical for Gantt charts)
pdftotext -layout "/path/to/schedule.pdf" /tmp/schedule.txt

# Check page count and metadata first
pdfinfo "/path/to/schedule.pdf"
```

Key metadata to note:
- **Title** — often "PM" (Project Management) or the project name
- **Pages** — 37+ is typical for a full project schedule
- **Page size** — A3 (842x1191) is standard for P6 exports; A4 is cramped
- **Rotation** — 90° = landscape orientation
- **Creation date** — revision date of the schedule

## Step 2: Read All Pages in Sections

The PDF is typically 2000-3000 lines of text. Read 200-line chunks:

```python
# After pdftotext, read in 200-line sections
from hermes_tools import read_file
for offset in range(1, total_lines, 200):
    section = read_file(path="/tmp/schedule.txt", offset=offset, limit=200)
    # Process each section
```

Each page repeats the header with project name, column headers, and page number.

### Common Page Footer Pattern (ignore after each page feed):
```
Actual Level of Effort | Remaining Work | Milestone | Page N of 37
© Oracle Corporation
```

The actual content is every line between page headers that starts with an activity ID or indentation.

## Step 3: Map the WBS Hierarchy

P6 Gantt exports use indentation to show WBS hierarchy. Activity ID prefixes reveal scope:

| Prefix | Phase | Typical ID Range |
|--------|-------|-----------------|
| MS | Milestones | MS1000-MS1020 |
| PE | Preliminaries (Permit/Mobilization) | PE1000-PE1030 |
| AS | Assessment & Survey | AS1000-AS1170 |
| EN | Engineering/Design | EN1000-EN1790 |
| PR | Procurement | PR1000-PR6900+ |
| CN | Construction | CN1000-CN3720 |
| TCH | Testing/Commissioning/Handover | TCH1000-TCH1210 |

**Reading the hierarchy:**
- Activities with no indentation = Level 1 (WBS summary)
- Single indent = Level 2 (phase grouping)
- Double indent = Level 3 (discipline/sub-phase)
- Triple indent = Level 4 (activity level with 'Preparation & Submittal' / 'Approvals' sub-groups)
- Leaf activities = individual tasks with ID (EN1000, PR1200, etc.)

### Example WBS from text layout:
```
Engineering                       ← Level 1 (WBS, duration shown inline)
  Design work                    ← Level 2
    3D Shot                      ← Level 3
      Preparation & Submittal    ← Level 3 phase
        EN1000 Prep & Sub of X   ← Level 4 (leaf activity)
      Approvals                  ← Level 3 phase
        EN1010 Approval of X     ← Level 4
```

## Step 4: Extract Key Metrics

### Duration and Dates
The text format is:
```
Activity ID | Activity Name | Original Duration | Start | Finish | Total Float
```

Values are tab-separated in the -layout output. Extract them per activity:

- **Original Duration** — working days (not calendar days)
- **Start/Finish** — format DD-Mon-YY
- **Total Float** — working days; 0 = critical path, positive = slack

### Milestone Analysis
Milestones appear as MS-prefixed activities with 0 duration:
- MS1000 = Contract Signature (project start trigger)
- MS1010 = Completion of Design Phases
- MS1020 = Project Completion Date

Check: are milestones properly dated? Some may show blank dates in extracted text.

### WBS Summary Durations (Top-Level)
Each WBS summary row shows the total duration for that phase in the `Original` column:
```
Engineering        237  01-Dec-25  02-Sep-26   15
Construction       176  02-Mar-26  22-Sep-26    0
Procurement        231  01-Dec-25  26-Aug-26   12
```

The summary row's finish date minus start date = phase float.

## Step 5: Assess Schedule Health (8 Dimensions)

### 1. WBS Completeness
What's covered vs what's missing:

| Phase | Should Include | Red Flags |
|-------|---------------|-----------|
| Preliminaries | Permits, mobilization, site offices | Missing if permit issuance overlaps design work |
| Assessment | Site surveys, structural/MEP/FLS assessment, BIM existing | Any assessment skipped (e.g., BMS) |
| Engineering | 50%/90%/100% design gates per discipline | Missing gates, missing disciplines (e.g., IT/network) |
| Procurement | Supplier prequal, material submittals, purchase orders, manufacturing, shipping, customs | Overseas manufacturing without buffer |
| Construction | Enabling, civil, arch, MEP, AV, showcases per floor | Missing trades or floors |
| Testing & Handover | Commissioning per system, snagging, initial acceptance, TOC | Compressed timeline, zero float |
| COBie/BIM FM | Throughout construction, not end-loaded | Only at final handover |

### 2. Phase Duration Realism

Check each major phase duration against known benchmarks:

| Phase | Museum Fit-Out Benchmark | Aggressive if |
|-------|------------------------|---------------|
| Design (50%→100% IFC) | 3-5 months | <3 months for complex exhibition |
| Procurement (prequal→PO→delivery) | 4-6 months | Overseas supply chain <4 months |
| Construction per floor | 6-10 weeks per floor | <6 weeks full fit-out per floor |
| Testing & Commissioning | 4-8 weeks | <4 weeks for museum-grade MEP+AV |
| Total Project | 12-18 months | <12 months for full museum rehab |

### 3. Float Distribution

Categorize all activities by total float:

| Float Range | Risk Level | Interpretation |
|-------------|-----------|----------------|
| 0 days | 🔴 Critical | Any delay → project completion delayed |
| 1-15 days | 🟠 High | Minor delays from suppliers/weather could slip |
| 16-30 days | 🟡 Medium | Manageable with expediting |
| 31+ days | 🟢 Low | Baseline items; can absorb minor disruptions |

Key check: count how many 0-float activities cluster at project end (testing/handover). The more that end in 0-float, the more fragile the delivery.

### 4. Sequencing Logic

Risk flags in sequencing:
- **Phases starting on Day 0** — site surveys, 3D shot, design all starting on contract day 1 implies no site-access milestone
- **Parallel overlapping** — 50% and 90% design running concurrently is fast-track; risks rework if 50% approvals change 90% direction
- **Assessment-to-demolition gap** — if assessment finishes months before demolition, site conditions may change
- **Floor concurrency** — all floors starting within 2 weeks of each other means resource sharing is impossible; needs double crews
- **Single-threaded testing** — all commissioning in one sequential batch means no partial handover

### 5. Procurement & Supply Chain

Critical checks for overseas procurement:
- **Manufacturing + shipping + customs + site inspection** total duration
- **Any 0-float items** in the supply chain (single supplier failure → delay)
- **Showcase manufacturing** — typically longest lead item (12-16 weeks)
- **First fix dependencies** — does site work wait for materials, or are long-lead items ordered early?
- **Customs clearance** — is there buffer for KSA customs delays?

### 6. Resource & Concurrency Risks

- **Same-trade on multiple floors simultaneously** — can one team install ceilings on 3 floors at once?
- **AV/BMS/IT installation windows** — do they overlap with finishes (dust risk)?
- **Subcontractor peaks** — all mock-up submissions within same 2-week window needs massive review capacity

### 7. Handover & Testing Compression

High-risk indicators:
- Testing duration < 5 weeks for museum-grade systems (MEP + AV + BMS + fire + IT + showcases)
- Snagging and final acceptance < 2 weeks
- Zero float between final acceptance and TOC
- COBie BIM deliverables at project end (should be progressive)
- No defect-liability or training period shown

### 8. Calendar and Holiday Check

- **Weekend model** — Saudi Fri-Sat or KSA government Sat-Wed? Verify P6 calendar matches contract
- **Public holidays** — Ramadan, Eid, National Day should be accounted for in float
- **5-day approval calendar vs 6-day construction calendar** — approval activities spanning a weekend take longer in calendar days

## Step 6: Build the Audit Report

Structure the output:

```markdown
## Schedule Audit — [Project Name] Rev [N]

**Source:** [filename] · [N] pages · P6 PDF Export
**Duration:** [Start] → [Finish] = [N] working days
**Total Float distribution:** 0-days: N | 1-15d: N | 16-30d: N | 31+: N

### Scope Coverage
| Phase | Duration | Float | Assessment |
|-------|----------|-------|------------|
| [Phase 1] | Nd | N-? | ✅/🟡/🔴 + comment |

### 🔴 Critical Risks (will delay project if unmanaged)
1. Risk description — root cause — impact if realized

### 🟠 High Risks (likely to cause issues)
1. ...

### 🟡 Medium Observations (worth monitoring)
1. ...

### Recommended Actions
[Ordered by priority, directed at the planner/scheduler]
```

### Key Sections to Always Cover

1. **Design-to-procure overlap** — is there a sequential gate where procurement waits for design completion?
2. **Overseas manufacturing chain** — cumulative duration from PO to site delivery
3. **Floor concurrency** — how many trades overlap across floors
4. **Testing & handover compression** — days from first test to TOC
5. **Float concentration** — where is 0-float concentrated? (usually project end)
6. **Missing scope** — any Phase/WBS from contract not in this schedule

## Pitfalls

- **Calendar info is lost in PDF export** — P6 PDF exports don't show which calendar each activity uses. Calendar effects need XER file analysis (see `xer-schedule-analysis.md`).
- **Relationship arrows are not extractable** — predecessor/successor logic is visual only in PDF. You can't compute the critical path from PDF — you infer it from 0-float activities.
- **Float in working days vs calendar days** — the float column in P6 exports is usually working days. 5 days float with a 5-day calendar = 7 calendar days.
- **Page footer noise** — each page has "Actual Level of Effort / Remaining Work" footer lines mixed with data. Skip these when parsing.
- **Line-wrapped activity names** — long activity names wrap to the next line. Read consecutive lines that don't start with an ID as continuation of the previous activity name.
- **Page feed breaks** — sections split mid-activity across page boundaries. Always check continuity at the start of each new page.
- **Don't assume all design phases are labeled** — some exports mix 50%/90% without explicit gate labels in activity names. Infer from activity IDs, duration, and sequencing.
- **Format differences between P6 versions** — P6 exports from different versions may have slightly different column layouts. The layout above is typical but not universal.
