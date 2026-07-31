# Rules & Conventions

## Golden Rules
- **Never ask permission** — baseline first, reality later
- **Always verify scope** before adding activities
- **Source-verifiable** — never assert without a doc reference
- **English-only** for formal output
- **Omit or flag TBC** rather than infer
- **Confirm task completion** — report what was done, changed, issues — never "ok done"

## NEVER Do
- `rm -rf` any path (OneDrive propagates immediately)
- Create new Excel files for registers (only append rows)
- Move unknown/non-project files from Downloads
- Reference /tmp paths in Odoo descriptions
- Auto-update sibling registers unless explicitly asked

## Entity Isolation

Samaya folders must NEVER contain Moqtana/Tqanny/Sada_Uhud/Sayyid al-Shuhada files, and vice versa.

### Entity Isolation Matrix

Each entity is fully isolated. Do not cross-reference, share files, share branding, or assume shared context.

| Entity | Owner | Branding | Repo / root path | Notes |
|---|---|---|---|---|
| **Samaya** | Eng. Mohamed Sultan (Tech Office Mgr) | Samaya Investment | `Bim Unit/`, `~/projects/*-workspace` | Work — primary employer |
| **Amjad Consultancy (ACG)** | External advisor | Amjad ACG | `~/projects/acg-*` (when created) | Consulting — bilingual submittals |
| **Sultan House (B210)** | Personal | None — use `CONFIDENTIAL` | `~/projects/sultan-house/` (when created) | Personal — land210.vercel.app |
| **Moqtana** | Separate entity | Moqtana | OneDrive-Personal | NEVER in Samaya paths |
| **Tqanny** | Separate entity (8 sub-projects: Darin, Shobra, Albiaa, Al Faw, Alrakaa, Antara, Said Alshohadaa, Tabuk) | Tqanny | `OneDrive-Personal(2)/Work/PWork/01_PROJECTS/Tqanny_Projects/` | NEVER in Samaya paths |
| **Sada_Uhud** | Separate entity | Sada_Uhud | (separate OneDrive) | NEVER in Samaya paths |
| **Sayyid al-Shuhada** | Separate entity | Sayyid al-Shuhada | (separate OneDrive) | NEVER in Samaya paths |
| **RCRC** | External client | RCRC Exhibition | `sultandroid/RCRC-Exhibition-Proposal` | Consulting — separate repo |

**Rule:** before touching a file, check which entity it belongs to. If unclear, ask. Cross-entity file movement is a `RULES.md` violation.

## Excel Style
- Formulas, number formatting (never "SAR" as text)
- Navy headers (#1E293B) with white text
- Alternating white/light rows
- openpyxl

## Schedule Audit
- File ending at IFC gate = design-phase-only, NOT full project
- Look for "DESIGN PHASES" in name
- Activity prefixes: PE/AS/EN/PR (design) vs CN/IN/TC/HD (construction)
- Check contract completion date before flagging unrealistic timelines
- OneDrive-locked PDFs → use EXTRACT_*.md in 07.5 Audit Report instead

## Communication
- Short directives, no fluff
- English for formal output
- Arabic OK for direction
- Inline Telegram text preferred (MEDIA: doesn't arrive)

## Daily Routine

The agent's session ritual — read on wake, write on close.

### On Wake (every session start)

1. `cd ~/hermes-memory && git pull --no-rebase` — pull hub identity
2. Read in order: `USER.md` → `RULES.md` → `MEMORY.md` → `AGENTS.md` → `PROJECTS.md` (per `AGENTS.md` §2)
3. Identify which project the user is asking about. `cd` into that project repo.
4. Read that project's `AGENTS.md` + `_Project_Memory/PROJECT_MEMORY.md`
5. State a one-line summary of who the user is + what project is in scope before doing work.
   Example: *"User: Eng. Mohamed Sultan, Tech Office Mgr · Project: Aseer Museum (WORK) · Mode: design package review"*

### On Close (every session end)

1. Append any **cross-project** facts learned this session to hub `MEMORY.md` with timestamp prefix:
   `[YYYY-MM-DD AGENT:hermes] New fact here.`
2. Append any **project-specific** facts to that project's `_Project_Memory/PROJECT_MEMORY.md`.
3. **Never** push credentials, project deliverables, or session chatter to the hub.
4. Commit + push any project repo changes: `git add -A && git commit -m "..." && git push origin main`.
5. Report what was done, what changed, what issues remain (per Golden Rule §"Confirm task completion"). Never "ok done".

### When to Push Back to Hub (trigger list)

Push only on:
- ✅ End of session, if a reusable fact was learned
- ✅ Explicit user request: "remember this", "add to memory"
- ✅ New contact / role mapping discovered
- ✅ New tool pattern / pitfall discovered

Never push:
- ❌ Mid-session chatter
- ❌ Project-specific facts (those stay in project repo)
- ❌ Unverified guesses (`RULES.md` says source-verifiable)
- ❌ Credentials of any kind
