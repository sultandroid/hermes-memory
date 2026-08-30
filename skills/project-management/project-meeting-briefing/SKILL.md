---
name: project-meeting-briefing
description: Prepare internal project meeting talking points / status briefings from the repo. Read the per-discipline tracker + registers (NOT the stale summary status file) before citing any number or status. Verify each claim against its source, then capture the discussion back to the repo. Use when the user asks "what do I say in the meeting", "give me the points", or is preparing for an internal coordination call.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [meeting, briefing, status, aseer, coordination]
    related_skills: [discussion-capture, submittal-register-management, project-status-publishing]
---

# Project Meeting Briefing — Talking Points from the Repo

## When to Use
- User asks "what do I say in the meeting", "give me the points", "نقاط أتكلم فيها", or is preparing for an internal coordination call / progress meeting.
- User wants a status summary of a discipline (electrical, structural, AV, acoustics, graphics, etc.) before a meeting.
- User is about to defend a position (e.g. "why hasn't demolition started", "we have an approved demolition plan") and needs the factual basis.

## Core Rule — VERIFY FROM SOURCE, NOT THE SUMMARY
The single biggest failure mode: citing the **stale summary status file** (`00_Status/project_status.md`, `master_dashboard.md`) as if it were current. These are auto-generated snapshots and lag the live registers. **The user WILL correct you** if you cite a number/status that the per-discipline tracker or register has since updated.

**Always read, in this order, before stating any number or status:**
1. **Per-discipline submission tracker** — `02_Schedule/<Discipline>/` (e.g. `AD_Engineering/`, `Rigging_Contractor/`, `Acoustic_Specialist/`). These hold the live per-package status (Code A/B/C/D, dates, "submitted today").
2. **`01_Registers/submittal_register.md`** — the master submittal log with CG response codes and dates.
3. **`00_Status/action_items.md`** — open actions, owners, due dates.
4. **Outlook SQLite** (via `outlook-data-extraction` skill) — for "what was submitted today" / latest CG replies / who said what. The email DB is often the freshest source.
5. Only then the summary files (`project_status.md`, `master_dashboard.md`) — as a cross-check, never as primary evidence.

**Pitfall — "X hasn't submitted" is a claim that needs proof.** Before saying a discipline is behind, check the tracker for recent submissions (e.g. electrical may have submitted Fire Alarm + Power outlets in the last week even if the overall % is low). Distinguish "nothing submitted" from "submitted but rejected (Code C/D)" from "submitted, awaiting CG".

## Distinguish the THREE different things that share a name
Project docs often have near-identical names for different items. Before answering, disambiguate:
- **Demolition plan** vs **demolition routing plans** vs **dismantling-for-cloud-survey** vs **waste-management SI** — different documents, different approval statuses. "We have an approved demolition plan" is only true for the specific one that is Code B.
- **Approved (Code B)** vs **submitted/under review** vs **rejected (Code C/D)** — never conflate. A "submitted" item is NOT approved.
- **Deemed Approved (DA)** = CG silent >14 days per ER §2.4.A — a distinct status, not "approved".

## Structure the briefing (verdict-first, per user style)
- **Lead with the 3–5 critical items** (red flags, cost, safety, client-obligation gaps) — not a flat list.
- **Table per discipline**: item | status | next step / owner / due.
- **Separate "what's actually blocking" from "excuses"** — the user values calling out when a party's stated blocker is refuted (e.g. "power already submitted, so nothing blocks them").
- **Give the exact defense line** the user can say verbatim in the meeting, with the doc refs to back it.
- **Flag what NOT to claim** (e.g. "we have an approved demolition plan" when the routing plan is still under review) — a wrong claim in a meeting is worse than no claim.

## Capture the discussion back to the repo (mandatory)
After the meeting/call, use the **`discussion-capture`** skill to persist the notes, decisions, and actions:
- `09_Agent_Workspace/discussions/YYYY-MM-DD_<slug>.md` + INDEX row + `action_items.md` rows.
- Live per-discipline tracker updates go in `02_Schedule/<Discipline>/`.
- Commit with the date in the message (project convention).

## Pitfalls
- **Never cite a stale summary as current.** Read the tracker + register first.
- **"Submitted" ≠ "approved" ≠ "rejected".** Use the exact Code (A/B/C/D/DA).
- **Disambiguate near-identical doc names** before claiming approval status.
- **A party's stated blocker may be an excuse** — verify against the actual state (e.g. "blocked on power" when power was already submitted).
- **Cost/safety/client-obligation items are the highest-value talking points** — surface them first (e.g. a pump replacement ≈ SAR 350–650K, a smoke curtain ≈ SAR 300–400K, a missing building license that is the owner's obligation).
- **The user wants NEW topics each meeting** — if the same points recur, say so and push for the genuinely-new issue (e.g. "only the structural one is new; everything else is old/repeated").

## Aseer-specific source map
See `references/aseer-source-map.md` for the per-discipline tracker paths, master registers, Outlook query targets, and the recurring meeting topics (Fire Alarm stamp chain, AD excuses, FF pump VO, skylight/atrium, rigging, structure, doors/hardware).
