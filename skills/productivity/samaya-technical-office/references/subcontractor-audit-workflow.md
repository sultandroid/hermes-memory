# Subcontractor Audit Workflow

## When to use

You need to verify that all existing subcontractor folders under `Subcontractors/` have:
- Standard 9-directory structure
- SCOPE_REQUEST.md (SOW)
- Files in the correct subdirectories
- No duplicate numbering conflicts
- Source traceability for approval documents

## Audit script (Python)

Run this from the project root:

```python
import os

BASE = "Subcontractors"
STANDARD = [
    "01_Schedule_and_BOQ", "02_Reference_Drawings", "03_Specifications_and_Standards",
    "04_Reference_Imagery", "05_Returned_Submittals", "06_RFIs", "07_Approvals",
    "Email_Data_Extraction", "_MANAGER_DASHBOARD",
]

subs = sorted([d for d in os.listdir(BASE) 
               if os.path.isdir(os.path.join(BASE, d)) and not d.startswith("_")])

for sub in subs:
    path = os.path.join(BASE, sub)
    existing = set(d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)))
    has_sow = os.path.exists(os.path.join(path, "SCOPE_REQUEST.md"))
    has_sr = os.path.exists(os.path.join(path, "_MANAGER_DASHBOARD", "SITUATION_REPORT.md"))
    missing = [s for s in STANDARD if s not in existing]
    fc = sum(len(files) for _, _, files in os.walk(path))
    
    status = "✅" if (has_sow and not missing) else "❌" if (not has_sow) else "⚠️"
    print(f"{status} {sub} | SOW={'Y' if has_sow else 'N'} | files={fc} | missing={missing if missing else '-'}")
```

## What to check per subcontractor

| Check | Criteria | Fix |
|-------|----------|-----|
| **SOW exists** | `SCOPE_REQUEST.md` present | Create using Samaya 10-section template (ref:subcontractor-creation-workflow.md) |
| **Standard dirs** | All 9 directories present | Create missing dirs with `mkdir -p` |
| **SitRep** | `_MANAGER_DASHBOARD/SITUATION_REPORT.md` exists | Create with status, dates, actions |
| **SOW .docx** | `SCOPE_REQUEST.docx` should mirror .md | Generate using `samaya_doc_template.py` (ref:samaya-docx-generation.md) |
| **Duplicate files** | Same file appearing under different names | Check MD5 hashes, remove original-named copies, keep project-registered versions |
| **Source traceability** | Files in `07_Approvals/` should have known origin | Check `Email_Data_Extraction/` for email database; trace supplier → sender → date |
| **Empty dirs** | 02_Reference_Drawings, 04_Reference_Imagery may be empty | Note as N/A in SitRep, don't delete (they're standard) |
| **Numbering conflicts** | Two subs sharing same `NN_` prefix | Use suffix: `a` = trade, `b` = purchasing/vendor/material. Keep original at `NN_`, new at `NNa_` or `NNb_` |

## Source tracing for approval documents

When files in `07_Approvals/` lack obvious provenance:

1. Check `Email_Data_Extraction/` for email database files (e.g., `*_EMAIL_DATABASE.md`)
2. Search the email database for the file name, supplier name, or subject keywords
3. Extract: sender company → intermediary (if any) → Samaya recipient → date received
4. Note whether the document is:
   - **Independent test report** (reliable for compliance decisions)
   - **Supplier-provided compliance cert** (supporting evidence only — may still require independent verification)
   - **Project-registered submission** (has MOC-ASEER-XX-XXX document number)
5. Flag in SitRep if supplier-provided evidence is being used as substitute for independent testing

## Deduplication

After tracing sources, remove duplicate files:
1. Compare MD5 hashes of same-named or same-sized files
2. Keep the project-registered version (MOC-ASEER-XX-XXX naming)
3. Remove the original-received copy (date-stamped name like `2026-05-08_*`)
4. Verify no broken references after removal
