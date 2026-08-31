# Live Meeting-Notes Capture (voice-transcribed)

Pattern for when the user is **in a live meeting** and feeds you the notes as a stream of short, messy, voice-transcribed messages (often Arabic + English mixed, garbled names, run-on sentences). They expect you to structure and persist each batch as it arrives.

## When this applies
- User sends multiple short messages that are clearly meeting dialogue (e.g. "Mr. Waris, we have some overdue dates at EV...", "Regarding the fire alarm system, it has not yet been received from Samaetel...").
- They say things like "ابقي فكرني فالاخر باي حاجه بيطلبوها" (keep reminding me at the end of anything they asked for) — i.e. they want a running "asks from us" list.
- They say "حدث نقاش الاستركشر برضوا او اي معلومات محتاجه تتحدث في اي مكان" (update the structural discussion too, or any info that needs updating anywhere).

## Workflow
1. **Create one discussion file** for the whole meeting (e.g. `2026-08-31_design-tracking-cg-pmc.md`) with frontmatter `date`, `topic`, `participants`, `status: active`.
2. **Append a numbered section per topic** as each message batch arrives (`## 1.`, `## 2.`, ...). Keep the file growing in place — do NOT rewrite from scratch.
3. **Maintain an `## Actions` table** at the bottom, adding a new `DT-N` / `MTG-N` row per action. Number sequentially across the whole meeting.
4. **Commit after each batch** (or every 2-3 batches) with a dated message naming the topics covered. Incremental commits keep the record recoverable and match the user's "always include YYYY-MM-DD" convention.
5. **Cross-reference Outlook emails** to enrich: query the SQLite DB for subjects matching the meeting topics (overdue deliverables, geotech, FLS, etc.), read the bodies, and fold the authoritative data (e.g. CG's overdue-deliverables table, a submittal's Code B status) into the discussion file. This turns live notes into a verified record.
6. **Update the linked discussion** (e.g. the structural-cloud-survey file) with a "Update — <meeting>" section when the meeting adds new info to an existing topic.
7. **Update `action_items.md`** with the same rows (mirror the discussion's Actions table), and add a row to `discussions/INDEX.md`.

## Handling noisy voice transcription
- **Interpret garbled names/terms** from context and note the interpretation, e.g. "Dougan-Beliz" → Dogan Kozan (ZNA lighting), "NANAT" → Namaa (FLS), "CJEA" → CG, "Mr. Pass/Paz" → Eng. Paz (unconfirmed).
- **Flag uncertain items back to the user** rather than silently guessing. Keep a short "ملاحظة" (note) at the end of your reply listing what you couldn't resolve (e.g. "4 vP samples — what is this exactly?").
- **Preserve the speaker's role** when identifiable (e.g. "Eng. Rashed (AD)", "General Adel (CG)", "Mr. Dougan (ZNA)") — it matters for who owns the action.
- When a message is a **reply/agreement** to a prior point, fold it into the existing section rather than creating a new one.

## The "asks from us" list (user request)
When the user asks to be reminded of what the other party requested, produce a **prioritized summary** of every ask/commitment from the meeting, with the most time-sensitive flagged (e.g. "⏰ quantities — today or tomorrow", "⏰ 50% — before next review"). Offer to set a cron reminder or draft a follow-up email.

## "Pull more details" — drill into the tracker for a per-system breakdown
When the user asks **"ممكن تطلع تفاصيل اكتر"** (can you pull more details) on a delay/overdue count, don't just restate the aggregate number. Read the per-discipline detail sheet in `01_Registers/design_phase_deliverables_tracker.md` (sections like `## 9. Electrical Deliverables (Detail)`, `## 11. Low Current & ICT Deliverables (Detail)`) and produce a **per-system table**: system | item count | status (Code C / In Progress % / Not started) | forecast date. This turns "49 electrical overdue" into a defensible breakdown (e.g. Fire Alarm 9 all Code C, Emergency/Standby 10 not started, LV Power 12 not started) that shows exactly where the block sits. Fold the breakdown into the impact-analysis file as its own numbered section.

## The "connect everything" impact analysis (user request)
When the user says **"ربط الدنيا مع بعض"** (connect everything together) or asks to show the impact of one party's delay, they want a **chain-reaction / critical-path analysis**, NOT more isolated notes. Build a separate `YYYY-MM-DD_<party>-delay-impact-analysis.md` file that:
- **States the numbers up front** — overdue counts per discipline (e.g. "Electrical 49, ICT 39"), % progress for the period (e.g. "1.4% in August"), and the party's rank in the CG overdue list (worst status).
- **Draws the chain reaction** as an ASCII flow: `delay → gate not finalized → downstream stage can't start → EOT/baseline revision blocked → overall project duration impact`. Label each arrow with the concrete target (e.g. "50% DD gate target 10-Sep, was 5-Sep, slipped from 20-Aug"; "IFC within next 6 weeks").
- **Lists the specific blocking items** (the packages holding the gate) in a table with status + who holds it.
- **Refutes the party's stated blockers** if they were already shown to be excuses (e.g. "blocked on power" when power was already submitted).
- **Ends with the required actions** (resource increase, hard date commitment, pressure meeting) as `ADI-N` / `IMP-N` rows, mirrored into `action_items.md` and the INDEX.
This is the deliverable that turns scattered meeting notes into a defensible position the user can present to management or the other party.

## The traceability map (user request: "اربط النقاش بالاميلات بسجل التقديمات" + "اربط بملفات المشروع الرسميه والخطط المعتمده")
When the user asks to connect the meeting to emails, the submittal register, AND the formal/approved documents, add TWO tables at the bottom of the discussion file (after `## Related refs`):

1. **Email & Submittal Cross-Reference** — `| § | Topic | Outlook Email ID | Submittal Ref | Register Status |`. Every meeting topic maps to its Outlook `Record_RecordID` + submittal doc ref + current Code (B/C/D). Follow with a compact `| ID | Date | From | Subject |` table of the key email IDs in the thread.
2. **Formal Documents & Approved Plans** — `| § | Topic | Governing Document | Repo Path |`. Map each topic to its authoritative source: Contract (`00_Contracts/`), ER (`00_Project_Charter/er_document.md`), SOW (`scope_of_work.md`), DMP (`01_DMP/`), BEP (`08_BEP/`), BOQ (`10_Main_Contract_BOQ/`), NRS Methodology (`04_NRS_Methodology/`), Baseline (`02_Schedule/master_programme.md`).

This produces the full chain **meeting topic → email → submittal → governing document**, which is the single most-requested output in design-tracking meetings. It also satisfies AGENTS.md Rule 4 (source traceability) and Rule 12 (cross-link everything).

## Pushing when the remote has moved (rebase conflict)
When `git push origin main` is rejected ("fetch first"), another agent pushed to the repo while you were capturing. Resolve without losing your work:

```bash
git stash push -m "pre-push local changes <date>"   # stash unrelated working-tree edits (webapp, sync_state, etc.)
git pull --rebase origin main                        # replay your commits on top of the remote's
# resolve each conflict: grep -n "<<<<<<<\|=======\|>>>>>>>" <file>
#   - keep the richer/newer side for content conflicts
#   - for NUMBERING collisions (two agents both wrote MOM-19), keep the remote's entry,
#     renumber yours to the next free slot, then fix the back-reference in your discussion file
git add <conflicted files>
GIT_EDITOR=true git rebase --continue               # GIT_EDITOR=true avoids the "Terminal is dumb, EDITOR unset" hang
# repeat until "Successfully rebased and updated refs/heads/main"
git stash pop
git push origin main
```

Key points:
- **`GIT_EDITOR=true` is required** on a dumb terminal (no EDITOR set) — without it `git rebase --continue` fails trying to open an editor for the commit message.
- **MOM numbering collision is the classic conflict** — check `meeting_minutes_register.md` for the next free number BEFORE assigning (another agent may have already taken MOM-19 for a weekly meeting; your design-tracking meeting becomes MOM-20). Grep the register first, then number.
- **Leave unrelated modified files alone** (`.sync_state.json`, webapp HTML, compliance_matrix) — stash them, don't commit them into your meeting-capture push.
- After resolving, `grep -rn "<<<<<<<\|=======\|>>>>>>>"` across the touched dirs to confirm zero markers remain before the final push.

## Pitfalls
- **Don't rewrite the file** — append sections. The user is mid-meeting; a rewrite risks losing a batch.
- **Don't guess names/terms silently** — the transcription is unreliable; confirm the ambiguous ones.
- **Keep the Actions table in sync** between the discussion file and `action_items.md` — they must not diverge.
- **Watch for the sibling-subagent `_warning`** on `action_items.md` (concurrent edits) — re-read before writing.
- **Commit per batch** — if the session dies mid-meeting, the captured notes are already saved.
