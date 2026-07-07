# Samaya Formal HTML Document Style

## Core Principle: Formal, Minimal Color

Samaya Technical Office documents must look professional and formal. The user explicitly corrected this across multiple sessions:
- 2026-06-23: "follow the style guide do not add more colors be formal"
- 2026-06-24: "no a lot for colors"
- Repeatedly corrected excessive colored badges, gradient backgrounds, and colored status indicators

**Golden rule: if an element does not need color to communicate its meaning, leave it neutral.** Plain text status descriptions ("Active", "Vacant", "Pending") are always preferred over colored pills/badges. Table rows should alternate white / #F8FAFC - never green-for-approved, red-for-vacant, amber-for-pending.

### Before Delegating Visual Design

Before delegating a section redesign to Claude or Codex, explicitly state: "Use ONLY var(--primary) for table headers. No colored badges for status. No gradients. Plain text for all status values." Subagents default to colorful designs unless told otherwise.

### Color Palette (use only these - no extras)

- **Primary (navy):** `#0F172A` — headers, section headings, tier badges, ALL table headers
- **Secondary (sky):** `#0284C7` — Tier 2 labels, specialist badges only
- **Tier 3 accent:** `#92400E` (amber-brown) — Tier 3 diagram bar only
- **Muted text:** `#64748B` — notes, scope descriptions, subtle info
- **Background light:** `#F8FAFC` — alternating row backgrounds, section group headers
- **Border:** `#E2E8F0` — table and card borders
- **Accent gold:** `#F59E0B` — cover accent line, revision badges
- **Fail red:** `#B91C1C` — NOT used in table cells. Use italic muted text for vacancies.
- **Pass green:** `#16A34A` — NOT used in table cells. Use plain text for Active status.

### What NOT to do

- ❌ **No gradients** — no `linear-gradient()`, no `background: radial-gradient()`. Use flat solid colors only.
- ❌ **No colored row backgrounds** — no green tint for approved, no red tint for vacant, no amber for pending. Use alternating white/`#F8FAFC` rows instead.
- ❌ **No colored status badges/pills** — no green/red/amber pills for status. Use plain text for status values.
- ❌ **No icon bullets in status cells** — no `● Active` with colored dots. Just plain text like "Active", "Vacant", "Pending".
- ❌ **No `color:var(--pass)` or `color:var(--fail)` on text** — keep status text in `var(--text-main)` or `var(--text-muted)`.
- ❌ **No secondary (blue) headers on location matrix or sub-contractor tables** — ALL table headers must be `var(--primary)`, even for specialist/engineering sections. Consistency across all tables.
- ❌ **No amber (Tier 3) colored headers** — only the Tier 3 diagram bar uses amber. All table headers use primary dark.

### Font & Base Sizes

Set a base `font-size: 11pt` on `body` so all `rem` values scale consistently from a known baseline:

```css
body { font-size: 11pt; }
td { font-size: 0.62rem; }   /* ~7pt — readable on A4 */
th { font-size: 0.6rem; }    /* same range */
```

Minimum readable size for annotations: `0.4rem` (~4.4pt). Anything below `0.38rem` is too small for print.

### Table Layout Pattern

**Critical:** Always set `table-layout: fixed` in the global `table` CSS to force percentage column widths to be respected:

```css
table { width: 100%; table-layout: fixed; border-collapse: collapse; }
```

Without `table-layout: fixed`, the browser auto-sizes columns based on content and ignores `th width%` values.

### Overflow Prevention

When using `table-layout: fixed`, always pair with word-wrap on cells:

```css
td, th { word-wrap: break-word; overflow-wrap: break-word; }
```
### Don't Auto-Open Files After Edits

After making HTML or Excel edits, **do NOT call `open`** on the file. The user refreshes the browser or reopens the Excel manually. Auto-opening is annoying and interrupts their workflow.

### Body Container Overflow

```css
body { overflow-x: hidden; }
svg, img { max-width: 100%; height: auto; }
h1, h2, h3, h4, p, li, div { hyphens: auto; }
```

### Column Width Patterns (common table types)

| Table Type | Columns | Width Distribution |
|---|---|---|
| Revision History | 6 | REV(7%) DATE(12%) DESCRIPTION(48%) PREPARED(12%) CHECKED(12%) STATUS(9%) |
| Distribution | 2 | RECIPIENT(30%) PURPOSE(70%) |
| QC Sign-Off | 5 | ACTION(14%) ROLE(22%) NAME(26%) SIGNATURE(24%) DATE(14%) |
| Authority Basis | 3 | SOURCE(18%) CLAUSE/DOC(28%) REQUIREMENT(54%) |
| Mobilization Milestones | 3 | DAY(10%) MILESTONE(70%) OWNER(20%) |
| Headcount Schedule | 6 | ROLE(50%) P1-P5(10% each) |
| Induction Steps | 4 | #(6%) STEP(20%) CONTENT(52%) OWNER(22%) |
| Sub-contractors | 4 | NAME(20%) DISCIPLINE(22%) PHASE(13%) MECHANISM(45%) |
| Risk Register | 9 | #(5%) RISK(22%) CAT(7%) P(5%) I(5%) R(5%) MITIGATION(30%) OWNER(13%) STATUS(8%) |
| Escalation Matrix | 4 | All 25% |
| KPIs | 3 | KPI(38%) TARGET(12%) DEFINITION(50%) |

For any table: ensure column widths sum to exactly 100%. Use `width:` on the `<th>` elements.

### Table Design Patterns

**Headers:** Always `background: var(--primary); color: white;` with consistent font-size (0.42rem for compact, 0.48rem for normal). **NEVER use secondary blue or amber for table headers.**

**Rows:** Alternate between `background: white` (no style) and `background: var(--bg-light)` (`#F8FAFC`). No per-row colored backgrounds.

**Status columns:** Plain text only. Values like "Active", "Approved", "Vacant", "Hiring", "Pending", "Remote". No colored pills, no dot icons, no background fills.

**Section group headers** (e.g. "Full-Time Samaya", "Specialist Firms"): Use `background: var(--bg-light)` row with bold `font-weight:700`, `colspan` across all columns.

**Badge labels** (FT/SP/INT in Tier 2/3 tables): Keep them compact (0.32rem), white text on colored background:
- FT → `background: var(--primary); color: white`
- SP → `background: var(--secondary); color: white`
- INT → `background: var(--text-muted); color: white`

### Location Matrix Tables (Section 6)

All three location matrix tables (Leadership, Engineering & BIM, Design Specialists) must use **identical styling**:
- Group section headers: `border-left: 3px solid var(--primary); background: var(--bg-light)`
- Table headers: `background: var(--primary); color: white` — no exceptions
- NO SVG icons in section headers (use plain bold text)
- Uniform column widths: ROLE(60%), HO(10%), SITE(10%), REM(10%), NOTES(10%)

### Page Counter

When the number of pages changes due to edits (splitting, merging, deleting pages), update the hardcoded total in the CSS:

```css
.page-number::after { content: "PAGE " counter(page-counter) " OF N"; }
```

Count with: `grep -c 'class="page"' filename.html`

### Tier Diagram Style (Section 3)

- 3-column grid with equal columns (`1fr 1fr 1fr`)
- Flat solid backgrounds per tier color: primary navy, secondary sky, amber-brown
- No gradients, no rounded corners beyond 2px
- Compact padding (3px 6px)
- Smaller font: 0.34rem for tier label, 0.44rem for title, 0.32rem for count

### Status Cell Text (approved version)

After user feedback, the clean style uses just the status word:

| Role | Status | Approval |
|------|--------|----------|
| Project Director | Active | Approved |
| QA/QC Manager | Vacant | Hiring |
| T&C Manager | Pending | Activates D88 |

No dots, no colored spans. If a role is Vacant or TBC, use `font-style: italic; color: var(--text-muted)` for the name.

### Cover Page

- Samaya logo top-left, ref/date top-right
- Arabic title below English title, matching: `مشروع متحف عسير الإقليمي · خطة إدارة موارد المشروع`
- 5-party logo row in cover footer: MoC · ACE M-B · CG · NRS · Samaya
- Logos rendered as `<img>` tags, not text
- Samaya logo on inner page headers only