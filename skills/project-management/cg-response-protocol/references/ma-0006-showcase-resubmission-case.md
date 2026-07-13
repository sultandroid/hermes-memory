# MA-0006 Showcase Resubmission — Worked Example

> Aseer Regional Museum · Glasbau Hahn · Showcases Materials
> CG Rejection Code C (15-Apr-2026) → Resubmission Prep (13-Jul-2026)

## The Problem

CG rejected MA-0006 Rev.00 (Showcases Materials by Glasbau Hahn) with Code C. Key complaints:
1. Materials don't comply with specs
2. Anti-reflective glass non-compliant
3. Must follow SI-007 (3D render → material board → IFC)
4. Brass must be patinated
5. **Provide 3 alternative suppliers**

## The Discovery

The Glasbau Hahn reply was **not in the project submittal folder** — it was sitting in Outlook since April 2026.

### Finding supplier replies in Outlook

```sql
-- Search by submittal ref
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
       m.Message_SenderList, m.Message_NormalizedSubject, m.Message_HasAttachment
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%MA-0006%'
ORDER BY m.Message_TimeReceived;
```

Three emails found:
- 21-Apr: Ahmed Salah → Glasbau Hahn (forwarded CG rejection)
- 22-Apr: Ahmed Metwally (Glasbau Hahn) → Ahmed Salah (Guardian Clarity datasheet)
- 29-Apr: Ahmed Metwally → All (formal comments reply sheet)

### Extracting attachments

```bash
osascript -e "
tell application \"Microsoft Outlook\"
    set theMsg to message id <ID>
    set atts to (every attachment of theMsg)
    repeat with att in atts
        set savePath to \"/tmp/\" & (name of att)
        do shell script \"touch \" & quoted form of savePath
        save att in (POSIX file savePath as alias)
    end repeat
end tell
"
```

## The Argument

Glasbau Hahn's 29-Apr-2026 reply sheet + Guardian Clarity datasheet proved:
- Guardian Clarity Neutral: Tvis > 97%, Rvis < 1% — museum grade
- All materials match finishes schedule Material IDs
- Patinated brass samples submitted per FI_ME_01
- Alternative powder-coated metal per NRS recommendation

**CG's "3 alternative suppliers" demand was based on the initial non-compliant submission.** Since technical compliance is now proven, request CG to accept single supplier with technical justification.

## Support Folder Structure

```
09_Submittals/MA-NNNN_Rev01_Support/
├── 01_CG_Rejection_Code_C/           CG rejection letter
├── 02_Supplier_Technical_Reply/      Supplier's comments reply sheet
├── 03_Manufacturer_Datasheet/         Manufacturer's technical datasheet
├── 04_Supporting_Data_Sheets/        All material data sheets (flat, no subdirs)
├── 05_PQ_Approval/                   Original prequalification approval
├── 06_Sample_Board/                  Sample board photo
├── 07_Related_Submittal_Support/     Cross-referenced material support
├── 08_Email_Thread/                  Full email chain (outside support folder for CG)
└── 09_Resubmission_Checklist/        CR Sheet + checklist (outside support folder for CG)
```

## CR Sheet Structure

| # | CG Comment | Reference | Response | Supporting Doc | Status | Remarks |
|---|-----------|-----------|----------|---------------|--------|---------|
| 1 | Materials don't comply | Rejection letter | Supplier reply + 14 data sheets | 02_Supplier_Reply/ + 04_Data_Sheets/ | CLOSED | All materials match finishes schedule |
| 2 | AR glass non-compliant | Rejection letter | Guardian Clarity meets FI_GL_04 spec | 03_Guardian_Datasheet/ | CLOSED | Tvis > 97%, Rvis < 1% |
| 3 | Comply with SI-007 | Rejection letter | NRS approved drawings 19-Jun | 08_Email_Thread/ | CLOSED | SI closed 27-Apr |
| 4 | Brass patinated | Rejection letter | Separate submittal MA-0007 | 07_MA_0007_Support/ | PARTIAL | Look & feel request sent to CG |
| 5 | 3 alternative suppliers | Rejection action | Request single-source acceptance | 02_Supplier_Reply/ + 05_PQ_Approval/ | OPEN | Awaiting CG decision |

## Look & Feel Approval Strategy

When supplier test reports/certifications take time (supplier lead time), but the visual sample is ready:

1. **Request CG to approve LOOK AND FEEL now** — visual appearance, colour, texture
2. Test reports & certifications to follow once received from supplier
3. Alternative samples from local suppliers in parallel
4. Submit outstanding docs as Rev.01 addendum within 30 days

## Separate Submittal Principle

**Do not block one submittal because a related submittal is pending.** Example:
- MA-0006 (showcase materials: glass, silicone, fabric, Corian, lighting, powder coating) — independent of brass
- MA-0007 (patinated brass) — separate submittal, separate rejection
- MA-0006 Rev.01 can proceed without MA-0007 approval

## Key Lessons

1. **Check Outlook first** — supplier replies often sit in email, not the project folder
2. **Extract attachments** — the supplier's reply sheet + manufacturer datasheet are the two key documents
3. **Build the argument** — "3 suppliers" was based on initial non-compliance; technical proof changes the negotiation
4. **Separate submittals** — don't let one Code C block another
5. **Look & feel first** — visual approval can proceed while technical docs catch up
6. **CR Sheet goes to CG** — email thread + checklist stay outside the support folder for direct sending
