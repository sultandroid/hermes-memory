---
name: rfi-register-management
description: Manage Aseer (and similar) RFI/TQ registers. Covers the comprehensive collect-all RFI register (RFI.xlsx → RFI_Aseer_Regional_Museum.md, mirrored to the aseer-museum-pm repo), the prior-reference lookup before declaring an RFI "new", and dedup-within-file checks.
trigger: user asks where to put an RFI, whether an RFI has a prior reference, to update the comprehensive RFI MD register, or to check for duplicate RFI entries.
tags: [rfi, tq, register, aseer, document-control, traceability]
---

# RFI / TQ Register Management (Aseer Museum)

## Trigger
- "where do I put this RFI?"
- "does this RFI have any prior reference?" / "لو له أي إشارة سابقة"
- "update RFI_Aseer_Regional_Museum.md on the repo" / "update as reference"
- "make sure there's no duplication in the file" / "منع التكرار فالملف"
- building or compiling a comprehensive RFI register from an Excel source

## Comprehensive RFI register (collect-all model)

The user maintains ONE comprehensive RFI register that gathers ALL RFIs — including ones already
discussed/documented elsewhere (repo `05_RFIs/`, `05_Comms/drafts/`, TQs). It is a **collect-all**
register, so overlap with repo-registered TQs is expected and allowed. **The rule that matters:
NO duplication WITHIN the register file itself.**

- Source of truth (OneDrive): `.../04_Docs/04_RFIs/RFI.xlsx`
- Compiled MD: `RFI_Aseer_Regional_Museum.md` (same OneDrive folder)
- Repo mirror: `/Users/mohamedessa/aseer-museum-pm/05_RFIs/RFI_Aseer_Regional_Museum.md`
- Pointer + `last_updated`: repo `01_Registers/rfi_register.md` (a `## Comprehensive RFI Register`
  section naming the file, date, item count, and which blocks it covers)

MD structure (two sections):
1. **Summary Table** — one big table: `No. | Subject | Question / Scope | Photo / Reference | CG Response`
2. **Detailed RFI Breakdown** — per-subject `### <Subject>` block, each item `#### Item #N` with
   `- **Question / Requirement:**` + optional `- **Photo / Reference:**` / `- **CG Response / Technical Impact:**`.

Subjects are **blocks with per-block numbering** (A/V Design 1..23, Show cases 1–8, Interior Design
Decision 1–6, Coordination 1–4, ...). Newer "Coordination" blocks (Mounts & Art Handling, Content &
AV Media, Collections & Loans, Replica vs Original) may have blank `No.` — offer to number them for
consistency.

## Mirror MD register to repo (2026-08-22 pattern)

1. `cp <OneDrive MD> /Users/mohamedessa/aseer-museum-pm/05_RFIs/RFI_Aseer_Regional_Museum.md`
2. Add/repoint the `## Comprehensive RFI Register` line in `01_Registers/rfi_register.md`; bump
   `last_updated` to today (YYYY-MM-DD, user requires dates in commit messages and status).
3. `git add` both, commit with date in message.
4. Post-commit hook dirties `06_Risk_System/webapp/src/index.html` — `git checkout -- <that file>`
   before push, then `git push origin main`. Report the commit hash.
5. Note the repo copy is a snapshot: if the user edits the OneDrive MD later, re-copy + commit.

## Prior-reference check (before declaring an RFI "new")

Search in this order — the user explicitly wants a real multi-source check, not a quick "no":

1. **Outlook SQLite** — subject LIKE `%Mount%/%Art Handl%/%Rigging%/%Content%/%Media%/%Codec%` AND
   `Message_Preview` LIKE. JOIN `folders` — Zamzam "projector mounting brackets" hits are unrelated,
   filter to the Aseer folder. Read full body of closest hits via AppleScript `plain text content of m`.
2. **RFI.xlsx** — grep ALL cells for topic keywords; a row may already exist (e.g. the 4 Coordination
   blocks at rows ~566–569).
3. **Repo `05_RFIs/RFI_00NN_*.md`** — individual files (e.g. `RFI_0029_Content.md`,
   `RFI_0030_AV_Content.md`, `RFI_0031_Replica.md`, `RFI_0032_Setworks.md`).
4. **Repo `05_Comms/rfis/*.md`** and **`05_Comms/drafts/*.docx`** — drafted TQs. `TQ-0028`
   (`MOC-MUS-ASE-1E0-TQ-0028_AV_Content_RFI_Rev00.docx`) was the strongest prior ref for the
   Content & AV Media RFI — it asks the same two questions.

**Verdict format** (user likes this): a table of prior refs (ref | doc | what it covers), then a
clear NEW-vs-covered verdict. For a collect-all addition that duplicates a repo TQ, recommend a
`Ref:` line pointing at the prior TQ rather than a standalone entry.

## Dedup-within-file check

Run a near-duplicate scan on question cells (normalize lowercase + collapse whitespace, flag pairs
with SequenceMatcher ratio > 0.85). **Pitfall:** most hits are false positives — the "URGENT Object
List" rows share a template but reference different OB/inventory numbers (different objects =
separate valid rows). Only flag true content duplicates (same subject + same substantive request).

## Drafting an RFI from correspondence (email + drawings)

When the user forwards an email thread + drawing PDFs and says "we wanted to mention this topic" (e.g. the Floor Boxes coordination email from NRS + `SK-MOC-ASE-AR-ARC-{BF/LGF/GF/1F}-DDD-1200/1201/1202/1203` Rev C sketches):

1. **Read the full email thread** via AppleScript `plain text content of m` — the quoted original (e.g. Ali's 92→2 floor-box reduction proposal) is as important as the latest reply (Jim's 3 considerations). Extract the design intent and open questions.
2. **Read the drawing PDFs** with `pdftotext -layout` — pull the drawing number, title, revision, suitability code, and the specific items (e.g. "Floor Box" legend, "Not in Scope"). Note the revision (Rev C = Revised And Resubmit).
3. **Draft the RFI** with:
   - A `Coordination - <Topic>` block title (e.g. "Coordination - Floor Boxes with Electrical Works").
   - A `Ref:` line citing the source email + drawing refs (e.g. "NRS email 17-Aug-2026 + sketches ... (Rev C)").
   - The SOW/ER section reference in the body.
   - The request split into **(a)(b)(c) sub-questions** so the responder can answer each cleanly.
4. **Confirm placement** — offer to add it as a new item in the Coordination block (after the existing 4) in the Excel + MD + repo, and ask the user to confirm the title before writing.

## Report style

Answer the two questions separately and concisely: **"where to put it"** (already present at row N /
block X, or new → which block/number) and **"any prior reference?"** (table + verdict + optional
Ref: offer). Confirm completion explicitly (what changed / copied / committed / pushed + commit hash).

## Related
- `project-register-manager` — general BIM Excel register management, append-not-create, cross-ref to Outlook.
- `outlook-email` — Outlook SQLite search, AppleScript body/attachment extraction, OneDrive EDEADLK recovery.
