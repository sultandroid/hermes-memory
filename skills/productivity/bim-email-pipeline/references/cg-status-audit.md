# CG Status Audit — Comprehensive Code Tracking

**Lesson from Jun 4, 2026:** The user corrected "6 Code C items" → "9 Code C items" because I only searched email archive keywords, missing items documented in existing project memory, disputes notes, and CG status maps.

## The 4-Source Cross-Reference Method

To find ALL CG response codes (especially Code C/Code D items needing action), **never rely on a single source**. Cross-reference all four:

### Source 1: Email Archives (Weekly MD files)
```
~/Documents/04_Outlook_Connection/mails/{week_no}.md
```
Search for patterns:
- `Code C` / `Code C –` / `C - Revise and Resubmit`
- `With Code C` / `With Code B` 
- `Code D` / `Disapproved`
- `Rejected`
- `B - Approved with Comments`

**Caveat:** An email saying "With Code C" may later be followed by "Rev.01 With Code B" — always check if a later email upgraded the status. A Code C on week 22 may be resolved by week 23.

### Source 2: PROJECT_MEMORY.md
```
Aseer-Museum/PROJECT_MEMORY.md
```
Check these sections:
- **Critical Issues** (section 3) — lists blocked items like IFC-0004
- **Submittals Dashboard** (section 5) — lists IFC packages with statuses
- **CG Response Status table** (newer section) — per-plan status
- **Active Code C Items** table (if exists)
- **Session Updates** — may document newly discovered items

### Source 3: disputes_and_rejections.md
```
Aseer-Museum/Scripts/notes/disputes_and_rejections.md
```
This file explicitly tracks all rejections, Code C returns, and escalation history. It may have a running total at the bottom (e.g., "Total active Code-C items: 6").

### Source 4: CG Status Mapping Files
```
Aseer-Museum/Email_Archive/CG_comprehensive_document_status_mapping.md
Aseer-Museum/Scripts/notes/submittals_cg_responses_matrix.md
```
These files map each document code to its CG response status. More comprehensive than individual email searches.

## Deduplication Process

After collecting items from all 4 sources:

1. **Merge by document code** — PL-0018, PL-0043, RP-0039, etc.
2. **Take the latest status** — if email says "Code B" for Rev.01 but the disputes file says "Code C" for Rev.00, the later revision's status is authoritative
3. **Remove resolved items** — items upgraded to Code B (approved with comments) are no longer blocking
4. **Verify against the most recent email archive** — the highest week number is the most current

## Reporting Format

When reporting Code C items to the user:

```
| # | Document | Code | Issue | Source(s) |
|---|----------|:----:|-------|:---------:|
| 1 | **IFC-0004** Life Safety | C | Needs PDD first | PM §3 |
| 2 | **PL-0018** Comm Plan | C | 8 comments | Email wk22/23 + PM |
```

Always include: document code, CG code, brief issue description, and which source(s) confirmed it.

## Common CG Code Meanings

| Code | Meaning | Action Required |
|:----:|---------|----------------|
| **A** | Approved | None — complete |
| **B** | Approved with Comments | Address minor comments, can proceed |
| **C** | Revise & Resubmit | Must revise and resubmit — **blocking** |
| **D** | Disapproved | Major rejection — contractually significant |
| U/R | Under Review | Awaiting CG response |

## Correction History & Lessons Learned

**2026-06-04 correction chain (user kept saying "still"):**
- First pass: 6 items (only from `disputes_and_rejections.md`)
- User: "no i think more" → expanded to 9 (added IFC-0004, SI-CG-ASEER-007, MA-0006, SC-0035 from email archives)
- User: "still" → expanded to 10 (added PL-0020 Stakeholder Rev00 from knowledge notes)  
- User: "still" → expanded to 11 (added PL-0043 rev00 original)
- User: "still" → expanded to include **aggregate** count: Weekly Report 13 shows **67 Code C total**

### 🔑 Key Lesson: Three Buckets of Code C Items

When asked "how many Code C need action?", the answer depends on scope:

| Bucket | Scope | Count | Source |
|--------|-------|:-----:|--------|
| **1. Specific documents** | Items with email confirmation | ~11 | Email archive + PM |
| **2. Aggregate total** | ALL categories combined | **67** | Weekly Report 13 §6 |
| **3. Per-category** | Breakdown by submittal type | varies | Weekly status dashboard |

### Why the Email Archive Underestimates

The email archive only captures items that triggered an email transaction (submission + CG response). Many Code C items live ONLY in the submittal register spreadsheet and never appear in email threads. The weekly report's aggregate table is the truer picture.

### Aggregate Counts from Weekly Report 13 (mid-May 2026)

| Category | Code C | Code D |
|----------|:------:|:------:|
| Material Submittal | 4 | 1 |
| Pre-Qualification | 37 | 10 |
| Document Submittals | 10 | 1 |
| Shop Drawings | 2 | 0 |
| IFC Drawing | 10 | 1 |
| Method Statement | 3 | 1 |
| Inspection Request | 1 | 0 |
| **TOTAL** | **67** | **14** |

### Always Cross-Reference THREE Sources

1. **Email archives** — explicit "Code C" mentions in weekly MD files
2. **disputes_and_rejections.md** — running log of all rejections
3. **Weekly status dashboard/report** — aggregate quantities by category

Never rely on only one source. Prefer the highest count when asked the aggregate number.
