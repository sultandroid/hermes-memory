---
name: discussion-capture
description: Capture project discussions into structured repo files — extract notes, decisions, and actions, and link them to their source (Outlook emails, CG submittals, registers). Use when a meaningful project discussion/analysis happens and the user wants it recorded so it stays useful.
---

# Discussion Capture — Structured Decision Records

Turn meaningful project discussions/analyses into reusable, linked repo files so the output is not lost. Triggered by the user saying "ارفع نتايج المناقشة على الريبو", "عمل سيستم للنقاشات", "وثّق القرار ده", or any substantive analysis that should persist.

## Core principle

A discussion file that just sits in a folder is useless. Every captured discussion must be **linked** back to its source AND to the registers it affects. Three-way linking: discussion → registers, registers → discussion, and a central INDEX.

## Where files live

```
09_Agent_Workspace/discussions/
├── INDEX.md                    # Central table of all discussions
└── YYYY-MM-DD_<short-slug>.md  # One file per discussion
```

Slug: lowercase, hyphens, ~40 chars max (e.g. `2026-08-27_structural-cloud-survey`).

## File template (frontmatter)

```yaml
---
date: YYYY-MM-DD
topic: <short title>
participants: [Eng. Mohamed Sultan, Hermes, ...]
source_emails: [<Outlook Record_RecordID>, ...]
source_docs: [<ZD-0106>, <PQ-0121>, ...]
status: active | resolved
---
```

## Body structure (in order)

1. **`# <Topic>`** — title matching the slug
2. **TL;DR** — one-paragraph verdict up front (mirrors the "verdict-first" reply style)
3. **Background / the question** — why this discussion happened
4. **Notes** — the actual findings/observations with evidence (doc refs, dates, sources)
5. **`## Decisions`** — table: `| # | Decision | Decision Maker | Linked To |`
6. **`## Actions`** — table: `| # | Action | Owner | Status | Linked To |`
7. **`## Sources`** — emails (Outlook IDs), CG submittals, daily reports, registers
8. **`## Related refs`** — cross-references to other docs

## Three-way linking (MANDATORY)

1. **Discussion → registers:** every decision/action row has a `Linked To` column pointing to the register + row (e.g. `` `01_Registers/submittal_register.md` (ZD-0106) ``).
2. **Registers → discussion:** add a reference to the discussion file in the affected register row(s) — e.g. update the ZD-0106 row in `submittal_register.md` to append "Decision log: `09_Agent_Workspace/discussions/...md`". Also update `action_items.md` rows and `handoff_log.md`.
3. **INDEX.md:** add one row per discussion (Date, Topic, File, Key Decision/Outcome, Linked Registers, Status).

## After capturing — commit

```bash
cd /Users/mohamedessa/aseer-museum-pm
git add 09_Agent_Workspace/discussions/ <edited registers> handoff_log.md
git commit -m "docs: <topic> discussion + register links <YYYY-MM-DD>"
```

Use `git mv` if relocating an existing file (preserves history). Include the date in the commit message per project convention.

## Pitfalls

- **Never leave a discussion file unlinked.** If you only wrote the file, you did half the job — link it to registers + INDEX + handoff_log.
- **Update register status codes too.** Capturing a discussion often reveals a status change (e.g. ZD-0106 "awaiting CG" → "Code B"). Update the register row in the same commit.
- **`git mv` to relocate** an existing file rather than `cp`+`rm`, so git history is preserved.
- **Use `sed -i ''` for bulk path updates** across several files when a file moves (macOS syntax), then verify with `grep -c`.
- After editing register files, watch for the sibling-subagent `_warning` — re-read before writing to avoid clobbering concurrent edits (see outlook-email skill).
- Repo rule: append-only for registers; never delete rows — mark `superseded`/`closed`.
