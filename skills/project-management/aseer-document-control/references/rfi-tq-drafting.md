## MANDATORY GATE — predecessor check before drafting ANY new RFI

**Never draft a new RFI/TQ until you have searched for predecessors on the same subject and read their status.** Many showcase/object queries were already raised, and several were closed by CG without an answer. Re-asking blind produces a register of duplicates, invites contradicting CG replies, and throws away the strongest part of the argument — the documented "we already asked" chain, which supports EOT and rebuts delay warnings.

### Step 1 — query the submissions DB for same-subject predecessors

```bash
sqlite3 08_Document_Index/submission.db \
  "select s.doc_no, s.revision, s.title, s.submitted_date, s.days_silent, st.code \
   from submission s left join status st on s.status_id=st.id \
   where s.title like '%<keyword>%' or s.doc_no like '%-TQ-%' \
   order by s.submitted_date;"
```

Table is `submission` with `status_id` → `status`; useful columns `doc_no, revision, title, submitted_date, days_silent, is_latest`.

### Step 2 — read the status code, and interpret `CL` correctly

| Code | Meaning | Action |
|------|---------|--------|
| `U` | Open / for review | Chase; do not re-raise the same question |
| `CL` | **Closed — CG closed it WITHOUT answering** | Re-ask is justified; say so factually; never present it as an answer |
| `A` / `B` | Approved | Answered — do not re-raise |
| `C` / `D` | Revise / rejected | Answer the comments, do not re-ask |

### Step 3 — separate ISSUED from INTERNAL queries

A register row with no Aconex record is an **internal placeholder, not an issued document**. Confirm an RFI actually went out before citing it as issued: check the Aconex export (`08_Document_Index/aconex_snapshots/ExportDocs-*.xlsx`, newest file) for the doc number, and the Outlook SQLite for an Aconex workflow transmittal. Rows in `01_Registers/rfi_register.md` alone do not prove submission.

### Step 4 — choose the move, then cite the predecessor in the new text

| Situation | Move |
|-----------|------|
| Predecessor open with the same question | **Chase** — no new RFI |
| Predecessor closed unanswered, new data now exists | **Raise**, cite it, close the old row in the register |
| Several open predecessors on one theme | **Consolidate** into one RFI that lists the open references |

Always put the link in the RFI body: *"this consolidates / supersedes `<ref>` as it relates to `<scope>`"*. Without it the Employer answers the same question twice and the two replies contradict each other.

### Step 5 — what is NOT an RFI

Do not raise an RFI for material a party already offered to provide (precedent photos, drawings, samples). That is a request for information, **not** a contractual query — send it by email. Note that a party who is "by others" / Ministry-appointed (check `01_Registers/interface_register.md`, T1 packages) has no Samaya contract, so the request routes **through the Employer** with the design lead, PMC and CG copied. Keep a direct chase to the party's counterpart in parallel for speed.

## Reference Format

`MOC-MUS-ASE-1A0-TQ-XXXX` (NOT `SIC-1G0` or other discipline codes)

## Contract References for Content/MoC-Provided Items

| Topic | Correct Reference | Wrong Reference |
|-------|-------------------|-----------------|
| Exhibition text, object labels, translations, imagery, copyright | SoW §2.2 (Scope Exclusions) | ER 2.5 (BIM-related) |
| Graphics design & wayfinding | SoW §6.22.1; SoW §8.14 | — |
| Content change cut-off / variations | Contract Art. 14 | — |

## Signatory

- **Project Director (Exhibitions):** Eng. Waris Sultan (since 13-Jun-2026)
- NOT Eng. Adel Darwish (was Interim PD, now superseded)
- Title: `Projects Director` (EN) / `مدير المشروعات` (AR) — NOT `Project Manager` / `مدير المشروع`

## Structure

1. **Header table** (RFI Ref, Date, From/To, Contract Refs, Response By)
2. **Subject line** — bilingual AR/EN
3. **Context paragraph** — why this RFI, what it follows up on
4. **Contract basis** — verbatim SoW clause if relevant
5. **Content table** (if requesting deliverables from MoC):
   - # | Required Content / Format | المحتوى المطلوب / الصيغة | Needed By
6. **Closing** — Yours faithfully + signature

## Key Rules

- Every claim traces to an approved source (SoW, ER, Contract, approved submittal, CG response)
- Bilingual AR/EN throughout
- 14-day contractual review period for CG response
- Reference open queries by number (e.g., "following open query TQ-0026")
- Content-driven scope (graphics, text, imagery) = MoC responsibility per SoW §2.2
