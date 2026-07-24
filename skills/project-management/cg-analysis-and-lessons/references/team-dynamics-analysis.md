# Team Dynamics & Attitude Analysis

Extract team morale, pressure points, and interpersonal friction from project documentation. Use when asked to assess "how is the team doing", "team attitude", "team health", or "organizational climate".

## Data Sources (in priority order)

| Source | What It Reveals |
|--------|-----------------|
| **PROJECT_MEMORY.md Section 0 (Latest Status)** | Active conflicts, urgent demands, who is pushing/pushing back |
| **Section 3 (Critical Issues)** | Escalation frequency, dispute patterns, blocked items |
| **Section 2 (Org Chart)** | Vacancies, interim roles, reporting lines |
| **Section 17 (Staffing Gaps)** | Unfilled positions → team strain |
| **Subcontractor status updates** | Who is cooperative vs adversarial vs abandoning work |
| **CG response patterns** | Rejection rate, tone (professional vs impatient), consistency |
| **NCR disputes** | Whether team accepts or pushes back — confidence indicator |
| **Meeting log (Section 13)** | Who attends, who is absent, action item ownership |
| **Email scan summaries** | Urgency markers ("urgent", "deadline", "must", "critical") |

## Analytical Dimensions

### 1. Internal Team Health

| Signal | What to Look For |
|--------|-----------------|
| **Vacancy rate** | Unfilled positions / total team size |
| **Reactive vs proactive** | Is team initiating or responding to demands? |
| **Dispute confidence** | Does team push back on invalid NCRs/SIs? |
| **Throughput** | How many submissions/emails processed per period |
| **Tone markers** | "urgent", "must", "need before Monday" — frequency and source |

### 2. Consultant/Client Relationship

| Signal | What to Look For |
|--------|-----------------|
| **Rejection rate** | Code C+D as % of total submissions |
| **Escalation frequency** | Formal rebuttals, SI disputes, NCR challenges |
| **Consistency** | Does CG contradict its own prior rulings? |
| **Tone** | Professional vs impatient vs adversarial |
| **New demands** | Additional reporting, new processes imposed mid-project |

### 3. Subcontractor Stability

| Signal | What to Look For |
|--------|-----------------|
| **Declined scopes** | Subcontractors who accepted then declined |
| **Legal claims** | Variation claims, termination threats |
| **Abandonment** | Zero manpower, stopped work |
| **Rejection cascade** | Multiple firms rejected for same scope (Code C cascade) |

### 4. External Pressure

| Signal | What to Look For |
|--------|-----------------|
| **PMC demands** | New reporting requirements, accelerated cadence |
| **Schedule pressure** | % elapsed vs % complete, rejected baselines |
| **Deadline density** | How many "urgent" deadlines in a 2-week window |

## Output Format

Present as structured sections with:

```
## Overall Climate: {LABEL}

{One-line summary of dominant dynamic}

### Samaya Internal Team
| Member | Attitude Signal | Evidence |
|--------|----------------|----------|

### CG (Consultant) — {Label}
| Indicator | Detail |
|-----------|--------|

### NRS / Other Design Partners — {Label}
| Indicator | Detail |
|-----------|--------|

### Subcontractors — Mixed / {Label}
| Subcontractor | Attitude | Detail |
|---------------|----------|--------|

### Key Attitude Risks
1. {Risk} — {detail}
2. ...

### Positive Signals
- {Signal} — {detail}
```

## Climate Labels

| Label | Meaning |
|-------|---------|
| **HIGH PRESSURE / DEFENSIVE** | Multiple disputes, high rejection rate, team pushing back |
| **TENSE / COMPLIANT** | High rejection rate but team accepting and resubmitting |
| **STABLE / PROFESSIONAL** | Normal project friction, no escalations |
| **COLLABORATIVE** | Low rejection rate, active coordination, positive tone |
| **CRISIS** | Legal claims, work stoppages, termination threats active |

## Pitfalls

- **One source is not enough** — cross-reference PROJECT_MEMORY with email scans, meeting logs, and submittal registers
- **Tone can be misleading** — a single "urgent" email doesn't indicate crisis; look for patterns over 2+ weeks
- **Vacancies don't always mean strain** — some roles may be intentionally unfilled (budget, scope not yet active)
- **CG inconsistency is a pattern, not an anomaly** — when CG contradicts itself, note it as a coordination gap, not a one-off error
- **Subcontractor decline ≠ team failure** — scope mismatch is a legitimate reason to decline; flag only when pattern emerges
- **Update frequency matters** — a PROJECT_MEMORY last updated 3 weeks ago may miss recent dynamics; check email scan dates
