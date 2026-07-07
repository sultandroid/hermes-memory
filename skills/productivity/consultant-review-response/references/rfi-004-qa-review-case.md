# RFI-004 QA Review — Reference Case

**Document:** FORMAL_RFI_004_CG_MoC_Content (Graphics Sub-08 — Exhibition Text & Content Delivery)
**Date:** 25-Jun-2026
**Verdict:** ISSUE (after fixes applied)

## Key Findings

### Blocker Found & Fixed
| Finding | Source Quote | Actual ER Text | Fix |
|---------|-------------|----------------|-----|
| Evidence D quoted fabricated ER §1.3 text | *"The Contractor shall coordinate graphic content placement with scenographers to ensure alignment with exhibition narrative and spatial layout."* | ER §1.3 Item 9: *"Coordinate the design of the Works with the design of the Scenographers Works, where stipulated herein."* | Replaced with verbatim ER text |

### User-Directed Acknowledged Items
| Item | User Direction |
|------|---------------|
| Doc reference number | DC adds at issue — not Technical Office gap |
| Response deadline | Handled via Aconex DS form workflow — not needed in document body |
| Curator on distribution | Not required — current list (MoC · CG · PMC · Samaya Tech Office) sufficient |
| Q4.1–4.2 pre-fill | Leave as questions — PM to decide |
| WITHOUT PREJUDICE clause | Added — always include on scope-boundary RFIs |

### Evidence Verification Results
All 6 evidence items (A–F) verified against source PDFs:
- **A** (SOW §2.2): PASS — semantic match
- **B** (SOW p.17): PASS — all 5 items confirmed
- **C** (SOW §8.14): PASS — verbatim match
- **D** (ER §1.3): FIXED — now verbatim
- **E** (Briefing Pack M2): PASS — close match
- **F** (Programme): PASS — dates confirmed

## Verification Method
1. Locate source PDF
2. `pdftotext <pdf> - | grep -n <clause>` to find section
3. `pdftotext <pdf> - | sed -n '<start>,<end>p'` to extract context
4. Compare quoted text vs source text character by character

## Relative Path Check
```python
import os
rel = '../../../../../_Style-Guides/samaya-rfi-style-guide/assets/samaya.png'
resolved = os.path.abspath(rel)
print(f'Exists: {os.path.exists(resolved)}')
```
