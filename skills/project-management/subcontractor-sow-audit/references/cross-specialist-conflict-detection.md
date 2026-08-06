# Cross-Specialist Conflict Detection from Email Batch Scans

Detect scope overlaps, contradictory CG responses, and multiple-supplier conflicts when scanning subcontractor/specialist emails.

## When to Use

- User asks "find any conflicts" after a batch email scan
- User asks to audit all subcontractor CG responses for a period
- Multiple CG responses arrive on the same day for different specialists

## Workflow

### Phase 1 — Email Scan (2-month window)

```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       f.Folder_Name as folder, m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject, m.Message_HasAttachment as att
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_TimeReceived >= strftime('%s', 'now', '-60 days')
  AND (
    -- Specialist/subcontractor keywords
    m.Message_NormalizedSubject LIKE '%PQ-%'
    OR m.Message_NormalizedSubject LIKE '%subcontract%'
    OR m.Message_NormalizedSubject LIKE '%specialist%'
    OR m.Message_NormalizedSubject LIKE '%setwork%'
    OR m.Message_NormalizedSubject LIKE '%BTT%'
    OR m.Message_NormalizedSubject LIKE '%NAFFCO%'
    OR m.Message_NormalizedSubject LIKE '%GUBI%'
    OR m.Message_NormalizedSubject LIKE '%GBH%'
    OR m.Message_NormalizedSubject LIKE '%showcase%'
    OR m.Message_NormalizedSubject LIKE '%lighting%'
    OR m.Message_NormalizedSubject LIKE '%acoustic%'
    OR m.Message_NormalizedSubject LIKE '%landscap%'
    OR m.Message_NormalizedSubject LIKE '%AV%'
    OR m.Message_NormalizedSubject LIKE '%interactive%'
    OR m.Message_NormalizedSubject LIKE '%IT%'
    OR m.Message_NormalizedSubject LIKE '%ICT%'
    OR m.Message_NormalizedSubject LIKE '%security%'
    OR m.Message_NormalizedSubject LIKE '%CCTV%'
    OR m.Message_NormalizedSubject LIKE '%fire alarm%'
    OR m.Message_NormalizedSubject LIKE '%fire suppression%'
    OR m.Message_NormalizedSubject LIKE '%plumbing%'
    OR m.Message_NormalizedSubject LIKE '%MEP%'
    OR m.Message_NormalizedSubject LIKE '%flooring%'
    OR m.Message_NormalizedSubject LIKE '%porcelain%'
    OR m.Message_NormalizedSubject LIKE '%Glasbau%'
    OR m.Message_NormalizedSubject LIKE '%Rawasin%'
    OR m.Message_NormalizedSubject LIKE '%ZNA%'
    OR m.Message_NormalizedSubject LIKE '%NRS%'
    OR m.Message_NormalizedSubject LIKE '%AD Engineering%'
    OR m.Message_NormalizedSubject LIKE '%ACE%'
    OR m.Message_NormalizedSubject LIKE '%Moharram%'
    OR m.Message_NormalizedSubject LIKE '%BMS%'
    OR m.Message_NormalizedSubject LIKE '%JADCO%'
    OR m.Message_NormalizedSubject LIKE '%GITCO%'
    OR m.Message_NormalizedSubject LIKE '%SPS%'
    OR m.Message_NormalizedSubject LIKE '%ELV%'
    OR m.Message_NormalizedSubject LIKE '%furniture%'
    OR m.Message_NormalizedSubject LIKE '%Anaroque%'
    OR m.Message_NormalizedSubject LIKE '%Emaar%'
    OR m.Message_NormalizedSubject LIKE '%Tannah%'
    OR m.Message_NormalizedSubject LIKE '%Hedaia%'
    OR m.Message_NormalizedSubject LIKE '%Hidayath%'
    OR m.Message_NormalizedSubject LIKE '%procurement%'
    OR m.Message_NormalizedSubject LIKE '%tender%'
    OR m.Message_NormalizedSubject LIKE '%supplier%'
    OR m.Message_NormalizedSubject LIKE '%contractor%'
    OR m.Message_NormalizedSubject LIKE '%vendor%'
    OR m.Message_NormalizedSubject LIKE '%subcon%'
    OR m.Message_NormalizedSubject LIKE '%SC-%'
    OR m.Message_NormalizedSubject LIKE '%prequalif%'
    OR m.Message_NormalizedSubject LIKE '%labour%'
    OR m.Message_NormalizedSubject LIKE '%labor%'
    OR m.Message_NormalizedSubject LIKE '%outsource%'
  )
ORDER BY m.Message_TimeReceived DESC
LIMIT 80;
```

### Phase 2 — Extract CG Codes from Preview

```sql
SELECT m.Record_RecordID, m.Message_NormalizedSubject,
  CASE
    WHEN m.Message_Preview LIKE '%A - Approved%' OR m.Message_Preview LIKE '%Approved%' THEN 'A'
    WHEN m.Message_Preview LIKE '%B - Approved%' OR m.Message_Preview LIKE '%Approved with Comment%' THEN 'B'
    WHEN m.Message_Preview LIKE '%C - Revise%' OR m.Message_Preview LIKE '%Revise and Resubmit%' THEN 'C'
    WHEN m.Message_Preview LIKE '%D - Rejected%' OR m.Message_Preview LIKE '%D - Disapproved%' THEN 'D'
    ELSE '?'
  END as cg_code,
  substr(m.Message_Preview, 1, 200) as preview
FROM Mail m
WHERE m.Record_RecordID IN (<ids>);
```

### Phase 3 — Download Attachments

Use the Python AppleScript generator pattern (see `references/python-applescript-generator.md` in outlook-email skill). For emails that fail with `message id N` on Outlook 16.90+, use inline `osascript -e` with `message id N` directly (this works for simple single-attachment extraction even when the `.applescript` file approach fails).

### Phase 4 — Read Documents

Use pdftotext for PDFs, textutil for .docx, openpyxl for .xlsx. Delegate parallel sub-agents (one per specialist group) for large batches.

### Phase 5 — Cross-Reference Against Existing Registers

Read these three registers before concluding:

| Register | Path | What It Tracks |
|----------|------|----------------|
| Specialist Register | `Technical_Office/Specialist_Management/specialist_register.md` | All 27 specialists, stage, status, SOW/plan paths |
| Prequalification Register | `01_Registers/prequalification_register.md` | All PQ refs with CG codes per revision |
| Subcontractor Package Register | `01_Registers/subcontractor_package_register.md` | OneDrive folder map, manager lanes, gaps |

### Phase 6 — Detect Conflicts (5 Types)

| Conflict Type | How to Detect | Example |
|--------------|---------------|---------|
| **Scope overlap** | Two+ specialists claim same scope (BMS, ELV, ICT) | GITCO BMS vs SPS ELV vs Rawasin AV/IT |
| **All suppliers rejected** | Same scope, all CG codes = D | Setwork: BTT (D), Saudi Emaar (D), Tannah (D) — no approved supplier |
| **Contradictory CG comments** | CG approves one specialist but rejects another for same scope | TLC (B) vs PINE (C) vs Evergreen (C) for landscaping |
| **Material non-compliance** | Submitted material fails spec requirements | GUBI porcelain: R9 vs R10, PEI 3 vs PEI 4 |
| **Scope boundary unclear** | No clear RACI between overlapping packages | Showcases (GBH) vs Setwork (Hedaia) — joinery boundary |

### Phase 7 — Report Structure

```
## CG Response Summary (by date)
| Ref | Doc | Supplier/Scope | CG Code | Verdict |

## 🔴 CONFLICTS FOUND
### 1. [Conflict Name] — [Severity]
- Evidence: email IDs, doc refs
- Impact: which packages/schedule affected
- Root cause: why it happened

## 🟡 Key Risks
| Risk | Impact | Urgency |

## ✅ Action Items
1. [Action] — [Owner]
```

## Pitfalls

- **"Final transmittal" ≠ Approved** — Aconex may label a transmittal "Final" even when CG code is C or D. Always read the actual CG code from the email body or attached PDF.
- **Tannah (طنه) may not have a separate PDF** — The Tannah setwork supplier PQ may be in a different batch or under a different doc number. Check Aconex transmittals.
- **Subcontract Management Plan rejection cascades** — ZD-0094 Rev.01 (Subcontract Management Plan) being D means there's no approved governance framework for managing subcontractors. This blocks all subcontractor appointments.
- **AV Design rejection affects Rawasin** — Even though Rawasin is a sister company with an executed contract, their 50% DD design was rejected. The design needs rework, not the contract.
- **BMS scope has 4 claimants** — GITCO (assessment + upgrade plan), SPS (ELV design includes BMS), Rawasin (AV/IT integration), JADCO (kick-off meeting). No single BMS strategy document exists.
- **Register may be stale** — The specialist_register.md may show last_updated weeks ago. New CG responses from today's email scan need to be added.
