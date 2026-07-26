# PQ (Prequalification) Email Processing — Aseer Museum

## PQ Subject Line Patterns

PQ emails follow predictable subject formats:

| Pattern | Example | Meaning |
|---------|---------|---------|
| `{Ref} / {Scope} - {Vendor}` | `MOC-MUS-ASE-1A0-PQ-0125 / Acoustic Specialist - JOCAVI` | Formal PQ submittal via Aconex |
| `Prequalification Documents {Vendor}` | `Prequalification Documents Molitor` | Internal review (Shihab → Ali), no PQ ref yet |
| `Approval of Laboratory Prequalification and Request for Quotation` | Lab prequal approved, RFQ follows | Usually Code B from Waris or direct from lab |
| `{Vendor} Prequalification` or `vendor Prequalification Documents` | Shihab submitting docs for internal review | Pre-Aconex draft stage |

## Sender → Role Mapping

| Sender | Role | What they send |
|--------|------|----------------|
| Hossam Mabrouk (hmabrouk@cg.com.sa) | CG reviewer | CG response with code A/B/C/D — the authoritative source |
| Hesham Abdelhameed | Doc Controller | Forwards CG responses to team, files in Asher Regional Museum folder |
| Shihab Al-Harbie | Technical Immersive Engineer (Rawasin/AV) | Vendor PQ docs for internal review, sent to Ali for approval before Aconex |
| Mohamed Samir | Procurement (acting QA/QC) | Forwards vendor PQ docs, coordinates submissions |
| Hani Alghamdi | Procurement | Submits vendor PQ docs to Hesham for CG submission |
| Soliman Obiya | Coordinator | Coordinates acoustic specialist PQs (AME, Acoustieg, TransOrient) |
| Amro Mohammed | MEP engineer | Material/equipment PQs (HVAC, plumbing, pipes) |
| Muhammad Waris Sultan Khan | Project Director | Lab prequal approvals, RFQ distribution |
| Adel Darwish | Interim PD (previous) | Filed PQ folders with Approval subfolders |

## Two-Phase Processing

### Phase A: Internal Draft PQs (from Shihab, Soliman, Hani — no PQ ref yet)

These are pre-submission docs sent for internal review. They don't have Aconex transmittal numbers or CG codes yet.

**SQLite query pattern:**
```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
       m.Message_SenderList, m.Message_NormalizedSubject, m.Message_HasAttachment
FROM Mail m
WHERE m.Message_SenderList LIKE '%Shihab%'
   OR m.Message_SenderList LIKE '%Soliman%'
   OR m.Message_SenderList LIKE '%Amro%'
ORDER BY m.Message_TimeReceived DESC LIMIT 20;
```

**Register treatment:** Add to prequalification_register.md with status `—` (no code yet). Note "Awaiting PQ ref" in Notes. Do NOT add to prequalification_log.md until a formal PQ ref is assigned.

### Phase B: Formal CG Responses (from Hossam Mabrouk / Hesham — with PQ ref and code)

These arrive via Aconex workflow transmittal emails. The CG code can be read from Message_Preview without extracting attachments.

**Read CG code from preview:**
```sql
SELECT m.Record_RecordID, m.Message_NormalizedSubject,
  CASE
    WHEN m.Message_Preview LIKE '%A - Approved%' THEN 'A'
    WHEN m.Message_Preview LIKE '%B - Approved%' THEN 'B'
    WHEN m.Message_Preview LIKE '%C - Revise%' THEN 'C'
    WHEN m.Message_Preview LIKE '%D - Disapproved%' THEN 'D'
    ELSE 'UNKNOWN'
  END as cg_code
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%PQ-%'
  AND m.Message_TimeReceived >= strftime('%s', 'now', '-14 days')
ORDER BY m.Message_TimeReceived DESC;
```

**Cascade updates for PQ responses (apply in this order to prevent stale references):**

1. `01_Registers/prequalification_register.md` — update CG code, date, and summary of CG comments in the Notes column. This is the source-of-truth PQ list.
2. `Technical_Office/Specialist_Management/prequalification_log.md` — update state from SUBMITTED → CG-CODE, fill CG Resp. date and Code column, update roll-up counts. Tracks the appointment lifecycle.
3. `Technical_Office/Specialist_Management/specialist_register.md` — update specialist name, PQ ref, stage, status (especially for acoustic, landscaping, lab, setwork specialists where new candidates appear or CG codes arrive).
4. `01_Registers/subcontractor_package_register.md` — update the relevant package row with new specialist names and CG codes.
5. If Code B (Approved): flag for MoC approval step
6. If Code C: check if a revised submission is being prepared (look for follow-up emails)

The register is the source of truth; the log derives from it; the specialist register references the log; the package register references the specialist register. Updating in this order prevents downstream stale references.

## Pitfalls

- **"Final transmittal" ≠ Approved.** Aconex sometimes labels CG responses as "Final transmittal" even for Code C. Always read the code from the email body or attached PDF, not the transmittal classification. Real example: PQ-0126 PINE was labelled "Final transmittal" in Aconex but the CG response was Code C.
- **CG responses may contradict the register.** If the email says Code C but the register says "Final" or "Approved", the email is the authoritative source — correct the register. The preview text contains the CG code in the format `X - Approved/Comment/Revise` — use this to verify before trusting the register.
- **Duplicates are common.** Multiple people (Samir, Hani, Soliman) often forward the same vendor PQ dossier. Dedup by filename and file size before filing.
- **Shihab's emails are internal, not submittals.** They're sent to Ali Abdelrahman for review. They don't go to CG until Ali approves and Hesham uploads them to Aconex. Don't add them to the CG-tracked register until that happens.
- **"prequ ana materials submittles" query pattern.** The user may use shorthand like "prequ ana materials submittles" (prequalification analysis materials submittals). This refers to prequalification documents with attachment analysis. Expand the search to cover both `prequalification` and `material submittal` patterns across multiple variants (prequ, PQ-, submitt, material sample).
- **Hossam Mabrouk CG emails carry the code in the first 500 chars of preview.** The classification line `Classification-ASE-External-...` is followed within ~3 lines by the code line `X - Approved/Revise/Disapproved`. A single SQL preview scan can read codes for 10+ PQs without extracting attachments.

## Knowledge Document Generation

After the register cascade is complete, generate specialist knowledge MDs from the extracted document content.

### Workflow

1. **Extract text:** Walk the filed document folders and run `pdftotext -layout <pdf> <txt>` for PDFs, `openpyxl` for XLSX, `zipfile -l` for ZIPs. Save all to a `_Text_Extracts/` directory.
2. **Analyze in parallel:** Delegate 3 sub-agents via delegate_task — acoustic, landscaping+labs, AV vendors+materials.
3. **Save format:** Per Phase 9 format in SKILL.md, saved to `Technical_Office/Specialist_Management/pq_knowledge/<group>.md`.
4. **Cross-check CG codes:** The PQ review sheet form may have blank code boxes. Always cross-check against the CG email preview text (Hossam Mabrouk). Annotate: `— per CG email from Hossam Mabrouk (<date>)`.
5. **Commit to repo** alongside register files.

### Known Image-Based PDFs (no extractable text)

Scanned documents pdftotext cannot read: CE DoCs, authorization letters, VAT certificates, trade licenses.

### Knowledge File Index (created 2026-07-26)

| File | Contents |
|---|---|
| `pq_knowledge/acoustic_specialists.md` | ACOUSTIEG (PQ-0123 C), AME (PQ-0124 C), JOCAVI (PQ-0125 C), TransOrient (PQ-0128 U) |
| `pq_knowledge/landscaping_labs.md` | Evergreen (PQ-0122 C), PINE (PQ-0126 C), TLC (PQ-0127 B), RAN Lab (PQ-0120 B), Saham (PQ-0121 U) |
| `pq_knowledge/av_vendors_materials.md` | NETGEAR, Molitor, Yamaha (PQ-0060), Q-Sys (PQ-0058), Iiyama (PQ-0034), Audinate, APLACO |
