# PRR Action-Addition Workflow

## When to Use

- Mid-review the user gives a mitigation directive like "we mitigate by arranging a coordination meeting" or "link X with Y" or "raise RFI to CG"
- The risk already exists in `risks.json` but the existing actions don't cover the new mechanism
- The risk has no `treatment_file` yet but now needs one
- The target close date is stale and needs extending to absorb the new action cycle

If the user just says "update PRR-XX-NN status" with no new mechanism, use the standard review-update path in `risk-review-workflow.md` instead — no new action needed.

## The Invariant Set (every action addition touches all of these)

When you add a new action to an existing risk, these fields MUST stay in sync across three files. Missing any one will surface as inconsistency on the next review.

### File 1 — `02_Registers/risk_register.md`

| Column | Change |
|--------|--------|
| Response Action | Update the mitigation description to mention the new mechanism |
| Target Close | Bump to the new longest action due date |
| Evidence | Append the MoM ID / submittal ref / RFI number that captures the mitigation |

All three changes on one row, one patch call.

### File 2 — `12_WeBsite/Risk/risks.json`

| Field | Change |
|-------|--------|
| `last_reviewed` | Today's date (YYYY-MM-DD) |
| `target_close` | Bumped to absorb the new action cycle |
| `treatment_file` | Set to `04_Plans/08_Risk/treatment/PRR-XX-NN.md` if it was `null` |
| `evidence` array | Append the new MoM / submittal reference |
| `response_action` | Updated text mentioning the new mechanism |
| `actions` array | Append a new action entry: `{id: "A{n}", text, owner, due, status: "In Progress", evidence: ""}` |
| `history` array | Append a `Reviewed` entry with `by: "Hermes"` and a one-line note explaining the change |

Score (`probability`, `severity`, `score`, `rating`) does NOT change just because a new action is added. The new action is part of the existing mitigation strategy. Only re-score if the user's directive is actually a strategy change (e.g. from "Accept" to "Mitigate").

### File 3 — `04_Plans/08_Risk/treatment/PRR-XX-NN.md`

If creating fresh, match the YAML frontmatter of `PRR-DES-01.md` exactly:

```yaml
---
last_updated: YYYY-MM-DD
owner_agent: Hermes
status: active
risk_id: PRR-XX-NN
source: <one-line evidence pointer>
---
```

Body sections in this order:
1. `# Treatment — PRR-XX-NN — <short title>`
2. `## Risk statement` — cause → event → consequence in three short sentences
3. `## Current score` — P × S table
4. `## Response strategy` — Mitigate / Avoid / Transfer / Accept, with rationale
5. `## Actions` — markdown table mirroring `risks.json` `actions` array
6. `## Residual risk (target)` — expected score after mitigation
7. `## Coordination meeting — MoM-NN draft` (only if meeting-driven mitigation) — date, location, chair, attendees, agenda, outputs

If the file already exists, patch it: update `last_updated` frontmatter, add the new action row, append the MoM draft if applicable.

## Worked Example — PRR-DES-04 on 2026-07-25

**User directive:** "for this PRR-DES-04 we mitiegate by arrange Coordination Meeting and LINK NRS with ZNA"

**Inference:** the mitigation is a coordination meeting between NRS (architect/interior) and StudioZNA (lighting) to formalise the verbal design direction (BLACK fixtures in G11/G13) into a documented DI. Target close pushed 2026-07-20 → 2026-07-30 to absorb the meeting cycle.

**Changes applied (in order):**

1. `02_Registers/risk_register.md` row 12:
   - Response Action: `"Issue design instruction; update schedules to MEP/ZNA/Procurement"` → `"Coordination meeting NRS↔ZNA (MoM-15) + DI for G11/G13 + update MEP/ZNA/Procurement schedules"`
   - Target Close: `2026-07-20` → `2026-07-30`
   - Evidence: `"look_ahead item 9"` → `"look_ahead item 9; MoM-15 NRS-ZNA"`

2. `12_WeBsite/Risk/risks.json` entry for `PRR-DES-04`:
   - `last_reviewed`: `"2026-07-14"` → `"2026-07-25"`
   - `target_close`: `"2026-07-20"` → `"2026-07-30"`
   - `treatment_file`: `null` → `"04_Plans/08_Risk/treatment/PRR-DES-04.md"`
   - `evidence`: appended `"MoM-15 NRS-ZNA coordination meeting (planned 2026-07-28)"`
   - `response_action`: extended with `"run NRS-ZNA coordination meeting; link direction into MEP/ZNA/Procurement schedules"`
   - `actions`: appended A3 with `{id: "A3", text: "Arrange NRS-ZNA coordination meeting and capture agreed fixture/finish direction in MoM", owner: "Technical Office", due: "2026-07-28", status: "In Progress", evidence: "MoM-15 draft prepared; invite pending — attendees: NRS (Jim Richards), StudioZNA, Samaya TO, Design Mgr"}`
   - `history`: appended `{"date": "2026-07-25", "action": "Reviewed", "by": "Hermes", "note": "Mitigation strategy updated: add coordination meeting (NRS-ZNA) to formalise verbal direction into documented instruction. Target close extended to 2026-07-30 to absorb meeting cycle + schedule update."}`
   - A1 `evidence` updated from `""` to `"DI draft pending NRS confirmation on fixture finish (BLACK) at coordination meeting A3"` (cross-link to A3)

3. `04_Plans/08_Risk/treatment/PRR-DES-04.md` — created. Frontmatter matches `PRR-DES-01.md`. Action table has 4 rows: A1 (DI), A2 (update schedules), A3 (coordination meeting), A4 (new control: design-direction log in CDE). MoM-15 draft appended as a `## Coordination meeting — MoM-15 draft` section with date, location, chair, attendees, agenda, outputs.

**Items surfaced to the user (not fabricated):**
- StudioZNA contact not in memory → left as `TBC` in the MoM invite
- Meeting slot → proposed 2026-07-28 to keep 30-Jul target close, asked user to confirm

**Verification:** `python3 -c "import json; json.load(open('12_WeBsite/Risk/risks.json'))"` parses cleanly; `risks.json` entry for PRR-DES-04 has 3 actions and 3 history entries; `treatment_file` path set; `risk_register.md` row 12 fields aligned.

## Pitfalls

### 🔴 Forgetting to push `target_close`
If the new action's `due` is later than the existing `target_close`, the risk will appear overdue as soon as the calendar passes. Always bump `target_close` to max(existing target_close, new action due) or later.

### 🔴 Re-scoring the risk when adding an action
Adding a new action is a response-action change, not a probability or severity change. The score stays. Only re-score if the user changes strategy (e.g. drops a mitigation entirely and the risk worsens) or if new evidence materialises.

### 🔴 Editing `index.html` directly
`index.html` is rebuilt by `build_risk.py` from `risks.json` on every deploy. A manual edit gets clobbered. If the live webapp needs to show the change, run `python3 build_risk.py` first, then deploy.

### 🔴 Treating "monitor the meeting" as a separate action
The meeting itself is the action (A3 in the worked example). The follow-ups (issuing the DI, updating schedules) are separate actions that depend on A3. Don't double-count.

### 🔴 Forgetting the cross-link from A1 to A3
When the new action gates an existing action (A1 is blocked until A3 confirms), update A1's `evidence` field to reference the gating action. Otherwise the dependency is invisible and the next reviewer sees two parallel actions that aren't actually parallel.

### 🔴 Score change in `risk_review_workflow.md` flow vs score change here
`risk-review-workflow.md` covers mid-review updates where the user explicitly changes score, status, or owner. This file covers the case where the user gives a NEW mitigation mechanism. The two can chain: user adds the meeting (this file) AND changes the score (the other file) in the same review. Apply both sets of edits, in this order: score/status first, then action addition.

### 🔴 Fabricating contact details
If the user says "link NRS with ZNA" and the ZNA contact isn't in memory, do NOT invent an email or name. Put `TBC` in the MoM invite and surface to the user. The user has corrected fabricated contacts before.
