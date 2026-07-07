# CG Email Triage — Analysis Pattern

A structured approach for reviewing consultant (CG) emails against project governance documents.

## Workflow

1. **Check recipients first** — Query `Message_ToRecipientAddressList` and `Message_CCRecipientAddressList` from SQLite. Verify who is in To vs CC before making any claims about routing.

2. **Read the full email body** — Use AppleScript to get `plain text content` of the message. Preview is truncated.

3. **Cross-reference against approved plans** — For each request in the email:
   - Check the approved **Communication Plan** (PL-0018) — does the routing match the matrix?
   - Check the approved **Design Management Plan** (PL-0029) — does the timeline align with milestones?
   - Check any **Time Baseline / Master Programme** (0PS-SH-006) — what does it say about phase durations?
   - Note: some of these may be in C status (Revise & Resubmit) — note that when referencing.

4. **Identify management inconsistencies** — Common patterns:
   - **Party confusion**: Requesting deliverables from a party that doesn't produce them
   - **Mixed baskets**: Grouping different deliverable types with different workflows into one flat request
   - **Undocumented deadlines**: Claiming "previously agreed" timelines not found in approved documents
   - **Wrong channel**: Emailing the wrong person (based on Communication Plan matrix)
   - **Unrealistic turnaround**: Tight deadline that ignores actual dependencies

5. **Verify before stating** — Always double-check from the DB, not from inference or preview text. Incorrect routing claims (e.g. "PD was in CC not To" when they're actually in To) erode trust immediately.

6. **Propose response channel** — Let the correct party (per the Communication Plan) respond through the proper channel. Example: PD responds stamped with the requested items — this teaches the channel by action, not words.

## Common Pitfalls

- **Assuming the email was sent to the wrong person without checking the actual To/CC lists from SQLite.** Always query `Message_ToRecipientAddressList` and `Message_CCRecipientAddressList` before making routing claims. The preview text does NOT show recipient fields reliably. An incorrect "PD was in CC not To" claim erodes trust immediately.
- **Stating organizational roles without verifying** (e.g., who is the PD — check recent emails or ask). Roles change and you should not assume.
- **Grouping deliverables into a single analysis when they have separate workflows and producers.** Tag each request item with its producer, submitter, and dependency before evaluating.
- **Claiming a deadline is "undocumented" without first checking the Master Programme comments.** CG's timeline claims may be embedded in a C-status document's comments — check before calling it unsupported.
- **Flagging "party confusion" too broadly.** CG oscillates between treating NRS as a separate entity and "under Samaya's umbrella." Check recent pattern before calling it an inconsistency — it may be standard operating procedure from their side.
- **Proposing the user reply with explanations** when CG bypasses the Communication Plan. Don't draft explanatory emails. The correct approach is to let the PD (per the matrix) respond with stamped deliverables — this teaches the channel by action, not words.

## CG Behavioral Patterns (Aseer Museum Context)

CG Project Director Mohammad Elbaz shows a consistent pattern:

1. **Batch-processing** — Silent for days, then dumps 5-10 decisions/reviews in one wave
2. **Aggression-timing** — Sends a tight-deadline demand email ~2 days after Samaya pushes back on something. Treat these as reactive, not routine.
3. **Authority fixation** — Uses "previously agreed-upon timeframe" / "per our agreement" language without document references. Check Master Programme comments for the actual source.
4. **Mixed baskets** — Flat-list requests bundling DD, materials, IFC, and coordination as one item, ignoring different workflows and producers.
5. **Contradicts own plan** — Approved a Communication Plan with routing rules, then emails the wrong party directly.
