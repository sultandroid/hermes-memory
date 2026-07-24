# Marking Tasks as Done — Do NOT Move Stages

**Rule (updated 2026-07-24, from user correction):** When the user asks to mark tasks as complete on a finished project, set `progress=1.0` only. **Do NOT change `stage_id`.** The task stays in its current stage (DD, Procurement, Mfg, On-site, etc.) — it is simply flagged 100% complete.

Rationale: stage represents the work phase, not completion. A 100% task in DD stage is still a "DD task" for reporting. Moving it to Handover corrupts the stage distribution and breaks Kanban views.

User's exact words: "I told you before: don't move the task between stages; just mark it as done in the same stage. Please update your skills for future use."

```python
# CORRECT — mark complete in place
models.execute_kw(db, uid, pw, 'project.task', 'write', [[task_id], {
    'progress': 1.0
}])

# WRONG — do not change stage
models.execute_kw(db, uid, pw, 'project.task', 'write', [[task_id], {
    'progress': 1.0,
    'stage_id': 479  # NEVER do this just to mark done
}])
```

Exception: only change stage if the user explicitly says "move to Handover" or "move to stage X".

## Bulk Project Closeout — Finished Samaya Projects

When a Samaya project is finished (opening ceremony, final handover signed) and the user asks to register all tasks as complete, run this workflow:

1. Find project by Arabic name: `project.project search_read` with `ilike`
2. List stages: `project.task.type search_read` with `project_ids in [pid]`
3. Count tasks per stage to confirm distribution
4. Identify active-stage tasks only: DD (36), Procurement (39), Manufacturing (659), On-site (40). Leave Handover (479) and Cancelled (480) alone.
5. Batch update `progress=1.0` on all active-stage task IDs. Do NOT touch `stage_id`.
6. Read back to verify.

## Samaya Project ID Map

- 121 = Zamzam VC
- 166 = JabalOmarRetails01
- 176 = JabalOmarRetails02
- 219 = Aseer Museum
- 139 = متحف خير الخلق (Maalim Al-Harameen — finished 2026-07-24)
- 164 = متجر خير الخلق (retail)

## Field Quirks to Remember

- `project.project` has NO `state` field. Use `task_count`.
- `project.task` has NO `kanban_state` field. Use `stage_id`.
- `progress` is float 0.0-1.0.
