---
name: PQ Submission Email — Short Default Template
version: 1.0
created: 2026-07-13
owner_agent: Hermes
status: active
basis: User preference — "we didnt talk to much we just tell its complince with project requirments, and give him the submittle sentance and give him the prequl files link if any"
applies_to: Any compliance update that produces files ready for Aconex upload
---

# PQ Submission Email — SHORT default

> **Use this.** It is the user's preferred default. The longer variant
> (with full compliance checklist, open-items list, deep CG-rule
> explanation) exists in the repo at
> `Technical_Office/Specialist_Management/pq_submission_email_template.md`
> for one-off cases where the full context is genuinely needed — do not
> send the long version by default.

## When to use

A compliance update (PQ, MA, or other) has just been filed in
`OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/02_Submittals/09_Prequalifications/`
(or a sub-contractor's `01_Schedule_and_BOQ/` folder) and is ready for
Aconex upload to CG.

## Shape (always 4 parts, in this order)

1. **One-line compliance state** — name the project rule the
   submission satisfies. One sentence.
2. **Submit sentence + PQ/MA lines** — header "Submitting for Aconex
   upload as follows:" then one line per submission: `<ref> — <full
   doc number> — <vendor> — <scope>`.
3. **PQ files block** — flat list of OneDrive paths, one per line.
   No commentary.
4. **One owner action** — typically: "Hesham — please upload to Aconex
   (separate transmittals) and circulate the CGP-WTRAN numbers."

## Template (copy & fill)

```
Subject: Aseer Museum — PQ Submission for Review and Aconex Upload — <Vendor 1> + <Vendor 2> — <PQ-1> / <PQ-2>

To:      Hesham Abdelhamid <hesham@samayainvest.com>
         Sultan (Eng. Mohamed Sultan) <sultan@samayainvest.com>
CC:      Shihab Mohamed <shihab@samayainvest.com>
         Adel Darwish <adel.darwish@samayainvest.com>
         Eng. Waris Sultan <waris@samayainvest.com>
         <Sub-contractor coordinator email>   # e.g. Rawasin for AV, GFT for joinery, Knauf for ceilings

Team,

The prequalification dossiers for <Vendor 1> and <Vendor 2> are ready. They comply with the project PQ requirements per DMP Rev C04 §5.1.2 and the CG Submission Sequence Rule (27-Apr-26).

Submitting for Aconex upload as follows:

<PQ-1> — MOC-MUS-ASE-1<disc>-PQ-<####> — <Vendor 1> — <scope>
<PQ-2> — MOC-MUS-ASE-1<disc>-PQ-<####> — <Vendor 2> — <scope>

PQ files (filed in OneDrive / BIM unit):
  <OneDrive path to PQ folder>/
    MOC-MUS-ASE-1<disc>-PQ-<####>_<Vendor>_<DocType>_<YearExt>.pdf
    (... one line per file)

<OneDrive path to sub-contractor BOQ folder>/
    <Vendor>_<Scope>_<Date>.xlsx
    <_Vendor>_<Scope>_DepositRecord.md

Hesham — please upload to Aconex (separate transmittals) and circulate the CGP-WTRAN numbers.

Sultan
Eng. Mohamed Sultan
Tech Office Manager — Aseer Regional Museum
Samaya Investment
```

## Anti-patterns (do not do)

- ❌ Don't include the 11-item compliance checklist. The matrix and
  gap register already have it. Repeating it in the email adds no
  decision value for the team.
- ❌ Don't list open items / known gaps in the email body. They live
  in `compliance_gaps.md` Notes and the gap register row. Mention
  them in the email only if they block Aconex upload (rare).
- ❌ Don't repeat the CG Submission Sequence Rule. One citation is
  enough; the auditor will read the register.
- ❌ Don't add a pre-amble or post-script explaining the email.
  Trust the team to read it.
- ❌ Don't pad the subject line. The pattern is fixed.

## After sending

1. Append the email filename to `00_Status/action_items.md` as the
   source of the actions it triggers.
2. Add a DRAFT row to `Technical_Office/Specialist_Management/prequalification_log.md`
   for any new PQ referenced in the email (so the markdown-register
   row count stays ahead of the actual Aconex submissions).
3. Update `last_updated` frontmatter on both files.
