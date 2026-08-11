# Refreshing Action Plans for Past-Due Open Risks

When a risk's `target_close` has passed but status is still `Open`, refresh its
action plan rather than leaving stale "Not Started" rows with past due dates.

## Workflow

1. **Check the treatment file FIRST** — `03_Plans/08_Risk/treatment/{ID}.md` is
   the authoritative action source. If it exists, sync its `## Actions` table
   into the JSON `actions` array (statuses, owners, due dates, evidence).
   In practice only ~2 of 10 past-due risks had treatment files; the rest need
   evidence-based refresh.

2. **Gather real evidence** from `01_Registers/submittal_register.md`
   (submission/approval dates, CG codes) and the WhatsApp archive before marking
   any action Done/In Progress. Examples from 2026-08-11:
   - Flooring samples submitted 11-Aug (USG, Marj Tiles, Mada Gypsum, Jazeera,
     EXA, Alwatania) → PRR-CON-05 A3 "Expedite MA-0001 resubmission" = In Progress
   - SMP Rev.01 submitted 23-Jul awaiting CG → PRR-COM-08 A1 = Done

3. **Extend `target_close`** to a realistic future date for risks still genuinely
   open; keep the old date in the history note.

4. **Mark merged risks Mitigated** — a risk whose treatment file has
   `merged_into: <other>` frontmatter may still show `Open` in JSON. Set status
   `Mitigated` and collapse its actions to a single "Merged into X" Done row.
   Example: PRR-SIT-02 merged into PRR-DES-07 (2026-07-20), structural DD Rev.02
   Code B 30-Jul → marked Mitigated.

5. **Handle missing `history` key** — some risks (e.g. PRR-COM-09) lack a
   `history` array. Use `r.setdefault('history', []).append(...)` instead of
   `r['history'].append(...)` (raises KeyError).

6. Rebuild webapp + markdown register + snapshot, redeploy, commit, push
   (see the Rebuild → commit → push workflow in the main SKILL.md).

## JSON action object schema

```python
{'id': 'A1', 'text': '...', 'due': 'YYYY-MM-DD', 'owner': 'Role',
 'status': 'Pending|In Progress|Done|Overdue|Open', 'evidence': '...'}
```

## Pitfall

The `actions` array in `risks.json` is frequently stale (all "Not Started" with
past due dates) even when the treatment file shows real progress. Always prefer
the treatment file + submittal register as evidence over trusting the JSON
action statuses.

## Lesson-linked risks need action-plan sync too

When new Lessons Learned are captured (LL-019 showcase redesign, LL-020 rigging
PQ-0130 Code D, LL-021 EOT LT-0007, LL-016 AD Engineering SOW dispute), the
linked PRR risks (PRR-SHC-02, PRR-PRC-04, PRR-COM-01, PRR-MEP-01) often have
stale action plans that don't reflect the triggering event. Update them in the
same pass — e.g. PRR-COM-01 gained an "EOT LT-0007 submitted 11-Aug = Done" row,
PRR-PRC-04 gained a "resubmit rigging PQ-0130" row, PRR-MEP-01 gained an
"AD SOW dispute resolution" row.

## Rating vs P×S mismatch

A risk can be rated `High` while P×S = 12 (Critical band). Recompute
`score = probability × severity` and fix `rating` per RMP bands (≥12 Critical,
8–11 High, 4–7 Medium, ≤3 Low). Example: PRR-SCH-05 was `High` with P4×S3=12 →
corrected to `Critical`. Also populate blank `cause`/`event`/`consequence`
fields (e.g. PRR-SI-001) that render as empty cells in the register.
