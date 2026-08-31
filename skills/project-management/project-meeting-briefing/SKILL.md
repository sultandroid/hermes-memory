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

## Live / incremental meeting capture (voice-transcribed notes)
When the user is **in a live meeting** (e.g. design tracking with CG + PMC) and feeds points as a stream of voice-transcribed messages, capture incrementally rather than waiting for the end. Full step-by-step workflow in `references/live-meeting-notes.md`:
- **One discussion file per meeting**, created on the first batch, then **appended** on each subsequent batch — do NOT create a new file per message.
- **Number the sections** (`## 1.`, `## 2.`, …) so later batches append cleanly after the last section.
- **Append new action rows** (DT-1, DT-2, …) to the same `## Actions` table in the discussion file AND to the matching section in `00_Status/action_items.md` — keep the two in sync.
- **Commit per batch** (not once at the end) so each increment is a recoverable checkpoint. Use a descriptive message naming the meeting + the new topics.
- **Interpret, don't transcribe.** Voice-to-text output is messy (fragments, wrong words, dropped names). Reconstruct the intent in clean engineering language. When a term is genuinely ambiguous (e.g. "4 vP samples"), ask the user to clarify rather than guessing — flag it explicitly in your reply.
- **Update related discussion files too.** If the new meeting adds facts to an earlier discussion (e.g. structural core-test results update the structural-cloud-survey discussion), append an "Update — <meeting>" section to that file and cross-link.
- **Update the INDEX.md** row for the meeting as it grows (or add the row on first batch).

## End-of-meeting "remind me of all requests" deliverable
The user often asks at the end of a live meeting: **"ابقي فكرني فالاخر باي حاجه بيطلبوها"** (remind me at the end of everything they requested). This is a distinct deliverable from the discussion file:
- **Maintain a running list of the other party's requests/commitments** as you capture each batch — don't reconstruct it from memory at the end.
- **Present it grouped by urgency**: due-soon (with the nearest deadline called out) vs open/TBC.
- **Call out the 2–3 nearest-deadline items** explicitly (e.g. "quantities due today/tomorrow", "50% back to 10-Sep before next review").
- Offer a follow-up (cron reminder or a follow-up email to CG/PMC listing the commitments) — the user values both.
- The discussion file is the *record*; the reminder list is the *action summary* — produce both.

## Capture the discussion back to the repo (mandatory)
After the meeting/call, use the **`discussion-capture`** skill to persist the notes, decisions, and actions:
- `09_Agent_Workspace/discussions/YYYY-MM-DD_<slug>.md` + INDEX row + `action_items.md` rows.
- Live per-discipline tracker updates go in `02_Schedule/<Discipline>/`.
- Commit with the date in the message (project convention).

**Pitfall — never add a cross-link to a MOM file that does not exist yet.** When you add a `Related Context` cross-link in a tracker (e.g. `design_phase_deliverables_tracker.md` → `04_Docs/08_Meeting_Minutes/08.2_Workshops/2026-08-26_Showcase_Coordination_MOM.md`), you MUST create that file in the same commit. A dangling link (referenced but never written) is worse than no link — it sends the next agent on a long search for "the notes" that were never captured. If the meeting notes are genuinely unavailable (locked Read AI recap, no transcript), write a stub file stating the meeting happened + what is known (from the tracker/email preview) and mark the gap, rather than leaving a broken pointer. Verify the target file exists before committing any cross-link.

## Pitfalls
- **Never cite a stale summary as current.** Read the tracker + register first.
- **"Submitted" ≠ "approved" ≠ "rejected".** Use the exact Code (A/B/C/D/DA).
- **Disambiguate near-identical doc names** before claiming approval status.
- **A party's stated blocker may be an excuse** — verify against the actual state (e.g. "blocked on power" when power was already submitted).
- **Cost/safety/client-obligation items are the highest-value talking points** — surface them first (e.g. a pump replacement ≈ SAR 350–650K, a smoke curtain ≈ SAR 300–400K, a missing building license that is the owner's obligation).
- **The user wants NEW topics each meeting** — if the same points recur, say so and push for the genuinely-new issue (e.g. "only the structural one is new; everything else is old/repeated").

## Aseer-specific source map
See `references/aseer-source-map.md` for the per-discipline tracker paths, master registers, Outlook query targets, and the recurring meeting topics (Fire Alarm stamp chain, AD excuses, FF pump VO, skylight/atrium, rigging, structure, doors/hardware).

## Variation Order claims
When a meeting surfaces a costly change the owner/consultant drove, see `references/variation-order-claim-framework.md` for the claim-construction logic: impact-originates-from-owner, the four pillars (hidden item / costly / document-priority / owner-obligation gap), the "present the problem not the solution" tactic, verbatim Aseer contract clauses, and the report structure.

## PM adjudication — weighing two parties' positions
When the user (acting as PM/TO) weighs a supplier's "we're blocked, awaiting replies" against the designer's "it was already resolved", produce a structured verdict, not a side:
- **State the balance of the argument** — e.g. "tips toward the designer on this point, not because the consultant is technically wrong, but because the questions raised don't justify the size of the delay."
- **Apply an explicit professional standard** (state it openly):
  | Situation | Ruling |
  |---|---|
  | Missing info does NOT block 50% DD; a documented Assumption can be placed | Delay on the DESIGNER |
  | Missing info radically changes the design → major redesign or contractual risk | Clarification justified |
- **Check for pattern, not just the incident** — is the blocker a one-off or a recurring behavior (no date commitment, "we try our best", a stated blocker already satisfied)? Pattern tips the verdict further.
- **List the exact evidence still needed for a final judgment** (meeting minutes cited, contract DD conditions, RFI register + response dates, baseline schedule + recovery plan) so the decision is provable, not asserted.
- **Give an operational move** to shift the burden of proof (e.g. "direct issue of 50% DD now with documented assumptions + RFI in parallel").
This verdict belongs in the discussion file + an action item (e.g. `AD30-18`), and is institutional memory for the next such dispute.
