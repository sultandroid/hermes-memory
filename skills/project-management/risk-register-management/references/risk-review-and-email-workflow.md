# Risk Review & Email Workflow

## One-by-One Risk Review with User

When the user asks to review risks one-by-one:

1. **Present ONE risk at a time** — never dump a list and ask "which one?"
2. **Show full details in a compact table:**
   - ID, Score, Rating, Status, Owner
   - Cause (1-2 lines)
   - Consequence (1-2 lines)
   - Response strategy
   - Action plan table (action, owner, due, status)
   - Overdue flag if any action past due
3. **End with a clear question** — "What action do you want to take?" or "Shall I move to the next?"
4. **When user gives an update** (e.g. "response should be raise RFI"), update BOTH the markdown register AND the JSON source of truth immediately, then confirm the change.

## Drafting Emails to Subcontractors Referencing Risk Register

When the user asks to email a subcontractor about a risk:

1. **Verify the risk details first** — read the full risk object from `risks.json` (not just the markdown summary) to get cause, consequence, response, and action plan.
2. **Check what source data the user is referring to** — if they mention a document (object list, report, etc.), read it or confirm its contents before drafting. Do not assume content exists where it doesn't.
3. **Draft concise email** with:
   - Risk ID and score as context
   - Specific request (what info/action needed)
   - Deadline if applicable
   - CC relevant stakeholders (PM, procurement)
4. **Present as plain text** — user copies and sends manually. No preamble explaining what the email contains.

## Handling Binary Source Documents

When a project document exists as a binary (Excel, PDF) and the user wants it referenced in the repo:

1. **First convert to markdown** — extract data into a `.md` file in the repo under the appropriate register folder. This is the primary reference.
2. **Optionally host the binary** on the project web server (e.g. `samaya-factory.com/aseer/registers/Risk/`) and link from the markdown.
3. **Never commit binaries to the repo** — per repo rules, OneDrive is the source of truth for binaries.
4. **If OneDrive is locked** (Resource deadlock avoided), extract data from an alternative source (e.g. NRS tender package JSON) rather than fighting the lock.

## MoC Object List — Key Facts

- Received 02-Jul-2026 from CG (Mohammad Elbaz) on behalf of MoC
- File: `6930_Aseer_Object Schedule_20260610 (1).xlsx` (188 MB, OneDrive)
- 295 objects total: 53 in showcases, 197 hung/mounted, 32 TBC
- Only 11 AV-relevant objects (5 Welcome Gallery screens + 6 Flowersmen slideshow projections)
- The list contains **physical objects only** — no AV media content (videos, motion graphics, interactives)
- Related risks: PRR-DES-05 (Critical), PRR-AV-01 (Medium), PRR-CNS-03 (Medium)
