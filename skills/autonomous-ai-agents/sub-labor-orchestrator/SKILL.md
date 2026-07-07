---
name: sub-labor-orchestrator
description: "MANDATORY QA PIPELINE for ALL substantive tasks. User Order -> Codex Rewrites -> Research Phase -> Claude Executes -> Codex Audits -> Fix -> Deliver. Also covers orchestration delegating coding/research/analysis to Claude Code CLI, Kimi CLI, and Codex CLI sub-labors. LOAD THIS SKILL FIRST on every task."
version: 3.4.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [orchestration, delegation, qa-pipeline, workflow, claude-code, kimi, sub-labor, research, web-search]
    related_skills: [claude-code, hermes-agent, bim-email-pipeline]
---

# Sub-Labor Orchestration — Claude Code & Kimi CLI

## 🔴 ALWAYS DELEGATE — User Has an Army

The user explicitly corrected: **"alwayes use labors bro keep your qouta i have army under your hand Claude and Kimi and Codex use them"**

This means:
- **Default to delegation.** Every non-trivial task goes to a sub-labor. Do NOT do it yourself.
- **Your role is orchestrator/leader.** Plan, delegate, integrate results. Not executor.
- **Heavy work:** OCR, SVG/HTML generation, bulk file ops, complex calculations, verification passes → delegate.
- **Quick checks:** Simple grep/ls/read can stay local. Everything else → labor.
- **Always name the labor** in your response: "Delegating to [Labor Name] because [reason]."

**Decision tree:**
```
Task received
├── Trivial (1 tool call, simple read/ls/grep) → do it yourself
├── Heavy (multi-step, analysis, generation) → delegate to labor
│   ├── OCR invoices + bank receipts → Kimi or delegate_task
│   ├── HTML/SVG generation → Claude Code
│   ├── Data extraction + classification → Kimi or delegate_task
│   ├── Bulk Excel reading (3+ sheets, multi-file) → delegate_task with toolsets=["terminal"]
│   ├── QA audit of output → Codex or Kimi
│   └── Complex research → delegate_task with toolsets=["web"]
└── User says "check" / "update" / "review" → ALWAYS delegate (implies multi-step work)
```

**Pitfall:** The user has corrected this multiple times. Every time you catch yourself executing heavy work directly instead of delegating, stop and re-route. The quota savings are not worth the correction.

**Specific failure pattern — inline Python heredocs for data extraction:** Multi-line Python scripts inside shell heredocs (`python3 << 'PYEOF'`) are fragile. F-strings with `\n`, escape sequences, and single/double quote nesting cause syntax errors that are hard to debug. Signs you're in danger: you're writing more than 3 lines of Python inside a heredoc, f-strings include newlines, or you're trying to read multi-sheet Excel files. Stop, write the script to a `.py` file with `write_file`, then execute with `terminal("python3 /tmp/script.py")`. Or better: delegate to a sub-agent.

## 🔴 MANDATORY: LOAD THIS SKILL AT START OF EVERY TASK

**Before ANY work begins on this session's first task, load this skill.** The pipeline below governs ALL substantive work — editing documents, checking email, updating registers, analyzing files, building reports. Any task beyond a single `ls` command needs this pipeline.

**How to know if this skill applies:** If you're reaching for any tool other than `read_file` or `terminal(ls)`, load this skill first. Specifically:
- User says "update" → load this skill (implies multi-step change)
- User attaches a file → load this skill (implies review + action)
- User says "check" / "look at" / "review" → load this skill (implies analysis)
- User gives a multi-sentence order → load this skill (implies complex work)

**Pitfall:** Do NOT start executing without loading this skill. The user has corrected this repeatedly. Loading the skill is the guardrail that prevents skipping the pipeline.

## 🔴 MANDATORY QA WORKFLOW (Mohamed Essa QA Policy — NO EXCEPTIONS)

### STEP 0: PROJECT CONTEXT DISCOVERY (before any work)
Before executing the main chain, ALWAYS identify the project context:

1. **Check the project root folder** — look at the directory tree above the file you're working on. The folder name (e.g. `Tqanny_Projects/`, `Samaya_Projects/`) tells you the company.
2. **Identify the entity:** Samaya Invest / Samaya, Maqtana for Projects (مقتنى للمشاريع), Tqanny (تقتنى), or others.
3. **Apply correct branding** in all deliverables — company logo/text, contractor name, client name must match what's in the project root. Do NOT assume branding from a previous project carries over.
   - `Tqanny_Projects` → use **مقتنى للمشاريع / Maqtana for Projects** (the contracting entity)
   - `Samaya_` anything → use **Samaya Invest / Samaya** branding
4. **Check PROJECT_MEMORY.md** at the project root if it exists — it has the project identity table with company, client, and consultant names.
5. **Check README.md** in the relevant folder — contains lead times, status, discipline descriptions. Use this proactively to identify long-lead items. Do NOT wait to be told.
6. **Check reference documents** — Appendix B.pdf is **authoritative** for subcontractor package lists and numbering order, NOT the README or any other file. When Appendix B and the README conflict, Appendix B wins.

**Pitfall:** Do NOT blindly reuse logos or company names from earlier reports. Each project's root folder tells you which company you're working for. When in doubt, ask the user which company/logo to use.
**Pitfall:** Do NOT wait for the user to tell you something is long-lead. If the README says "14 weeks" for a package, that means its 50% package must include procurement lead items. Proactively adjust stage masks.

### THE CHAIN (mandatory, never skip):
```
User Order → STEP 0 (Project Context) → CODEX REWRITES → [RESEARCH PHASE if needed] → Claude Executes → CODEX AUDITS → Fix → Deliver
```

### The Steps:

1. **User gives order** → do NOT execute yet
2. **STEP 0: Project Context Discovery** — check the project root folder to determine company branding, client, and project identity before any work begins. ALSO check README, PROJECT_MEMORY.md, and reference files for lead times, priority flags, and scheduling constraints that affect deliverable decisions.
3. **Codex CLI rewrites the order first** — must send the raw user order to Codex via `terminal(codex exec ..., pty=true)` for restructuring into a clear task spec before ANY labor touches it. This is non-negotiable — the user explicitly requires this.
4. **[RESEARCH PHASE — if the task needs web research]** — see the dedicated Research Phase section below. Codex's structured spec identifies what needs researching. Route to the fastest capable labor (Pattern A/B/C). Research findings are appended to the structured spec before execution.
5. **Claude Code executes** — does the heavy work (HTML gen, analysis, documents) based on Codex's structured spec + any research findings
6. **Codex CLI audits ALL output** — checks: div balance, tags, CSS, logos, entity encoding, line-number corruption, data accuracy AND research accuracy (sources cited, facts verified). Nothing ships without Codex sign-off.
7. **Fix** — apply Codex's findings
8. **Deliver** — only after Codex sign-off

### ⚠️ CRITICAL PITFALL: NEVER Skip the QC Audit — It Is Not Optional

The user has explicitly corrected this multiple times: **"alwayes review your work use consaltant"** and **"did you make review and QC?"**. You MUST run QC after EVERY output generation — registers, specs, Excel files, emails, any deliverable. This is NOT optional.

**QC options (use in order of preference):**
1. **KIMI** — preferred for register/file generation QC. If KIMI times out on long prompts, route to...
2. **delegate_task** — send the generator script or output to a subagent with toolsets=["terminal","file"] for review
3. **Manual review** — only when both above fail. Apply the QC checklist yourself.

**Good QC prompts:**
- "Review this register generator script. Check stage masks, descriptions against SOW, 50% package depth, category header overlap, missing items."
- "Audit this Excel register output. Verify item counts match, stage assignments are appropriate for long-lead items."

**Never say "I'll run QC after" — run it before delivering. The user can see the gap.**

### ⚠️ CRITICAL PITFALL: Proactively Check Project Context

Before making decisions about deliverables (e.g. which items go at 50% vs IFC), check the project context files FIRST:
- README.md in the project/subcontractor folder — contains lead times, status, discipline descriptions
- PROJECT_MEMORY.md — project identity, contacts, schedule notes
- Reference documents — Appendix B (authoritative package list), lead-time tables

Do NOT wait for the user to tell you something is a long-lead item. If the README says "14 weeks" for showcases, that means 50% must include long-lead procurement items. If Appendix B contradicts the README, Appendix B is authoritative.

### Source-Faithful Wording Rule

When creating deliverables from contract documents (SOW, ER):
- Use the EXACT wording from the source document for descriptions
- "list same as SOW Listed" — do NOT paraphrase, summarize, or extrapolate
- Only SOW and ER are valid references for submittal items. Do NOT cite external specs, interface matrices, or vendor docs as sources.

## Spec-First Workflow (User Preference — Jun 2026)

When managing subcontractor deliverables and creating submittal registers, use **spec-first**:

1. **Write a SPEC.md** for each subcontractor package (stored in `_MANAGER_DASHBOARD/`) defining: scope, SOW/ER references, deliverables by stage (50/90/100/IFC), standards, coordination interfaces, lead-time flags
2. **Generate the Excel register** FROM the spec — the register is a **derived output**, not the source of truth
3. **The spec is canonical** — update the spec when scope changes, regenerate the register

**File location rule:**
- Management `.md` files (SPEC.md, SCOPE_REQUEST.md, SITUATION_REPORT.md, RESEARCH_NOTES.md) → `_MANAGER_DASHBOARD/`
- Excel registers (.xlsx) → own subfolder named `<Package>_Submittal_Register/` at the root of the subcontractor folder
- Do NOT put `.xlsx` files inside `_MANAGER_DASHBOARD/`
- Generator scripts (.py) → `02_Submittals/`

Do NOT create the register directly from the SOW. Writing the spec first forces completeness.

### Construction Submittal Register Pattern

When creating Excel registers for construction subcontractor packages:

**Structure:**
- Stage-mask approach: `[50%, 90%, 100%, IFC]` — 1=due at that stage, 0=not due
- Items organized by category (A, B, C...) matching SOW structure
- Saved to 3 locations: `02_Submittals/<Register>/`, `Docs/09_Registers/<Register>/`, `Subcontractors/<NN_Discipline>/<Register>/`
- Generator script (.py) kept at `02_Submittals/` for regeneration

**50% package must be substantial:**
- For long-lead items (check README for lead times), push procurement decisions to 50%
- Minimum 5-8 items at 50% for a credible design gate review
- Include: schedules, preliminary drawings, design criteria, existing conditions surveys

**QC checklist for registers (run before delivery):**
- [ ] Stage masks match lead-time logic (long-lead = earlier stages)
- [ ] Descriptions use exact SOW wording
- [ ] 50% package not critically thin (<3 items triggers review)
- [ ] Category header ranges don't overlap (latent bug)
- [ ] References only cite SOW § or ER §
- [ ] All 3 save locations updated
- [ ] **Cross-package scope check**: If a subcontractor's scope overlaps with another (e.g. rigging is structurally related to structural steel), add the shared items to BOTH registers. The structural designer's register should include the rigging items even if rigging has its own Appendix B package folder. Keep both — the separate folder for tracking AND the merged items in the designer's register.

### Subcontractor Folder Numbering Rule

Subcontractor folders must be numbered to match **Appendix B order**, NOT the old README numbering or a custom scheme. Related packages (e.g. M&E + MEP Designer) should be adjacent. Do NOT create folders for Appendix B packages that don't already exist in the project — only work within the existing folder structure.

### Source-Faithful Wording Rule

When creating deliverables from contract documents (SOW, ER):
- Use the **EXACT wording** from the source document for item descriptions
- The user says **"list same as SOW Listed"** — do NOT paraphrase, summarize, or extrapolate
- Only SOW and ER are valid references for submittal items. Do NOT cite external specs, interface matrices, or vendor docs as sources.

### Draft Email Files Rule

Do NOT create or leave any draft email files (*draft*email*.md, _Email_to_*.md, DRAFT_EMAIL_*.*, or similar) anywhere in the project. The user considers these clutter across ALL variant patterns. If you draft an email, deliver it in the chat or send it directly — never save it as a project file.

### Labor Roles
- **Codex CLI = QC Gate + Order Rewriter** — rewrites/structures ALL user orders before any labor touches them. Then audits ALL output before delivery. Nothing ships without Codex sign-off.
- **Claude Code = Main Labor** — executes structured orders from Codex (HTML gen, deep analysis, documents)
- **Kimi = Monkey Work + Fast Research** — quick checks, file sorting, data extraction, AND fast web research via built-in SearchWeb. First-rank labor for simple lookups, product specs, code references, price checks. Also handles parallel deep research via delegate_task with toolsets=["web"].

### Always Name the Labor
When you delegate to a sub-labor, explicitly state **which one** and **why** in your response. Format: "Delegating to **[Labor Name]** because **[reason]**."

### Labor Org Chart
```
Hermes Agent (Leader — Plan, Delegate, Deliver)
  │
  ├── Codex CLI (QC Gate)
  │     • Rewrites ALL user orders into clear structured tasks
  │     • Audits ALL Claude Code output before delivery
  │     • Catches HTML/CSS bugs, layout breaks, entity errors, structural issues
  │     • Runs validation scripts (tag balance, regex, Chrome headless render)
  │
  ├── Claude Code (Main Labor)
  │     • Executes structured orders from Codex
  │     • Heavy work: HTML gen, deep analysis, document creation
  │     • Specialist subcontractor work
  │
  └── Kimi (Monkey Work + Fast Research)
        • Quick checks, file sorting, data extraction
        • Simple lookups, grep/glob tasks
        • 🆕 Fast web research via SearchWeb (Pattern A)
        • 🆕 Parallel deep research via delegate_task with toolsets=["web"] (Pattern B)
```

### ⚠️ The Codex CLI QA Gate — What Codex MUST check before any delivery:

**Branding (project-specific — identify from Step 0):**
- Company name: matches the entity identified from the project root (e.g. مقتنى للمشاريع / Maqtana for Projects, Samaya, etc.)
- No cross-contamination: logo/name from project A does NOT appear in project B's deliverables
- Logo-strip: consistent header style (single-line or multi-logo) matching the project's established template
- Client name: verify against PROJECT_MEMORY.md or the project folder context

**HTML reports:**
- Div balance: open_divs == close_divs (mismatch breaks page layout)
- @page CSS: must have `size: A4 portrait; margin: 0` (double margins = broken layout)
- .sheet: must have `overflow:hidden` and `page-break-after:always`
- Logo paths: must use relative `../` prefix from the document's location
- No line-number corruption: grep for `^[0-9]+|` prefix pattern — if found, strip immediately
- Template consistency: logo-strip, meta-grid, doc-strip must all be present on each page

**Content / data:**
- Scope tags: [MoC], [NRS], [SAMAYA] assigned correctly
- RAG status: OK/Partial/Pending/Missing/Future/N/A — no incorrect status
- Counts match: total items == sum of all status counts

**Process quality:**
- All critical findings from the last audit round were fixed
- No placeholder text left in (TBD, TODO, NRS FILL)
- File written to the correct path

## 🔷 RESEARCH PHASE — Multi-Agent Research Workflow

When the user's task requires web research (regulatory lookups, technical specs, product pricing, supplier vetting, standards, best practices), execute this phase AFTER Codex rewrites the order but BEFORE Claude Code executes.

### Research Decision Tree

```
User Order → Codex Rewrites
  → Does the task need research?
    → NO → Skip to Claude Code execution
    → YES → What kind?
      → SIMPLE (1-2 facts, product lookup, price check, code ref)
        → Fastest capable labor: Kimi (Pattern A)
      → COMPLEX (multi-aspect, regulatory, competitive analysis)
        → Parallel multi-agent: delegate_task × 2-3 (Pattern B)
      → DEEP SYNTHESIS (cross-source analysis, regulatory deep-dive)
        → Claude Code with WebSearch (Pattern C)
```

### Speed Ranking for Research

| Rank | Labor | Startup | Search Tool | Best For |
|------|-------|---------|-------------|----------|
| 🥇 1st | **Kimi CLI** | ~2s | SearchWeb (built-in, not deferred) | Quick fact-check, product lookup, price check, single question |
| 🥈 2nd | **delegate_task** | ~5s | web_search, web_extract (direct tools) | Parallel multi-aspect research (2-3 subagents) |
| 🥉 3rd | **Claude Code** | ~10-15s | WebSearch (deferred — loaded on demand) | Deep synthesis, regulatory analysis, multi-source cross-ref |

### Pattern A: Fast Research — Single Labor (Kimi)

**Use when:** 1-2 simple questions, product spec lookup, price check, building code section lookup, supplier name verification.

```bash
# Single question — fastest possible
echo "What are SEC electrical requirements for museum exhibition in Saudi Arabia?" | kimi --print --quiet

# Multi-part lookup
cat << 'EOF' | kimi --print --quiet
Research these for Aseer Museum (Abha) exhibition fit-out:
1. Civil Defence NOC requirements for museum occupancy in KSA
2. Typical temp/humidity specs for museum AV equipment rooms
3. Approved suppliers for museum display cases in Saudi Arabia
Cite sources for each.
EOF
```

**Extract Kimi's answer cleanly (strip protocol JSON):**
```bash
cat << 'EOF' | kimi --print 2>&1 | python3 -c "import re,sys;d=sys.stdin.read();m=re.findall(r\"text='([^']*)'\",d);print(m[-1] if m else d)"
Research question
EOF
```

### Pattern B: Parallel Multi-Agent Research — delegate_task

**Use when:** Multi-aspect research where 2-3 independent angles can be explored simultaneously. Each Hermes subagent gets full `web_search` + `web_extract` tools.

```python
# Parallel: 3 subagents research different aspects independently
delegate_task(
    tasks=[
        {
            "goal": "Research SEC electrical requirements for museum exhibition fit-out in KSA. Report: regulations, NOC steps, timeline, exemptions for existing buildings.",
            "context": "Project: Aseer Museum (Abha), existing 2015 building, D&B fit-out. Contract 0010003521.",
            "toolsets": ["web"]
        },
        {
            "goal": "Research Civil Defence + Municipality NOC requirements for museum occupancy in Abha, KSA. Report: docs needed, approval stages, timeline, responsible entities.",
            "context": "Aseer Museum renovation — need permits/NOCs before exhibition fit-out proceeds.",
            "toolsets": ["web"]
        },
        {
            "goal": "Research museum-grade AV system suppliers and display case suppliers in Saudi Arabia/GCC. Report: 3-5 suppliers per category with contact info, lead times, price ranges (SAR).",
            "context": "Budget reference for Aseer Museum AV hardware (BOQ §011). Looking for regional suppliers.",
            "toolsets": ["web"]
        }
    ]
)
```

**Good candidates for parallel research:**
- Multiple authorities (SEC + Civil Defence + Municipality)
- Multiple product categories (AV + MEP + glass + lifts)
- Competitive comparison (3 vendors for same item)
- Multi-clause contract review (ER clause X + SOW section Y + BOQ item Z)
- Technical standards across disciplines (BIM + MEP + fire safety)

**Avoid parallel when:**
- Single simple lookup (Pattern A is faster)
- Sequential dependency (finding A needed before researching B)
- Subagent context window would be exceeded (chain instead)

### Pattern C: Deep Synthesis — Claude Code

**Use when:** Research needs cross-referencing multiple sources, regulatory analysis across authorities, or technical standard deep-dives that benefit from Claude's stronger reasoning.

```bash
claude -p "Research and synthesize: Complete authority approval requirements (NOCs) for a museum exhibition fit-out in Abha, Saudi Arabia. Cover: SEC (electricity), Civil Defence (fire safety), Municipality (building), CITC (telecom), SCD/GDCD (heritage if applicable), Emirate. For each: documents, processing time, fees, and whether the existing 2015 building changes requirements. Cite all sources." --allowedTools "WebSearch,WebFetch" --max-turns 15
```

**Good candidates for deep synthesis:**
- Regulatory cross-reference across 3+ authorities
- Technical standards analysis (ISO 19650 BIM, ASHRAE museum HVAC, NFPA fire)
- Multi-source price validation
- Competitive landscape analysis
- Feasibility studies requiring researched precedent

### Pattern D: Research → Build Pipeline

When the task is "research X then create a deliverable about X":

```python
# Step 1: Parallel research via Pattern B
results = delegate_task(
    tasks=[
        {"goal": "Research topic A", "toolsets": ["web"]},
        {"goal": "Research topic B", "toolsets": ["web"]}
    ]
)

# Step 2: Feed research + Codex spec → Claude Code builds deliverable
terminal(command="""claude -p 'Using these research findings: [topic A results] [topic B results], create the HTML report...' --allowedTools Read,Edit,Write,Bash --max-turns 20""", workdir="/path")
```

### Research Quality Checklist (audited by Codex)

After Claude Code builds deliverables from research, Codex's audit must include:

- [ ] All factual claims have cited sources
- [ ] No hallucinated regulations, standards, or prices
- [ ] Price ranges are reasonable with attribution
- [ ] Dates, deadlines, and timelines are accurate
- [ ] Regulatory requirements match current KSA standards
- [ ] Vendor/supplier names and contacts verified
- [ ] Research findings cross-referenced against contract/SOW/BOQ
- [ ] No contradictory claims between research sources resolved

---

## The Hierarchy

```
You (Hermes — Lead/Orchestrator)
├── Claude Code CLI v2.1.153 — Main Labor
│     Complex documents, Odoo/Notion, MCP, heavy coding, HTML generation
│
├── Codex CLI v0.128.0 — Quality Controller (QC Gate)
│     Audits ALL Claude Code output before delivery
│     Catches HTML/CSS bugs, layout breaks, entity errors, structural issues
│     Runs via terminal(pty=true) or codex exec --sandbox workspace-write
│
├── Kimi CLI v1.43.0 — Monkey Work + Fast Research
│     Fast checks, file sorting, data extraction, simple lookups
│     🆕 Quick web research via SearchWeb (Pattern A)
│     🆕 Parallel research via Hermes delegate_task (Pattern B)
│
└── Pi Agent v0.78.0 — General Coding Assistant (Secondary)
      Backup labor when Claude Code quota exhausted
      Print mode via `pi -p "task"`
```

## Critical Rules

### Cross-Audit Pattern: Order Matters

The proven ordering (verified in 2026-05-29 session with Codex CLI):

1. **[Research Phase (if needed)]** — see dedicated Research Phase section: Pattern A (Kimi fast), B (parallel), or C (deep synthesis)
2. **Claude Code executes** — does the heavy work (HTML gen, analysis, documents) incorporating research findings
3. **Codex CLI audits** — checks ALL output: HTML structure, tag balance, CSS, entity encoding, logo paths, content accuracy AND research accuracy (sources, facts, prices, regulations)
4. **Fix** — apply Codex's findings
5. **Deliver** — only after Codex sign-off

**Why this order:** Codex rewrites and structures the order (identifying research needs). Research phase finds facts and sources. Claude Code produces the work with those facts. Codex CLI reviews with fresh eyes, catching structural issues Claude missed (line-number corruption, bare & characters, div imbalance, missing closing tags) AND research accuracy issues (hallucinated sources, wrong prices, incorrect regulations). This is the proven QC gate pattern with integrated research validation.

**Codex CLI audit scope (files >50KB):** For large HTML files, Codex runs Python validation scripts (tag balance, regex patterns, Chrome headless render check) plus manual review. It produces a structured QA report with PASS/FAIL per check.

### User Communication Preferences

### "Update Memory" = ALL Stores

When the user says "update memory", update ALL of:
1. **Hermes agent memory** — via `memory(action='add')` tool
2. **Project memory files** — `Scripts/PROJECT_MEMORY.md`, `Scripts/notes/*.md`, or equivalent
3. **Notion project page** — append session update via `ntn` CLI
4. **Any other relevant knowledge stores** — skills, registers, summary docs

Never do just one. The user explicitly corrected this.

### MANDATORY: Document Style Guide — Engineering Template v2.0

This user has an established Engineering Template v2.0 style guide. EVERY HTML document generated for this project MUST follow it. Do NOT generate documents in a generic or incorrect format — the user will reject and redirect.

**Location:** `~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/`

**Quick reference:**
- Palette: Navy #0F172A primary, Sky #0284C7 secondary
- Border radius: max 2px — no rounded corners, no box-shadow
- Font: Inter (EN), Tajawal/Amiri (AR)
- Format: A4 portrait, print-ready @page CSS
- Language: Bilingual — English lead, Arabic secondary on section titles/labels
- Logo row: 5-party — MoC (Client) · ACE (PMC) · CG (Consultant) · NRS (Design) · Samaya (Contractor)
- Cover: DC block with doc-no, rev, status, dates, originator
- Footer: doc-no · context · page-number on every section
- Status badges: pass (green) / fail (red) / partial (amber) / neutral (gray)
- Doc code: project-specific prefix (e.g. ASR-SAM-RMP-001 Rev 00)

**Template files:**
- HTML: index.html + css/style.css
- Word: Doc Style Guide/samaya_doc_template.py
- Full reference: Engineering-Deck-HTML-Style-Guide.md

**Pitfall:** Even internal team docs must follow this style guide. Start from the template, not scratch.

### Real-Data Sourcing Rule (registers, logs, status docs)

When creating a register, log, or status document that reflects project conditions:
1. Source risk events, status data, and metrics from ACTUAL project evidence: recent emails, correspondence logs, daily reports, submittal status, CG review comments.
2. Do NOT populate from generic templates / typical construction risks. The user will flag template-generated content that does not match real project conditions.
3. Before generating, gather: recent Outlook emails (last 30 days), CG correspondence status, subcontractor status, daily reports, schedule updates.
4. Cross-reference against the project actual current phase.
5. Only then build with verifiable evidence.

**Pitfall:** A register with generic risks (e.g. BIM model clashes, AV hardware obsolete) that do not match what is actually happening on site will be rejected. Real risks are things like CG review backlog on plans, specialist not yet onboarded, design submission rate vs deadline.

### English-Only Output

The user does NOT read Arabic in conversation (said "i cant read your arabic"). All agent-to-user responses must be in English only.

Exception: Writing Arabic text INTO files (bilingual HTML documents, Arabic MD files) is correct — the user wants Arabic content IN documents. The chat conversation is always English.

### ⚠️ CRITICAL PITFALL: "Simple" Tasks Still Go Through Full Workflow

**NEVER short-circuit the workflow for a task that seems "simple" or "just a check."** The user's exact words when catching this: "why you didnt folow", "why you forget".

**Examples of deceptive "simple" requests that trigger the full workflow:**
- "check download folder" / "check my Downloads" → full organization scope (see `references/downloads-organization-pattern.md`)
- "check email" / "check outlook" / "check my emails" → **FULL PIPELINE** — see the `bim-email-pipeline` skill for the complete 9-step scope. Quick reference:
  1. Dedup — check Email_Archive/ first, skip already-processed emails
  2. Find project-related emails (by sender, subject, project code) — includes ALL attachments
  3. Download attachments from Outlook to `/tmp/` (bypasses OneDrive file-lock)
  4. Classify by category (PL, ZD, HSE, SI, NCR, RP/REP, MSG, etc.)
  5. Copy to correct project subfolders
  6. Send key attachments to labors (Kimi fast / Claude deep) for markdown enrichment → save to `Scripts/notes/`
  7. Archive as markdown in `Email_Archive/`
  8. Update registers
  9. Update knowledge base with labor-generated summaries
  10. **RIBA Deliverable Tree Refresh** — After any batch of new project data (emails, submittals, weekly reports):
      - Locate `Aseer_RIBA_Stages4to6_Deliverable_Tree.html` in `Completed Tender Package From NRS/`
      - Cross-reference each new document/submittal against the tree's RAG criteria
      - Update items with new evidence: change descriptions + RAG status (Pending→Partial, Missing→Partial, etc.)
      - Recalculate counters: OK/Partial/Pending/Missing/Future → verify total unchanged
      - Bump revision number (e.g. Rev 00→Rev 01)
      - Example from May 2026: Hesham's emails provided evidence to move 11 items (10 Pending→Partial, 1 Missing→Partial)
  Do NOT stop at listing — the user corrected this explicitly.
- "update memory" → ALL stores (memory tool + PROJECT_MEMORY.md + Notion + registers)
- "clean up X" → inventory → dedup → organize → report
- "rename folder in OneDrive" / "organize folders in 2026" → **NEVER batch-rename via sub-labor** (Codex uses `mv` which breaks OneDrive sync). Always rename ONE at a time via OneDrive web and let sync propagate. See `macos-housekeeping` skill → Renaming section + cascade corruption warning.
- "what's new" → discover → categorize → summarize → register

**Rule:** ANY user request that involves examining, organizing, modifying, or acting on files/information MUST go through the full Codex rewrite → execute → audit pipeline. The user's frustration was proportional to me assuming "check download folder" was a quick `ls` command when it meant a full multi-phase operation.

**Trigger words that signal scope expansion:** check, look at, clean, organize, sort, arrange, file, move, register, update, outlook, email.

**Scope expansion rule: "Check X" means classify ALL files, not just one category.**
When the user says "check download folder" / "scan download folder" or similar, the scope includes ALL files — not just one type. The user corrected this explicitly: "useful for anything not only for plans". This means:
- Scan EVERY file in the target directory
- Classify by usefulness to ANY project purpose (not just your current workstream)
- File each document to its most appropriate location
- Delete duplicates and old versions
- Only leave behind truly non-project files (installers, personal items, calendar invites)
- Don't filter by document code prefix (PL-, ZD-, etc.) — include proposals, meeting minutes, RFIs, vendor docs, drawings, everything

**"update" + file attachment = full pipeline.** When the user says "update" while attaching a file (or referencing an existing document), assume it means: audit the document for errors → research new evidence → apply corrections → update all counters → Codex audit → deliver. Do NOT start editing the file directly.

When you hear these, do NOT act directly. Write a plan, send to Codex for rewriting, and scope the full implied workflow before executing.

### File Organization: "Check Downloads" Pattern

"Check download folder" / "check my Downloads" means the following full workflow. See `references/downloads-organization-pattern.md` for the detailed process.

TL;DR scope:
1. **Phase 1: Inventory** — scan all files, compute hashes, identify duplicates + version variants
2. **Phase 2: Classification** — categorize by project (Aseer, Zamzam, Tahakom, etc.) and type
3. **Phase 3: Destination structure** — create project-based hierarchy
4. **Phase 4: Dedup + versioning** — exact duplicates deleted, version variants archived (keep latest)
5. **Phase 5: Move execution** — organized into project folders with operation log
6. **Phase 6: Register + memory update** — PROJECT_MEMORY.md, Notion, Hermes memory, project registers
7. **Phase 7: Final report** — summary of everything done

### 📁 File System Searches: Local First, Then Delegate

When searching for an unknown file, person, supplier, or term across the filesystem:

1. **Search locally first** — `rg`, `grep`, `mdfind`, `search_files()` are faster and more reliable than subagents for this task
2. **Only escalate to labor** if local search returns nothing. delegate_task with file tools can timeout (600s) on broad searches.
3. **Multiple spelling variants** — try Faqeeh/Faqih/الفقيه variants before concluding "not found"

**Proven pattern (2026-06-05):** Searching for "Alfaqueeh" via delegate_task timed out. Same search via local rg/grep/mdfind completed instantly. Start local.
---

When organizing files across folders (moving, copying, or deleting):
1. **Inventory first** — list all locations of the file (Downloads, Desktop, Outlook Temp, project subfolders, Email Archive, Subcontractors)
2. **Deduplicate** — group by filename + file size to find true duplicates
3. **Keep the canonical copy** in the proper BIM subfolder
4. **Delete known duplicates** — temp files (Outlook Temp), wrong-project copies (Jabal Omar docs that belong to Aseer), Desktop copies of already-filed documents
5. **Preserve legitimate copies** — Subcontractor copies needed for vendors, email archive .eml files
6. **Report** — what was deleted, what was kept, where the canonical copy lives

## Skill Audit Protocol (ALL skills/scripts — mandatory)

Every new or rewritten skill/script MUST be audited by a labor as an **"AI Skills Professional"** before finalizing. This is mandatory QA, not optional.

**Trigger:** Any time you create (`skill_manage create`), rewrite (`edit`), or significantly patch (`patch`) a skill or standalone script.

**Auditor role:** The labor acts as a senior code reviewer / systems architect. Not a peer — a professional reviewer judging code quality, security, error handling, and architecture.

**Rubric (each dimension scored A-F):**
| Category | What to check |
|----------|--------------|
| Code Quality | Structure, typing, readability, comments, dead code |
| Error Handling | Timeouts, retries, state corruption, crash recovery |
| Security | Injection vectors, path traversal, secret leaks, ReDoS |
| Tool Integration | AppleScript/cron/bash — reliability under failure |
| Cron-readiness | Lock file, exit codes, log rotation, dup prevention |
| Maintainability | Config vs hardcode, documentation, DRY |

**Output format:**
```
# AUDIT REPORT — [Skill/Script Name]
Overall Grade: C (Needs Significant Improvement)

## 1. CRITICAL (Must Fix)
- C1: ... (severity + code location + fix)
## 2. MAJOR (Should Fix)
- M1: ...
## 3. MINOR (Nice to Fix)
- m1: ...
## 4. Security Summary
## 5. Overall Rating & Recommendations
```

**After audit:** Apply ALL critical fixes and as many major fixes as practical before re-submitting to the user. Only skip if the user explicitly says "ship it as-is".

**Canonical audit output format (proven in session):**

```
# AUDIT REPORT — [Skill/Script Name]
**Size:** N lines, single-file design
**Runtime evidence:** [state/behavior observed]

## 1. CRITICAL (Must Fix — security / data loss / reliability)
- C1: [Title] — [severity + code location + concise fix]
- C2: [Title]
  - **Location:** Lines NN-NN
  - **Problem:** [concrete impact]
  - **Severity:** [Data loss / Injection / Duplication / Crash]
  - **Fix:** [code snippet]

## 2. MAJOR (Should Fix — correctness / reliability / performance)
- M1: [Title]
- M2: [Title]

## 3. MINOR (Nice to Fix — polish / clarity / edge cases)
- m1: [Title]
- m2: [Title]

## 4. SECURITY SUMMARY
| Vector | Severity | Issue |
|--------|----------|-------|
| [e.g. SQL injection] | CRITICAL | [description] |

## 5. OVERALL RATING
| Category | Grade | Notes |
|----------|-------|-------|
| Code Quality | C+ | Clean enough but lacks structure/typing |
| Error Handling | D | No retry, no timeout, no corruption recovery |
| Security | C- | Injection vector in [component] |
| Cron-readiness | D | No lock, no exit codes, unbounded state/log |
| Maintainability | C | Hardcoded paths, dead code, no config |
| **Overall** | **C** | Needs Significant Improvement |

## 6. CODE-LEVEL RECOMMENDATIONS (top N in priority order)
1. [Fix] — concrete change
2. [Fix] — concrete change
...
```

**After audit:** Apply ALL critical fixes and as many major fixes as practical before finalizing. Only skip if user explicitly says "ship it as-is".

### English-Only User-Facing Output

The user **does not read Arabic in conversation**. All agent-to-user communication must be in English only. Bilingual documents (PEP, VE, TQ reports) should be written with Arabic lead + English follow IN THE FILE, but the CHAT conversation with the user is always English.

### Recommendation Tone: "HOLD" Not "REJECT"

When making invoice or action recommendations in reports:
- **Use "HOLD"** — conservative, leaves room for negotiation
- **Do NOT use "REJECT"** — too aggressive, user explicitly corrected this
- If partial work exists, say: "Pay ~45K, HOLD balance ~45K"
- Explain the reasoning: what EV justifies partial payment

### 🔴 CRITICAL: read_file() Truncation — Data Loss When Patching Then Writing

**WARNING: `read_file()` defaults to 500 lines.** If the file is longer, you silently get a partial view. Writing that back to disk **permanently truncates** the file.

This has happened **multiple times** (2026-05-29, 2026-06-16):
- 1,458-line PEP (152KB) → 56KB (destroyed, rebuilt from backup)
- 781-line HTML (51KB) → 500 lines (bottom 281 lines lost, had to regenerate sections)

**Common failure pattern — cascade trap:**
1. `patch()` one thing in a large file ✓ (fine)
2. Then `execute_code` with `read_file()` + regex + `write_file()` to make a second change
3. `read_file()` without `limit=N` returns only first 500 lines
4. `write_file()` overwrites the file with truncated content → **bottom of file lost**

You won't notice until you verify with `wc -l` or discover missing sections.

**Mitigation (MANDATORY — recovery patterns included):**

**Check for contamination after any write:**
```bash
grep -cP '^\s*\d+\|' file.html
```
If > 0, the file has line-number prefixes embedded. Fix with:
```python
import re
with open('file.html') as f:
    raw = f.read()
clean = re.sub(r'^\s*\d+\|', '', raw, flags=re.MULTILINE)
with open('file.html', 'w') as f:
    f.write(clean)
```
Then re-check: `grep -cP '^\s*\d+\|' file.html` should return 0.

**CRITICAL — execute_code hazard:** `from hermes_tools import read_file` returns content WITH line-number prefixes (`1|...`, `2|...`) in `content["content"]`. Writing that back directly POISONS the file with line numbers AND truncates at 500 lines if no limit is passed. Both risks compound.

**Surge deploy pitfall (Jun 2026):** Line-number contamination (`1|`, `2|`... at line starts) is invisible during local file viewing but completely breaks the CSS cascade on the deployed site. The `1|`, `2|` etc. appear as raw text nodes inside `<style>` tags, causing CSS to fail silently after the first contaminated line. **Always run this check before any Surge deploy:**

```bash
grep -cP '^\s*\d+\|' index.html
# If > 0, DO NOT deploy until fixed
python3 -c "import re; open('index.html','w').write(re.sub(r'^\s*\d+\|', '', open('index.html').read(), flags=re.MULTILINE))"
grep -cP '^\s*\d+\|' index.html  # verify 0
```

Safe pattern inside execute_code:
```python
from hermes_tools import read_file, write_file
import re
raw = read_file("path", limit=10000)
html = re.sub(r'^\s*\d+\|', '', raw["content"], flags=re.MULTILINE)
# now safe to process and write
html = html.replace("old", "new")  # your edits
write_file("path", html)
```

**Proven recovery (2026-06-16):** 781-line HTML (51KB) was written back with 483 line-number prefixes AND truncated to 500 lines. Bottom 281 lines lost entirely. Recovery required: (1) restore missing sections from original content, (2) strip line-number prefixes with regex, (3) verify with grep for remaining artifacts.

**Prevention rules:**
1. **Use `terminal(cat path)` instead of `read_file()` when you need full file content** — cat has no line limit and no line-number pollution
2. If you must use `read_file()` inside `execute_code`, always pass `limit=10000` and strip line numbers before processing
3. After ANY write_file call, verify with both `wc -l` and the contamination grep above
4. When doing sequential edits on one large file (patch → execute_code → write_file), **do the execute_code work first, then patch** — or consolidate into a single pass
5. Best practice for large HTML: use `terminal("cat path | python3 -c '...'")` with a processing pipeline instead of read_file+write_file

### ⚠️ Create Backups Before Delegating Destructive Edits

Before sending ANY file-patching task to a sub-labor (Claude Code patch, Codex audit that may write changes):
1. **`cp file.html file.html.bak`** — create a timestamped backup
2. **Note the file size** — `wc -c file.html` so you can detect corruption after the edit
3. **Verify the backup is valid** — `head -1 file.html.bak` should show DOCTYPE or expected header

Without a backup, a failed patch has no clean revert point. The subagent's summary may claim success even when other parts of the file were corrupted. The backup is your safety net.

**Proven failure mode (Jun 2026):** Claude Code patched page 15 of an 18-page HTML proposal to redesign the timeline. The patch succeeded on page 15 but corrupted unrelated pages (BOQ, payment) through CSS overflow clipping and content shifts. Without a backup, the only revert point was an older version missing many intermediate improvements. Don't repeat this.

---

When you delegate a task to a sub-labor, you MUST explicitly state **which one** and **why** in your response to the user. This is non-negotiable.

Format: *"I'm delegating this to **[Labor Name]** because **[reason]**."*

This applies to all non-trivial work:
- `delegate_task` calls
- `terminal()` calls running `claude -p '...'` or `kimi -p '...'`
- Any task beyond simple terminal commands

**Exception:** Trivial terminal commands (`ls`, `grep`, simple Python one-liners) and file reads don't need a labor announcement.

### Plan → Audit → Implement
Before executing any multi-step or impactful task:
1. **PLAN** — Write a design document or plan
2. **AUDIT** — Delegate the plan to a sub-labor (Claude Code recommended) for review
3. **IMPLEMENT** — Only execute after audit approval or with conditional approval applied

This prevents costly mistakes and catches edge cases early.

---

## Claude Code — Capabilities

**Model:** Claude Opus 4.7 (1M context) — the most powerful Claude model

**Active Tools (always available):**
- **Read** — reads text, images, PDFs, notebooks
- **Edit** — exact string replacements in files
- **Write** — create or overwrite files
- **Bash** — execute shell commands
- **Glob** — fast file pattern matching
- **Grep** — ripgrep-powered content search
- **Agent** — launch sub-agents (Explore/Plan/Coder)
- **Skill** — invoke named skills
- **ToolSearch** — defer-load additional tools
- **AskUserQuestion** — ask the user questions
- **ScheduleWakeup** — schedule /loop iterations

**Deferred Tools (loaded on demand):**
- WebSearch, WebFetch — web search and page fetching
- CronCreate/List/Delete — cron job management
- TaskCreate/Get/List/Output/Stop/Update — task management
- EnterPlanMode/ExitPlanMode — planning mode
- EnterWorktree/ExitWorktree — git worktree isolation
- Monitor — stream background process events
- NotebookEdit — Jupyter notebook editing
- PushNotification — send push notifications
- RemoteTrigger — trigger remote agents

**MCP Servers Connected:**
- Notion, Google Drive, Google Calendar, Gmail (all active)
- WordPress.com (needs auth)

**Key Flags:**
- `-p` / `--print` — non-interactive one-shot mode (preferred for automation)
- `--output-format json|stream-json` — structured output
- `--json-schema` — force JSON schema validation
- `--max-turns N` — cap agentic loops (print mode only)
- `--max-budget-usd N` — cap API spend
- `--allowedTools` — whitelist specific tools
- `--dangerously-skip-permissions` — auto-approve all tool use
- `--model sonnet|opus|haiku` — switch model
- `--effort low|medium|high|max` — reasoning depth
- `--worktree` / `--tmux` — isolated git worktree + tmux
- `--bare` — minimal mode (skip hooks, plugins, MCP discovery)
- `--continue` / `--resume` — session continuation
- `--mcp-config` — load MCP servers from JSON

---

## Pi Agent — Commander Role (User Preference)

Pi Agent (`@earendil-works/pi-coding-agent@0.78.0`) is an AI coding assistant with read/bash/edit/write tools. Installed at `~/.npm-global/bin/pi`. Default provider is `opencode-go`.

**User explicitly requires:** Pi Agent acts as **commander/orchestrator** that delegates to other labor CLIs (Claude Code, Codex, Kimi), NOT as a simple worker. When deploying Pi Agent, feed it the task and tell it to distribute work to the labor army.

```bash
# Delegate as commander (not just worker)
pi -p "As commander, plan and delegate: [task]. Use claude -p for deep work, codex exec for QA, kimi for quick lookups." --name "Pi Commander Session"

# Print mode (automation)
pi -p "task description"

# Interactive mode
pi "task description"
```

Good as secondary commander when you need to offload orchestration. Supports model switching at runtime (`Ctrl+P`). Path: `~/.npm-global/bin/pi`.

Note: There's a separate Python package `pi` (v0.1.2) at `~/.venvs/pi/bin/pi` which is a different tool and broken on Python 3.14 — ignore it.

## Kimi CLI — Capabilities

**Model:** Kimi-k2.6 / kimi-for-coding (262K context, thinking enabled)

**Tools:**
- **ReadFile** — read text files with line numbers, offset support
- **WriteFile** — create or overwrite files (overwrite + append modes)
- **StrReplaceFile** — precise string replacement (single/multi/regex)
- **Glob** — find files using glob patterns
- **Grep** — ripgrep content search (context, case-insensitive, multiline)
- **Shell** — bash commands with background execution and timeout
- **Agent** — delegate to sub-agents (coder/explore/plan)
- **SearchWeb** — internet search with content extraction
- **FetchURL** — fetch and extract web page text
- **ReadMediaFile** — read images and videos (up to 100MB)
- **AskUserQuestion** — interactive prompts
- **SetTodoList** — manage todo lists
- **EnterPlanMode / ExitPlanMode** — planning mode
- **TaskList / TaskOutput / TaskStop** — background task management

**Key Flags:**
- `-p` / `--print` or `--quiet` — non-interactive mode (preferred)
- `--model NAME` — override model
- `--thinking` / `--no-thinking` — toggle reasoning
- `--yolo` — auto-approve all actions
- `--plan` — start in plan mode
- `--afk` — fully autonomous (no user prompts)
- `-C` / `--continue` — resume previous session
- `-r` / `--resume ID` — resume specific session
- `--output-format stream-json` — streaming output (with --print)
- `--agent-file` — custom agent spec
- `--mcp-config` / `--mcp-config-file` — MCP servers

**Limitations:**
- Cannot switch models at runtime
- No git operations by default (needs explicit instruction)
- No MCP server auto-discovery like Claude
- Max 1000 lines per read, 2000 chars per line

---

## Step-by-Step Decomposition for Large Redesign Tasks

**User preference (June 2026):** For large page redesigns or multi-page profile overhauls, break into small sub-tasks and execute them one at a time. Do NOT send a monolithic prompt to a single labor call.

### Why step-by-step?

1. **Verifiable progress** — check each sub-task output in the browser before continuing
2. **Lower risk** — if a sub-task breaks the page, only that sub-task needs reverting, not the whole redesign
3. **Focused context** — each sub-task is small enough for the labor to handle precisely
4. **User can course-correct** — after any sub-task, the user can say "no, do it differently" without wasted work

### How to structure sub-tasks

For a page redesign (e.g., QA/QC page, Colour-Managed Print page):

```yaml
Sub-task 01: Fix page identity — update header, title, headline text
Sub-task 02: Fix hold point order — correct sequence 01→05
Sub-task 03: Rebalance layout — adjust grid columns, gaps, padding
Sub-task 04: Enlarge photos — increase image heights, add badges
Sub-task 05: Add deliverables strip — tags at bottom
Sub-task 06: Final visual QA — verify all items correct
```

### Execution pattern

```bash
# Step 1: Fix page identity
terminal(command="claude -p 'Sub-task 1: fix the page header and title... details...'", timeout=120)

# Step 2: Verify in browser / check HTML
terminal(command="curl -sL https://site/ | grep -c 'expected-text'")

# Step 3: Next sub-task
terminal(command="claude -p 'Sub-task 2: hold point order...'", timeout=120)

# Step 4: Verify again
# ...repeat until all sub-tasks done
```

### When to use

- Page-by-page profile redesigns (QA/QC, Colour-Managed Print, Materiality & Craft)
- Any multi-page content overhaul (>3 pages affected)
- When the user explicitly asks for step-by-step ("make it step by step")
- When you're unsure about design direction — sub-tasks let the user course-correct

### When NOT to use

- Single simple edits (one URL change, one photo swap)
- Mechanical bulk operations (find-replace-50-files type tasks)
- Tasks where all sub-tasks are trivially independent and can run in parallel

## Decision: Which Sub-Labor?

**PRIMARY RULE:** Codex = QC Gate (reorders + audits), Claude Code = main executor + deep research synthesis, Kimi = fast research + monkey work.
- ALL user orders go through Codex first for rewriting/structuring
- If research needed → route to fastest labor (Kimi for simple, delegate_task for parallel, Claude for deep synthesis)
- Claude Code executes the structured orders (including research findings)
- Codex audits ALL Claude Code output AND research accuracy before delivery
- Kimi handles fast web research and simple tasks directly

### 🔴 Mohamed Essa's Preferred Variant (2026-06-09)

The user explicitly stated their preferred division of labor for file generation / costing / analysis tasks:

> **"plan with codex, do with claude, KIMI is QC"**

This means:
- **Codex = Plan** — Codex creates the structured execution plan. Not just rewriting the user's order, but building the full methodology with paths, steps, categorization rules, validation criteria.
- **Claude = Execute** — Claude Code does the actual work: reads source files, creates output files, generates workbooks/documents.
- **KIMI = QC** — Kimi reviews/validates the output. If Kimi times out on large files, fall back to Python validation scripts run locally.

**When this variant applies:** Template-based multi-file generation (Excel costing workbooks), bulk document creation, repetitive file processing across N projects.

**Why the roles differ from the default:**
- Codex's planning is stronger for construction-style tasks (build a methodology → apply to N projects)
- Claude's execution is more reliable for openpyxl/docx generation
- KIMI's QC catches edge cases Codex might miss

**Signal words to use this variant:** "make File for quotation", "same methdology", "apply to all", "template for all", "cost analysis for each project".

| Task Type | Labor | Why |
|---|---|---|
| **Rewrite/Structure user order** | **Codex CLI** | QC Gate — first step in every workflow |
| **HTML & document generation** | Claude Code | Heavy template work, complex docs |
| **QA Audit of Claude Code output** | **Codex CLI** | QC Gate — mandatory before any delivery |
| **Template-based multi-file costing generation** | **Codex (plan) → Claude (exec) → KIMI (QC)** | User's explicit preferred variant |
| **Scope audit (contract vs deliverable)** | Claude Code (execute) → Codex (audit) | Two-step: Claude builds matrix, Codex verifies |
| **Fast web research (1-2 questions)** | **Kimi** | Pattern A — SearchWeb built-in, fastest startup (~2s) |
| **Parallel multi-aspect research** | **delegate_task × 2-3 subagents** | Pattern B — independent angles simultaneously with toolsets=["web"] |
| **Deep synthesis / regulatory analysis** | **Claude Code** | Pattern C — WebSearch + stronger reasoning for cross-source analysis |
| Quick checks, file sorting, data extraction | Kimi | Monkey work — fast, lightweight |
| Parallel auditing across multiple files | Codex CLI | Native HTML validation scripts |
| Git operations, PR review | Claude Code | Native git worktree, --from-pr, ultrareview command |
| General coding (fallback) | **Pi Agent** | Secondary labor when Claude Code unavailable |
| **Vision/Image Analysis (when main model can't see)** | **Kimi** or **delegate_task** | User says "let kimi read for you" — preferred fallback. Kimi has ReadMediaFile capability. Alternative: start local HTTP server → browser_navigate → browser_vision via delegate_task with toolsets=["browser","terminal","file"] |

---

## Delegation via delegate_task (Parallel / Heavy Work)

For heavy research, auditing, or multi-project work, use `delegate_task` instead of `terminal(command="claude -p ...")`:

```
delegate_task(
    goal="What the labor should accomplish",
    context="Background info, file paths, constraints",
    toolsets=["terminal", "file", "web"]
)
```

When the subagent should use the **copilot CLI** (GitHub Copilot ACP transport) instead of the parent provider:

```
delegate_task(
    goal="...",
    acp_command="copilot",           # force copilot CLI
    acp_args=["--acp", "--stdio"],   # required args
)
```

Set these env vars in `~/.hermes/.env` once to make copilot the default for all subagents:
```
HERMES_COPILOT_ACP_COMMAND=copilot
HERMES_COPILOT_ACP_ARGS=--acp --stdio
```

**Known limitation**: Copilot CLI on macOS calls the opencode-go API as its backend. If your opencode-go session quota is exhausted, delegation fails with HTTP 404. Use this only when opencode-go quota is available.

**Non-interactive subagent** (never blocks on prompts): add `--no-ask-user` to `acp_args`.

**Always mention the delegation in your response to the user.** Example:
*"I'm delegating this to **Claude Code** since it has the Odoo connection details in its project memory."*

## 🔴 CRITICAL PITFALL: Subagent HTML Structure Drift

When a subagent redesigns or rewrites an HTML file, the output may use **different class names, DOM structure, or attribute patterns** than what your subsequent injection scripts expect. This caused cascading failures in a Jun 2026 session: a subagent redesigned gallery HTML using `onclick` on divs instead of `<a>` tags, breaking injection scripts that searched for `<a>` selectors.

**Prevention:**
- Before running any transformation script against a subagent's output, **verify the DOM structure**:
  ```
  grep -o 'class="[^"]*"' output.html | sort | uniq -c | sort -rn | head -20
  ```
- Write injection scripts resilient to minor structural changes -- match on partial class names, use generic parent traversals
- After the subagent completes, verify with `wc -l` and `head -5` to confirm no truncation
- Adapt your injection to the subagent's actual output structure rather than assuming old patterns

### Sub-pitfall: Subagents Change Identifiers on Partial Redesigns

When a subagent is tasked with a **partial section redesign** (refresh styling but keep structure), it may **change badge numbering, section IDs, or page labels** that should remain stable. Example: a subagent redesigning a gallery section changed "01 / Gallery" to "05 / Gallery" because an exec summary was section 05 -- the subagent assumed badge renumbering was required.

**Prevention (add to every partial-redesign delegation goal):**
1. **Explicitly list which identifiers to preserve** in the goal: "Preserve the existing section badge (01 / Gallery), section ID (#gallery), and all data arrays. Only modify the card styling."
2. **After delegation, verify identifiers are intact** -- check section badges, page numbers, and `id=` attributes
3. **For React/TSX sections**, verify the export name and import path weren't altered
4. **Fix is usually a simple patch** if badge numbers drifted. Prevent by being explicit in the goal.

## 🔴 CRITICAL PITFALL: JavaScript `const` Does Not Create a `window` Property

When injecting JavaScript data between separate `<script>` blocks in HTML, `const MATERIAL_DATA = {...}` does **NOT** create a `window.MATERIAL_DATA` property in strict/modern JS. A subsequent script that checks `window.MATERIAL_DATA` gets `undefined`.

**Fix — use one of these for cross-script-block data sharing:**
```javascript
// Pattern A (preferred): Assign to window explicitly
window.MATERIAL_DATA = { ... };

// Pattern B: Use var (var at top level creates window property)
var MATERIAL_DATA = { ... };
```

**Why:** `const`/`let` at script top level create lexical bindings but NOT `window` properties. `var` does. `window.X =` always works.

## Parallel Build Pipeline (Pattern E)

For large multi-file projects (Next.js sites, document packages, multi-component systems), break the work into independent streams and delegate them in **parallel batches** via `delegate_task(tasks=[...])`.

### When to use
- Project initialization with multiple independent layers (setup + data + assets)
- Building a system with separate non-overlapping components (core + UI + pages)
- Any task where 3 workstreams can run simultaneously without file conflicts

### Batch structure
```
Batch 1 (all parallel):
├── Setup: Initialize project, install deps, configure build
├── Data: Create data models, types, fixtures
└── Assets: Copy/optimize images, fonts, static files

Batch 2 (all parallel):
├── Core components: Business-logic-heavy parts
├── UI components: Layout/presentation parts
└── Pages: Wire everything together
```

### Implementation
```python
# Batch 1: Independent foundations
results = delegate_task(tasks=[
    {"goal": "Initialize Next.js project...", "toolsets": ["terminal", "file"]},
    {"goal": "Create data layer with TypeScript types...", "toolsets": ["terminal", "file"]},
    {"goal": "Copy and optimize all assets...", "toolsets": ["terminal", "file"]}
])

# Batch 2: Build on top
results2 = delegate_task(tasks=[
    {"goal": "Build core components...", "toolsets": ["terminal", "file"]},
    {"goal": "Build UI components...", "toolsets": ["terminal", "file"]},
    {"goal": "Build pages...", "toolsets": ["terminal", "file"]}
])

# Final: Verify
terminal("npm run build")
```

### Critical rules for parallel builds
1. **No overlapping files** — each task must write to DIFFERENT directories. Use `src/data/`, `src/components/`, `src/app/` separation.
2. **Run `npm run build` after ALL batches** — individual tasks compile in isolation but integration reveals import/type mismatches.
3. **Share context** — each task needs the project root path and awareness of other tasks' output locations for consistent imports.
4. **Limit to 3 concurrent tasks** — respects `max_concurrent_children=3` configured limit.

### Proven result (Jun 2026)
A full Next.js 14 interactive site (13 pages, 8 components, 4 data modules, 107 images) was built in 3 parallel batches x 2 phases = ~8 minutes total wall time vs ~30+ minutes sequentially.

**User confirmed pattern:** said "you kan make todo list and delegate tasks in parellel to solders" — the user's preferred approach for large multi-file builds.

## Delegation Patterns

### Claude Code — Print Mode (Preferred)

```
terminal(command="claude -p 'task' --allowedTools 'Read,Edit,Write,Bash,Glob,Grep' --max-turns 10", workdir="/path", timeout=120)
```

### Claude Code — JSON Output (Proven for Long Tasks)

For tasks that take 3-8 minutes (multi-file generation, analysis), the `--output-format json` flag is essential:

```bash
claude -p "Create 13 Excel workbooks following this plan..." --max-turns 40 --output-format json
```

**Why JSON mode:** Returns a structured result with `session_id`, `num_turns`, `total_cost_usd`, `duration_ms`, and the actual `result` text. This lets you track cost and turn count for long-running tasks.

**Proven parameters (2026-06-09):**
- Task: Create 13 costing Excel workbooks from diverse source files (xlsx, xls, docx)
- Turns: 15 (within --max-turns 40)
- Duration: ~458s real time, ~387s API time
- Cost: ~$4.30 (Opus, 3.6M cache read tokens)
- Result: All workbooks created and validated with correct totals

**Key tips for long print-mode tasks:**
- Set `--max-turns` high enough (40+ for complex tasks) — Claude may need many turns to read sources, write code, run it, debug, re-run
- Set `--timeout 600` on the terminal call
- Parse the JSON result with `2>&1 | tail -50` to get the summary at the end
- The `result` field contains Claude's final message
- `num_turns` tells you if you need to increase `--max-turns` next time

### Claude Code — Interactive via tmux (Multi-turn)

```
terminal(command="tmux new-session -d -s claude-task -x 140 -y 40")
terminal(command="tmux send-keys -t claude-task 'cd /path && claude' Enter")
terminal(command="sleep 5 && tmux send-keys -t claude-task Enter")  # trust dialog
terminal(command="tmux send-keys -t claude-task 'Main task prompt here' Enter")
terminal(command="sleep 30 && tmux capture-pane -t claude-task -p -S -50")
terminal(command="tmux kill-session -t claude-task")
```

### Codex CLI — Invocation Patterns (QC Gate)

Codex is the Quality Controller. Use it to audit ALL Claude Code output before delivery.

### Codex — One-Shot Task (via terminal)

```bash
codex exec "task description" --sandbox workspace-write
```

Note: `--full-auto` is deprecated in favor of `--sandbox workspace-write`.

### Codex — QA Audit (HTML verification with Python scripts)

Codex is particularly good at running validation scripts on HTML files:

```bash
codex exec "Read file X.html and create a QA report at /tmp/report.md listing all HTML quality issues: div balance, missing tags, doctype, font loading, @page CSS, sheet sizing, logo paths, line number contamination" --sandbox workspace-write
```

### Codex — Must run inside a git repo

Codex refuses to run outside a git directory. Create a scratch repo for standalone tasks:

```bash
cd $(mktemp -d) && git init && git add -A && git commit -m "init" && codex exec "task" --sandbox workspace-write
```

### Codex — Background mode (long tasks)

```bash
terminal(command="codex exec '...' --sandbox workspace-write", workdir="/path", background=true, pty=true)
# Monitor with process(action="poll"), get results with process(action="log")
```

### Codex — Key Limitations

- **PTY required** — Codex is interactive; use `pty=true` in terminal calls
- **Git repo required** — refuses to run outside one
- **Cannot use via ACP delegate_task** — delegate_task ACP transport fails with "stdin is not a terminal"
- **Model:** gpt-5.5 (OpenAI), reasoning effort: medium

---

### Vision Delegation Pattern (When Main Model Cannot See Images)

**Signal:** User attaches an image (photo, CAD elevation, screenshot) but the active model lacks vision support. The user may say "let kimi read for you."

**Options (in order of user preference):**

**Option A — Kimi CLI directly (user's preferred fallback):**
```bash
kimi -p "Describe this image in full detail for [purpose]" -f /path/to/image.jpg --quiet
```
Kimi has native `ReadMediaFile` capability — no browser workaround needed. Works for JPEG, PNG, HEIC up to 100MB.

**Option B — delegate_task with browser+vision:**
For subagents that have browser tooling but no image-attachment support:
```python
delegate_task(
    goal="Describe this [item] in full detail for [purpose]",
    context=f"""
Image path: {path}
Method: 1) Start Python HTTP server in /tmp
        2) Copy image to /tmp/ 
        3) Navigate browser to localhost
        4) Use browser_vision to analyze
Provide: components, proportions, materials, joinery, finish, hardware
""",
    toolsets=["browser", "terminal", "file"]
)
```
Works when Kimi is unavailable or when the analysis needs to merge with other subagent results.

**Option C — Claude Code (for deep analysis + synthesis):**
```bash
claude -p "Analyze this joinery CAD elevation..." -i /path/to/image.jpg --max-turns 10
```
Claude Code handles images natively. Good for complex images needing multi-step reasoning (e.g., cross-referencing drawing annotations with a spec sheet).

**Pitfalls:**
- Kimi's `--quiet` times out on prompts >500 chars → use `--print` for long prompts, parse `text='...'` from output
- Browser_vision may also fail if the subagent's model lacks vision → try the other option
- For CAD elevations: pixel-level edge density analysis (Python PIL) can reveal structure even without vision — horizontal bands = shelves/countertops, vertical columns = supports/panels
```python
from PIL import Image, ImageFilter
img = Image.open(path).convert('L')
edges = img.filter(ImageFilter.FIND_EDGES)
```

### Kimi — Print Mode (Preferred)

```bash
echo "prompt" | kimi --print 2>&1
```

**IMPORTANT:** Kimi's `--print` flag outputs the full protocol JSON — not just the response. To extract Kimi's actual answer text, grep for `text='...'` in the output, or use `--quiet` for short prompts.

**Flag behavior (learned 2026-05-28):**
- `--quiet` (or `-p` with no flag) — cleaner output but **times out on long prompts** (>30s). Use only for trivial prompts (<500 chars).
- `--print` — shows full debug protocol but works reliably on long prompts. Pipe output through a parser.
- `--print --quiet` — contradictory flags; can cause immediate exit.
- ✅ **Best practice for long prompts:** Pipe stdin with `cat << 'EOF' | kimi --print` and parse the `TextPart(text='...')` sections from the output.
- ❌ **Avoid:** passing file paths for Kimi to read via its ReadFile tool if the prompt is long — the combined ReadFile+response cycle can timeout. Pipe the file content directly instead.

**Session continuation:** Kimi outputs `To resume this session: kimi -r <session-id>` at the end of each run. Save this for multi-turn conversations.

### Kimi — With File Attachments

```
terminal(command="kimi -p 'analyze this' -f file1.py -f file2.py --quiet", workdir="/path")
```

### Kimi — Plan Mode

```
terminal(command="kimi -p 'plan this implementation' --plan --quiet", workdir="/path")
```

### Kimi — Autonomous AFK Mode

```
terminal(command="kimi -p 'task' --afk --quiet", workdir="/path")
```

### ⚠️ Kimi Timeout on Large Files

Kimi's ReadFile + response generation routinely times out (>60s) on files >30KB or combined prompt+read cycles. Proven 2026-05-28 with ~50KB HTML files.

**Workarounds:**
1. **Pipe content via stdin** instead of passing a file path:
   ```bash
   cat /path/to/file.html | kimi --print 2>&1 | python3 -c "import re,sys;d=sys.stdin.read();print(re.findall(r\"text='([^']*)'\",d)[-1])"
   ```
2. **Use `--print` (without `--quiet`)** — `--quiet` causes immediate exit on long prompts. `--print` shows full protocol but works reliably.
3. **For files >50KB** — skip Kimi. Use Claude Code for both audit rounds.
4. **Do NOT pass file paths** for Kimi to read via its ReadFile tool when the file is large — the combined ReadFile + response cycle exhausts the session timeout.

---

## Enterprise Integration Patterns

### Odoo ERP — Delegate to Claude Code

Two Odoo instances are accessible via Python XML-RPC + certifi:

| Instance | URL | Odoo | User |
|---|---|---|---|
| **Samaya Inv.** | samayainv.odoo.com | 18 | sultan@samayainvest.com | POs, invoices, accounting |
| **Moqtana Factory** | 167.99.224.43:8069 | 18 | mohamedsultanabbas@gmail.com | Projects, manufacturing, inventory |
| **Dawam Tech** | dawam-tech.odoo.com | 19 | sultan@dawamtech.com | (separate entity) |
| **Dawam Tech** | dawam-tech.odoo.com | 19 | sultan@dawamtech.com | |

**Credentials:** Samaya creds at `~/.config/samaya/odoo.env` (mode 600). Dawam details in Claude's project memory at `~/.claude/projects/*/memory/reference_odoo_dawam.md`.

**Delegation pattern (query POs, projects, vendors):**
```
terminal(command="claude -p 'Read creds from ~/.config/samaya/odoo.env. Connect to samayainv.odoo.com via XML-RPC with certifi SSL context. List all active projects and their POs for project ID [X].' --allowedTools 'Read,Bash' --max-turns 5", timeout=120)
```

### Notion — Two Access Paths
1. **Through Claude Code MCP** (claude.ai Notion) — delegate for complex operations
2. **Direct API** via `NOTION_API_KEY` in `~/.hermes/.env` — use curl or the `productivity/notion` skill

### Environment Discovery — Using Claude Code's Project Memory

When you need to find **user-specific connection details** (Odoo URLs, database names, API endpoints, credential file locations) — delegate to **Claude Code** to search its own project memory and configs:

```
terminal(command="claude -p 'Search your project memory, ~/.claude/projects/*/memory/, and all config files for [topic]. Report all findings with file paths.' --allowedTools 'Glob,Grep,Read' --max-turns 5", timeout=120)
```

Claude Code stores project context in `~/.claude/projects/*/memory/` — this includes Odoo connection references, database configurations, API endpoints, and verified model IDs.

**Use this pattern for:** Odoo, databases, API endpoints, SaaS credentials, MCP server configs, environment-specific URLs, and any other connection detail that may have been configured in a past Claude session.

**Pitfall:** Do NOT put API keys/secrets in skill files or reference docs. Claude's discovery can find the *locations* of credential files (e.g., `~/.config/samaya/odoo.env`) but the secrets themselves stay in those files.

**Username correctness is critical.** Always verify exact email format from the credentials file or Claude's project memory rather than assuming the hyphenation (e.g., dawamtech.com vs dawam-tech.com). The URL may have a hyphen but the email may not — don't guess, have Claude look it up.

---

## Parallel Delegation Pattern

For tasks that can be split into independent workstreams:

```
terminal(command="claude -p 'part A' --allowedTools 'Read,Edit,Bash,Write' --max-turns 10", workdir="/path", background=true, notify_on_complete=true)
terminal(command="kimi -p 'part B' --quiet", workdir="/path", background=true, notify_on_complete=true)
```

Then process(action="wait") on both and synthesize results.

---

## Available Reference Files

| File | Purpose |
|------|---------|
| `references/html-qa-checklist.md` | Codex CLI QA checklist for HTML deliverables |
| `references/notion-pm-audit.md` | Notion project page PM audit methodology |
| `references/react-section-redesign-workflow.md` | React section redesign via delegate_task - parallel batch workflow, identifier preservation, verification checklist |
| `references/memory-skills-exchange.md` | Memory and skills exchange cronjob - auto-syncs all 8 labors every 6h |
| `references/update-memory-protocol.md` | Multi-store sync for "update memory" |
| `references/downloads-organization-pattern.md` | Full 7-phase workflow for "check Downloads" / file organization tasks |
| `references/scope-audit-checklist.md` | Contract scope audit checklist (Aseer Museum) |
| `references/pptx-hotspot-extraction-pattern.md` | 🆕 Extracting PPTX callout positions → interactive 3D render hotspot viewer with proximity pins and rich tooltips |
| `references/print-pdf-portal-pattern.md` | 🆕 React print-to-PDF via createPortal: CSS page-break rules, A4 sizing, fixed-position pitfalls, Vite build hang workaround |
| `references/project-cost-reallocation.md` | 🆕 Cross-project cost reallocation: inventory → identify misallocations → split rules → update FCAs → audit trail |
| `references/html-tree-expansion.md` | Expanding HTML deliverable tree categories with sub-deliverables — Python generation, file insertion, counter updates, pitfalls |
| `references/outlook-applescript-email-search.md` | Proven AppleScript patterns for searching Outlook inbox (by sender, by keyword), performance data, known issues, and noise filtering |
| `references/folder-standardization-pattern.md` | Template-based folder reorganization: study reference → inventory → apply structure → classify files → preserve → README → audit → fix |
| `references/pep-stage-gate-workflow.md` | 🆕 Building bilingual Stage-Gate Project Execution Plans: full pipeline from concept extraction through Codex rewrite → research → Claude Code build → Codex audit → overflow test → delivery |
| `references/aseer-showcase-naming-convention.md` | 🆕 NRS showcase/cabinet naming patterns (Type-2, ID.Nr.08, A2742-18XX, SC_01) — detect misplaced Aseer files in other project folders |
| `references/construction-submittal-register-pattern.md` | 🆕 Building Excel submittal registers for construction subcontractors: item structure, stage masks, category headers, long-lead rules, common pitfalls |
| `references/chunked-write-fallback-pattern.md` | 🆕 Chunked write_file + patch fallback for when delegate_task times out on large document generation (>8K-token arguments) |
---

3. Monitor background processes with `process(action="poll")` / `process(action="wait")`
4. Clean up tmux sessions when done
5. Report sub-labor results back to the user — summarize what was done, what changed
6. Kimi `--quiet` is preferred over `--print` for cleaner output
7. Claude's `--dangerously-skip-permissions` skips all permission dialogs — use with trusted tasks only
8. Claude's MCP servers (Notion, Gmail, etc.) can be leveraged for cross-platform tasks
11. Kimi's `--afk` mode is fully autonomous — best for long-running background tasks
12. Both support session continuation (`-C` / `--continue`) for iterative work
11. **Codex via PTY only
