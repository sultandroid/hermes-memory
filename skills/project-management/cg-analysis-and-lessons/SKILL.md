---
name: cg-analysis-and-lessons
description: Analyze consultant (CG) rejection patterns, build reviewer profiles, forecast submittal outcomes, and maintain a lessons learned register with daily watch system. Ties to approved project plans (PQP, Procurement, RMP, DMP).
---

# CG Analysis & Lessons Learned System

## Overview
Systematic analysis of consultant (CG) rejection patterns on a construction/museum project. Covers: extracting verbatim CG comments from PDFs, building reviewer profiles, forecasting submittal outcomes, maintaining a lessons learned register compliant with project plans, and running an event-driven lens system (pre-submit gate + post-response capture) with a daily cron safety net.

## Trigger

User asks to:
- Analyze CG rejection patterns or reviewer behaviour
- Build/maintain a lessons learned register
- Forecast submittal outcomes
- Process project emails and update registers — lessons learned is a mandatory target, not optional
- Review any CG response, NCR, or submittal rejection
- Update project documentation after a significant event (personnel change, overdue submission, escalation, process failure)

## Mandatory Protocol (encoded in AGENTS.md)

Every agent that touches a CG-related action MUST run the **7 Lenses** before and after the action. This is a hard rule, not optional.

### Pre-Submit Gate (before sending anything to CG)

| Lens | Check |
|------|-------|
| 🔴 Rejection | Has this submittal type been rejected before? Check `cg_rejection_patterns.md` |
| 🟡 Condition | Are all previous Code B conditions closed? Check `cg_code_b_conditions.md` |
| 📋 Checklist | Run the pre-submission checklist in `cg_forecast_engine.md` §3 |
| 💡 Improvement | Is there a lesson from a similar past submittal? Check `lessons_learned_register.md` |

If any check fails → **do not submit**. Flag the blocker and resolve first.

### Post-Response Capture (when CG replies)

When a CG response arrives (any code), run ALL 7 lenses:

| Lens | Action |
|------|--------|
| 🔴 Rejection | Code C or D? → Capture CG comment verbatim → Log as lesson |
| 🟡 Condition | Code B with conditions? → Add to `cg_code_b_conditions.md` |
| ⏰ Delay | Response took >14 days? → Flag as DA risk in submittal register |
| ⚠️ NCR | New NCR issued? → Root cause analysis → Log as lesson |
| 🔄 Rework | Does the response require rework? → Capture the process gap |
| 📋 Checklist | Did we miss a checklist item? → Update the checklist |
| 💡 Improvement | Any positive finding? → Capture for future projects |

### Cron Fallback

The daily cron at 1 PM KSA is a **safety net** — catches anything the event-driven process missed. The primary mechanism is the pre-submit gate and post-response capture above.

## Workflow

### Phase 1: Extract CG Comments from PDFs

1. **Locate the CG response PDF** — OneDrive correspondence folder or Adel Darwish's bank
2. **Extract text** using `pdftotext`:
   ```bash
   pdftotext /path/to/pdf.pdf - 2>/dev/null
   ```
3. **Record for each submittal:**
   - Submittal ref (MA-XXXX, PQ-XXXX, ZD-XXXX)
   - CG reviewer name (from signature block)
   - Date of response
   - Verbatim CG comment text
   - Code assigned (A/B/C/D/U)

### Phase 2: Build CG Rejection Pattern Register

Create `Technical_Office/CG_Analysis/cg_rejection_patterns.md`:

1. **Consolidated rejection table** — all C/D submittals with verbatim CG comments, grouped by type (IFC, PQ, MA, Design, HSE)
2. **Recurring rejection patterns** ranked by frequency:
   - Missing supporting documentation
   - Incomplete submission
   - Non-compliance with specs
   - Missing specialist endorsement
   - Sequencing violations
   - Insufficient technical data
   - Single-source supplier
   - Cross-disciplinary coordination gaps
   - Org chart deficiencies
   - Disputed milestones
3. **Rejection rate by discipline** — table with total, C, D, C+D%
4. **Cycle time analysis** — average review times per code, fastest/slowest, DA triggers
5. **Forecast section** — predicted CG response for submittals under review, with rationale
6. **Recommendations** — immediate (7d), medium (30d), long-term (60d)

### Phase 3: Build CG Reviewer Profiles

Create `Technical_Office/CG_Analysis/cg_reviewer_profiles.md`:

Per reviewer:
- Role and known submittals reviewed
- Tendencies (strictness, focus areas, common conditions)
- Review speed (days per submittal type)
- Submission strategy (how to pre-empt their concerns)
- Comparison matrix (strictness, speed, focus, typical outcome)

### Phase 4: Build Code B Conditions Register

Create `Technical_Office/CG_Analysis/cg_code_b_conditions.md`:

- All Code B conditions tracked as open obligations
- Pattern analysis (BIM coordination, sustainability, alt suppliers)
- Gap list of PDFs still to extract

### Phase 5: Build Forecast Engine

Create `Technical_Office/CG_Analysis/cg_forecast_engine.md`:

1. **Forecast matrix** — predicted code by submittal type with confidence level
2. **Reviewer-specific forecast** — per reviewer prediction
3. **Pre-submission checklist** — universal + type-specific items to verify before any submission
4. **Lessons learned database** — each entry: LL-ID, source event, root cause, impact, corrective action, preventive action, governing plan, linked risk
5. **Quick reference tables** — "CG Will Reject If..." and "CG Will Approve If..."

### Phase 6: Create Lessons Learned Register

Create `03_Plans/11_Quality/lessons_learned_register.md`:

**Structure per lesson:**
- LL-ID, date captured, source event, category
- Root cause, impact
- Corrective action, preventive action
- Governing plan (PQP / Procurement / RMP / DMP / SMP)
- Linked risk ID (PRR-XXX)
- Owner, status (🔴 Open / 🟡 In Progress / 🟢 Closed)

**KPI compliance table** — per quarter, target ≥ 2 lessons (per PQP §12.2)

**Daily Watch System — 7 Lenses:**

| Lens | Question | Triggers When... |
|------|----------|-----------------|
| 🔴 Rejection | Any submittal Code C or D today? | Any C/D → capture CG comment verbatim |
| 🟡 Condition | Any Code B with new conditions? | New conditions = open obligations |
| ⏰ Delay | Any submittal past 14-day SLA? | Day 10+ → log as DA risk |
| ⚠️ NCR | Any new NCR issued? | New NCR → root cause analysis |
| 🔄 Rework | Any rework from CG comment? | Rework = process failure |
| 📋 Checklist | Any checklist item missed? | Missed item → update checklist |
| 💡 Improvement | Any better way found? | Improvement = positive lesson |

**Cron job setup:**
```bash
# Daily at 1 PM KSA — runs the 7 lenses
cronjob action=create name=lessons-learned-daily-watch \
  schedule="0 13 * * *" \
  workdir=/path/to/repo \
  prompt="Run the 7 daily lenses on today's CG responses..."
```

### Phase 7: Update Risk Register

For each C/D submittal without a risk entry, add to `01_Registers/risk_register.md`:
- Risk ID (PRR-PRC-NN or PRR-CG-NN)
- Risk event, cause, consequence
- P×S score, response action, owner, target close date
- Evidence column with CG comment reference

## File Structure

```
Technical_Office/CG_Analysis/
  cg_rejection_patterns.md      — All C/D submittals + patterns + forecast
  cg_reviewer_profiles.md       — Per-reviewer tendencies + strategy
  cg_code_b_conditions.md       — Code B conditions as open obligations
  cg_forecast_engine.md         — Prediction engine + lessons + checklists

03_Plans/11_Quality/
  lessons_learned_register.md   — Formal LL register + daily watch system

99_Archive/11_Lessons_Learned/  — Closed lesson evidence
```

## Reference Files (in skill directory)

- `references/cg-reviewer-behavior-patterns.md` — Condensed CG behavior patterns from 13 lessons learned. Quick reference for "what will CG reject/approve" and per-reviewer tendencies.
- `references/lesson-entry-template.md` — Template for appending new lessons to the register. Includes category options, status codes, and governing plan references.

## Key Commands

```bash
# Extract CG comment from PDF
pdftotext /path/to/CG_response.pdf - 2>/dev/null

# Find CG response PDFs in OneDrive
find /path/to/OneDrive -name "*MA-00*" -o -name "*PQ-00*" 2>/dev/null

# Set up daily watch cron
cronjob action=create name=lessons-learned-daily-watch \
  schedule="0 13 * * *" \
  workdir=/path/to/repo \
  prompt="Run the 7 daily lenses..."
```

## Lessons Learned Register — Client-Sharable Only (HARD RULE)

The lessons learned register (`03_Plans/11_Quality/lessons_learned_register.md`) is a **formal project deliverable** shared with the client (MoC/CG). This is a hard rule — the user explicitly corrected this.

### What belongs

Every lesson must pass ALL of these checks:
- **Project-relevant only** — would you show this to the client? If no, it doesn't belong.
- **Tied to an approved plan** — each lesson links to PQP, Procurement, RMP, or DMP
- **Tied to a risk** — each lesson links to a PRR risk ID
- **Actionable** — has corrective action (what we did) and preventive action (what we'll do differently)

### What NEVER belongs (user correction — do not repeat)

- ❌ Internal process notes (OneDrive sync issues, cover sheet miscounts, tool quirks)
- ❌ Tool/environment quirks (write to /tmp first, git push failures, cron setup)
- ❌ Session-specific one-off events that don't affect the project outcome
- ❌ Anything that would confuse or embarrass the project in front of the client
- ❌ "Lessons" that are really just internal workflow improvements

**If a lesson wouldn't be shared with MoC/CG, it does not go in the register.** Period. The user will remove it and correct you.

### Lesson Structure

Each lesson has: LL-ID, date captured, source event, category, root cause, impact, corrective action, preventive action, owner, status (Open/In Progress/Closed), governing plan, linked risk ID.

### Web App Deployment

The lessons learned register is deployed as an interactive web app at `samaya-factory.com/aseer/registers/LN/`:

- Single HTML file, no build tools
- Sortable/filterable table, detail modal, CSV snapshot download, A4 PDF print with Samaya doc styling
- Dashboard KPI counters (total, open, in progress, by category)
- **Auto-updates on every git commit** via post-commit hook + daily cron at 1 PM KSA
- The update script (`~/.hermes/scripts/update-all-registers.sh`) parses the markdown, rebuilds the HTML, and deploys via scp

See `references/lessons-webapp-deployment.md` for the full build and deploy workflow.
See `register-webapp-template` skill for the complete template, pitfalls, and auto-update setup.

## Pitfalls
- **PDFs may not exist in correspondence folder** — check email attachments, Aconex, Adel Darwish's bank
- **Some CG responses lack named reviewers** — mark as "CG (general)" and update when identified
- **B-code conditions are often not recorded** in registers — must extract from PDFs separately
- **Lessons must tie to approved plans** — PQP §12.2 (≥2/quarter), Procurement §5, RMP §10.1
- **CG reviewer assignment is unpredictable** — prepare every submission to the strictest reviewer's standard
- **Do not claim closure on referenced documents** in CR Sheets — state facts, not statuses
- **Lessons learned register is a living document** — update daily via cron, review quarterly per PQP KPI
- **Lessons are for the client** — never include internal process notes, tool quirks, or session-specific events. If it wouldn't be shared with MoC/CG, it doesn't go in the register.
- **The 7-lens system is event-driven, not time-driven** — the primary trigger is every CG interaction (pre-submit gate + post-response capture). The daily cron is a safety net, not the primary mechanism.
