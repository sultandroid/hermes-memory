# Risk Register Merge — ID Collision Reference

From the Aseer Museum C08→C09 merge (2026-07-18): merging a PM's consolidated Excel register into the repo's JSON SoT.

## ID Collision Cases Found

When the same PRR-XXX-XX ID means **different risks** in each register, the collision must be resolved before import.

| ID | Repo (Technical Office) | PM Consolidated | Resolution |
|----|------------------------|-----------------|------------|
| PRR-COM-01 | EOT Claim / time-schedule dispute (Critical 12) | Scope changes post-award (High 9) | Kept repo's COM-01 as-is; PM's "scope changes" was a different risk → not imported |
| PRR-COM-02 | Milestone certification lag (High 9) | SAR 0 certified — cash flow (Critical 12) | **SAME risk**; updated repo score to Critical |
| PRR-COM-05 | Insurance adequacy (Low 3) | EOT Claim 01 rejected (Critical 12) | **DIFFERENT risks**. Re-ID repo insurance to PRR-COM-07; created new PRR-COM-05 for EOT rejection |
| PRR-CON-01 | Site mobilisation incomplete (Medium 6) | Blockwork mandate vs drywall (High 8) | **DIFFERENT risks**. Kept repo CON-01; added PM's as PRR-CON-03 |
| PRR-CON-02 | Escalator dismantling clashes (Medium 6) | Heavy art commissions load (Medium 6) | **DIFFERENT risks**. Kept repo CON-02; added PM's as PRR-CON-04 |
| PRR-APP-01 | Stramp/renovation licence (Critical 12) | CG review backlog (High 9) | **DIFFERENT risks**. Kept repo APP-01; added PM's permit block as PRR-APP-04 |
| PRR-MEP-01 | MEP packages lag (High 9) | MEP upgrade exceeds allowance (Critical 12) | **SAME risk**; updated repo to Critical |
| PRR-SIT-01 | As-built conditions differ (High 9) | Undocumented MEP discovered (Medium 6) | **SAME risk**; downgraded repo to Medium per PM assessment |
| PRR-HSE-01 | Summer heat + HSE plan (Medium 4) | HSE fit-out exposure (Medium 6) | **SAME risk**; updated score to 6 |

## Detection Method

Do NOT trust IDs alone. Read the risk event/cause/impact descriptions side by side:

```python
for r_repo in repo_risks:
    for r_pm in pm_risks:
        if r_repo["id"] == r_pm["id"]:
            print(f"COLLISION: {r_repo['id']}")
            print(f"  REPO: {r_repo['title'][:60]}")
            print(f"  PM:   {r_pm['title'][:60]}")
```

## Re-ID Strategy When Collision Found

1. The **repo's existing risk keeps its ID** — it's the established record
2. The **external risk gets a new ID** from the next available serial in its category
3. Document the re-mapping in both the merge script `history` and `merge_note`

## Required JSON Fields

Each risk object must have all fields:

| Field | Type | Example |
|-------|------|---------|
| `id` | str | `PRR-CNS-01` |
| `category` | str | `CNS` |
| `title` | str | Short descriptive one-liner |
| `cause` | str | Root cause / trigger |
| `event` | str | What could happen |
| `consequence` | str | Impact description |
| `probability` | int | 1-4 |
| `severity` | int | 1-4 |
| `score` | int | prob × sev |
| `rating` | str | Critical/High/Medium/Low |
| `status` | str | Open/Watch/Mitigated/Closed |
| `owner` | str | Role from `data["owners"]` |
| `target_close` | str | YYYY-MM-DD or "" |
| `created` | str | YYYY-MM-DD |
| `last_reviewed` | str | YYYY-MM-DD |
| `treatment_file` | str | Path or "" |
| `evidence` | list[str] | Source references |
| `response_action` | str | Mitigation description |
| `actions` | list[dict] | Sub-actions with id/text/owner/due/status/evidence |
| `history` | list[dict] | Change log entries with date/action/by/note |

## add_risk() Parameter Order (the common bug)

The function expects **exactly 5 string params** before the 2 int scores and owner string:

```
add_risk(id, cat, title, event, cause, consequence, response, prob, sev, owner)
         s    s    s      s      s      s            s         i     i    s
```

Missing one shifts all params, causing `TypeError: '>=' not supported between instances of 'str' and 'int'`.
