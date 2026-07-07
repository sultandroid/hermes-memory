# Contract Readiness Assessment — Worked Example

**Pattern:** Full subcontractor quotation review pipeline — email discovery → extraction → gap analysis → CG comment cross-reference → scope split confirmation → contract readiness verdict.

## Pipeline Overview

```
1. Email Discovery ──→ 2. Extract Attachments ──→ 3. Read Quotation
       │                        │                        │
       ▼                        ▼                        ▼
4. Read Project Baseline (ER/SOW/DMP extracts, Samaya Rev-01 SOW)
       │
       ▼
5. Build Gap Matrix ──→ 6. Check CG Review Status ──→ 7. Confirm Scope Split
                                                    │
                                                    ▼
                                    8. Synthesise Contract Readiness
                                                    │
                                                    ▼
                                    9. Go/No-Go Verdict + Next Steps
```

## Phase Detail

### 1. Full Email Thread Discovery

Do NOT query only recent emails. Find ALL emails in the thread:

```sql
SELECT id, received, folder, sender, subject, att
FROM Mail JOIN folders ON Record_FolderID = Record_RecordID
WHERE Message_NormalizedSubject LIKE '%<keyword>%'
  AND (Message_NormalizedSubject LIKE '%<vendor>%' OR Message_SenderList LIKE '%<vendor>%')
ORDER BY received ASC;
```

Key: read the thread FROM THE BEGINNING. The earliest email often has the original proposal.

### 2. Extract All Attachments

AppleScript `touch`-before-`save` pattern. Extract PDFs, DOCX, XLSX. Then `pdftotext`.

### 3. Read Quotation Against Our SOW

Compare item-by-item against ER, SOW, DMP extracts.

**Chronology trap:** If Samaya issued a Rev-01 SOW AFTER the vendor's quotation date, the vendor hasn't priced the added deliverables.

### 4. CG Review Status

Check if the SOW doc was submitted to CG. Doc code pattern: `MOC-MUS-ASE-1XX-ZD-NNNN`.
Codes: A=Approved, B=Approved+Comments, C=Resubmit, D=Rejected.

### 5. Scope Split Confirmation

User may clarify who-does-what mid-review. Document these changes — they change what counts as a "gap."

### 6. Fee Re-Baseline (when scope changes)

| Item | Original | Change | Revised |
|---|---|---|---|
| Stage X | fee | +/- deliv. | estimate |
| **Total** | | | **revised** |

### 7. Contract Readiness Matrix

| Dimension | Status | Notes |
|---|---|---|
| Scope coverage | ✅/⚠️/❌ | vs ER/SOW/DMP |
| CG comment alignment | ✅/⚠️/❌ | Map CG to vendor scope |
| Scope split correct | ✅/⚠️/❌ | Right role? |
| Fee reasonable | ✅/⚠️/❌ | Market-appropriate |
| Terms acceptable | ✅/⚠️/❌ | LD, insurance, payment |
| **Verdict** | **GO/CONDITIONAL/NO-GO** | |

---

## Worked Example: ZNA Lighting Designer (Aseer Museum, June 2026)

**Thread:** "Request for Proposal - Lighting Design Services for Project Rev. 3297"

**Timeline:**
- 31-May: Hakami raised BIM cost → move to MEP Designer
- 02-Jun: Hakami sent ZNA proposal for team review
- 05-Jun: Sultan cross-reference complete — "substantially compliant"
- 07-Jun: SOW submitted to CG as ZD-0056
- 11-Jun: CG Code B (9 comments)
- 13-Jun: Samir → prepare CRS
- 14-Jun: ZNA quotation + payment schedule forwarded

**Key findings:**
1. ZNA quoted on old scope (01-Jun). Samaya Rev 01 (05-Jun) added 8+ deliverables
2. Stage 5 OPTIONAL — SOW §8.8 mandates it firm with site focusing
3. Stage 6 absent (as-built, commissioning, aftercare)
4. BIM removed → Radiance Group (Dr. Waleed Salah)
5. Shop/workshop dwgs → MEP contractor
6. CG comments mostly covered — #3 (action plan) + #8 (meetings) need confirmation

**Fee re-baseline:**
| Item | Original | Adjustment | Revised |
|---|---|---|---|
| Stage 4 | £21,227 | +conservation, UV/IR, daylight, O&M, data-set | ~£24-26k |
| Stage 5 | £10,875 | −shop-dwg review +site focusing | ~£6-8k |
| Stage 6 | — | +as-built, witness, aftercare | ~£5-7k |
| **Total** | **£32,102** | | **~£35-41k** |

**Verdict:** CONDITIONAL — proceed once ZNA revises fee covering full scope, confirms site focusing, adds Stage 6.
