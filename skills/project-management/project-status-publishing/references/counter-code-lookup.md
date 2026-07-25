# Counter-Code Lookups (HSE-26, PRR-3, DDR-2, etc.)

## When to use

User asks for the status of a short alphanumeric code: `HSE-26`, `PRR-3`, `DDR-2`, `MA-7`, etc. These are project-specific shorthand, **not** literal document IDs.

## The pattern

Format: `<KEY>-<SEQ>` where:
- `KEY` = a 2-4 letter discipline/artefact prefix
- `SEQ` = a sequence number (usually small, but not a doc number)

The sequence is **relative to a counter** that lives in a specific register, plan tracker, or counter file. It is not the same as the formal doc number (PL-0010, ZD-0043, SC-0035).

## Resolution workflow

1. **Identify the key + sequence.** `HSE-26` → key=HSE, seq=26.
2. **Identify the counter source.** Each key has a canonical home. For the Aseer Museum PM repo:
   | Key | Counter home |
   |-----|--------------|
   | HSE | `08_Document_Index/00_plan_tracker.md` (16 HSE plans) + `10_Manager_Lanes/09_HSE_Manager/dashboard.md` |
   | PRR | `01_Registers/risk_register.md` or `06_Risk_System/risks.json` |
   | DDR | `08_Document_Index/00_plan_tracker.md` (design deliverable reviews) |
   | MA  | `01_Registers/materials_register.md` (Material Approval entries) |
   | SC  | `01_Registers/submittal_register.md` |
   | TQ  | `01_Registers/rfi_tq_register.md` |
   | NCR | `01_Registers/ncr_register.md` |
   | SI  | `01_Registers/site_instruction_register.md` |
3. **Check the counter source for the seq.** The Nth entry in that counter (or the entry whose sequence field matches N) is the target.
4. **If the seq is out of range** (e.g. HSE-26 when only 16 HSE plans exist), the code is either wrong, from a different counter, or refers to a future/inactive entry. Flag the gap and return what does exist.
5. **If multiple keys match** (e.g. "HSE" could be the discipline or a plan family), return the full set and ask the user to disambiguate.

## Example: HSE-26 (Aseer Museum, 2026-07-25)

HSE-26 doesn't match any plan in the tracker (only 16 HSE plans: PL-0010, ZD-0041, PL-0045/46/47/48/49, PL-0043, PL-0054, PL-0036, PL-0037, PL-0040, SC-0035, ZD-0053, ZD-0052). Correct response: report the full HSE snapshot from the plan tracker and note the seq=26 doesn't resolve — ask the user to clarify or check the source counter file.

## Pitfalls

- **Never invent a doc number** to make a counter code "fit" (don't guess `PL-0026` or `ZD-0026`).
- **Counter files can have multiple counters** (e.g. a risk register might have separate counters for project risks vs. HSE-specific risks). Pick the one whose scope matches the key prefix.
- **Some keys are unstable across revisions** — a counter that's been re-baselined may renumber. Always check the current version of the counter file, not a memory of it.
- **The "26" in HSE-26 might be a rev number, not a sequence** — but for HSE, revs are 01/02/03, not bare numbers. If the user says "26" without a Rev prefix, it's almost always a sequence, not a revision.
