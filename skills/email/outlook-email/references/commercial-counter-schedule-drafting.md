# Drafting Commercial Reply / Counter-Schedule Emails

Applies when the user asks to draft a reply to a vendor/specialist commercial email (payment schedule, fee proposal, contract terms, resolution request). The `outlook-email` skill's "Creating Draft Emails" section covers format; this covers the *content discipline* that prevents the two most common failures.

## Rule 1 — Check the repo for the ALREADY-AGREED position BEFORE drafting

The user frequently works out the commercial position in advance and records it in the repo. Drafting from scratch (or from the incoming email alone) re-invents or contradicts the agreed position and wastes a round-trip.

Before writing a single line, search:
- **GitHub issues** on the project repo (`gh issue view <n> --repo sultandroid/<repo> --json comments`) — the user opens issues like `[Commercial] Revised BIM payment schedule - <vendor>` and the agreed counter-schedule is often already posted as a comment.
- **Formal letter files** in the repo (e.g. `03_Plans/05_Cost/REVISED_*_<VENDOR>_<date>.md`) — a ready-to-send letter may already exist.
- **Correspondence register** (`05_Comms/correspondence_register.md`) — confirms contract refs, amounts, dates.

If a prior agreed position exists, the draft must MATCH it (amounts, instalment triggers, retention, re-timing). Do not silently produce a different schedule.

## Rule 2 — Verify the arithmetic: the schedule MUST sum to the outstanding balance

A counter-schedule that changes instalment amounts (e.g. raising final retention) must be rebalanced so the total equals the outstanding contract balance. Failure mode seen: changing final payment from USD 1,500 → USD 4,000 without lowering another line produced a schedule summing to USD 14,000 against a USD 13,500 outstanding — a 500 error the user caught.

Checklist before presenting:
- Total contract value (from PO / proposal / correspondence register)
- Paid to date (advance/mobilization + completed phases)
- Outstanding = total − paid
- Sum of all proposed instalments == outstanding
- If you change one line, adjust another to keep the total

## Rule 3 — Verify vendor "stalled / no input" claims against the submittal register

A vendor may claim the project stalled on the client's side ("no approvals, no go-ahead") to justify a reserved-period compensation claim. Before conceding, check the submittal register (`01_Registers/submittal_register.md`) for the relevant discipline's approvals. If the design input the vendor needed was already approved (e.g. mechanical submittals Code B / deemed approved), the claim is weakened — cite the specific doc refs + codes + dates in the reply.

## Rule 4 — Scope changes the user requests mid-draft must propagate everywhere

If the user says "postpone X for now" (e.g. defer 5D BIM), update:
- The introduction (state the deferral + rationale, e.g. reduce resource load, possible later call-off)
- The instalment table (remove/re-label the affected line)
- The "key changes" list
- The total (if the deferred scope carried a payment, rebalance)

## Rule 5 — The repo formal-letter file can be a STALE DRAFT; the email thread is the authoritative final position

The repo's `REVISED_*_<VENDOR>_<date>.md` file is often a **draft that was superseded** once the vendor replied and the two sides actually agreed. Do NOT treat the repo file as the final position — it may propose a schedule that was never accepted (e.g. a USD 20,000 counter-schedule when the real outstanding was USD 13,500 and the vendor accepted a different split).

When closing a commercial GitHub issue or reporting the agreed position, **reconstruct the actual agreement from the email thread**:
- **Sent Items** — the user's own confirmation letter (the agreed schedule, terms, scope adjustments).
- **Inbox replies** — the vendor's acceptance (often explicitly "I confirm my acceptance ... at the unchanged total of USD X").
- **Later vendor emails** — receipt acknowledgments / payment reminders that confirm amounts received to date and the next due instalment.

Then **reconcile the repo file to the email-agreed position** (update amounts, triggers, total, terms) and note it supersedes the earlier draft. The emails are the source of truth for what was actually agreed; the repo file is only a snapshot that may be stale. Verified 2026-08-28: Radiance BIM payment issue #268 — repo draft said USD 20,000, but the email thread (Outlook 51606/51586/51928) showed the agreed USD 13,500 schedule; the repo file had to be rewritten to match.

## Rule 6 — OneDrive contract stubs block verification

Contract PDFs/DOCX in OneDrive are often cloud stubs that fail to hydrate (`pdftotext` → "Couldn't find trailer dictionary", `textutil` → "couldn't be opened", `brctl download` → "Path is outside of any CloudDocs app library"). When you cannot read the original payment schedule, say so explicitly and ask the user to confirm the original advance/mobilization figure (or open the file in Finder to force hydration) rather than guessing. Never fabricate the original schedule.

## Rule 7 — A revised payment schedule is NOT a contract amendment (terminology precision)

When the user agrees to a vendor's revised payment schedule, the deliverable is a **payment rescheduling** — it re-times/re-splits the outstanding balance against deliverables. It does **not** amend the contract's scope, terms, or total value. Do NOT write "issue the contract amendment" or "contract amendment" anywhere in the repo file, the GitHub issue close comment, or the email draft unless the parties actually amended the contract.

Failure mode (2026-08-28): the repo file `REVISED_BIM_PAYMENT_RADIANCE_2026-08-20.md` and the issue close comment both said "issue the contract amendment" as a remaining action. The user corrected: "مش تعديل للعقد مجرد جدوله للدفعات" (it's not a contract amendment, just a rescheduling of payments). The Mobilization trigger is "acceptance of the revised payment schedule", not "issue of a contract amendment".

Checklist:
- Trigger wording: "acceptance of the revised payment schedule" (not "issue of contract amendment").
- Remaining-action wording: "release Mobilization payment USD X by <date>" (drop any "issue the contract amendment" line).
- Total value stays unchanged (rescheduling preserves the outstanding balance).
- Only use "amendment" if the parties explicitly amended scope/terms/value.
