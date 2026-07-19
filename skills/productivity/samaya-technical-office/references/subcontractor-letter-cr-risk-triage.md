# Subcontractor Letter → CR Sheet → Risk Register Triage

When CG requests action on a material submittal (e.g., MA-0007 Patinated Brass) and the subcontractor sends a letter with their position, use this triage workflow to decide next steps.

## Trigger

CG sends a comment/request (e.g., "provide 2 alternative certified manufacturers" or "provide test reports"). Subcontractor simultaneously sends a letter stating their position (e.g., "we don't recommend this material" or "test results expected end of August").

## Workflow

### 1. Read the subcontractor letter

Scanned PDF letters from subcontractors (Glasbau Hahn, etc.) are typically image-based. Use the `document-analysis` skill's OCR pipeline:

```python
# macOS: sips → pytesseract (simplest for single-page scanned letters)
import pytesseract
from PIL import Image
img = Image.open('/tmp/letter.png')
text = pytesseract.image_to_string(img, lang='eng')
```

Key things to extract from the letter:
- **Date** — when was it sent
- **Subcontractor's position** — do they recommend or advise against the material?
- **Timeline** — when will test results/certificates be available?
- **Risk warnings** — any explicit disclaimers about material performance
- **Requests** — do they ask for anything (e.g., "don't hold shop drawing approval")

### 2. Read the CR sheet

The CR sheet (Comment Response Sheet) is the formal response to CG. Find it in the subcontractor's `06_Correspondence/` folder. Key items to check:

- **Which CG comments are already addressed** — items 4-5 typically cover MA-0007
- **What's the proposed strategy** — e.g., "approve look & feel now, test reports to follow"
- **What's the status** — CLOSED, PARTIAL, REQUESTED, OPEN
- **Does the CR sheet already account for the subcontractor's position?** If not, it needs updating

### 3. Check the risk register

Search the Master Risk Register (PRR) for existing coverage of this material risk:

- **Risk ID** — e.g., PRR-PRC-05 for patinated brass
- **Current score** — P × S (1-4 scale)
- **Rating** — Critical / High / Medium / Low
- **Mitigation** — what's already planned
- **Status** — Open / Watch / Mitigated

If the subcontractor's letter introduces NEW risk information (e.g., "only 1 supplier exists" when CG asked for 3 alternatives), the risk score may need upgrading.

### 4. Cross-reference the three sources

| Source | Key Question |
|--------|-------------|
| Subcontractor letter | What is their position and timeline? |
| CR sheet | What response strategy is already drafted? |
| Risk register | Is this risk already captured and scored? |

**Common patterns:**

| Pattern | Action |
|---------|--------|
| CR sheet already addresses the issue | Update CR with subcontractor's letter as supporting evidence, resubmit |
| Subcontractor contradicts CG request | Update CR to reflect subcontractor's position, propose alternative path (e.g., PVD-coated alternative) |
| Risk not captured or under-scored | Add/upgrade risk in PRR, link to DDR |
| Subcontractor letter changes timeline | Update risk register with new dates, flag schedule impact |

### 5. Present options to user

Don't offer multiple-choice menus. Present the situation clearly:

```
GBH Letter 002 (16 Jul):
- No Oddy test reports available — submitting for testing, results end of August
- GBH does NOT recommend patinated brass (5 reasons: limited supply, result not guaranteed, colour inconsistency, matching issues, time-consuming)
- Request that brass approval not hold shop drawing approval

CR Sheet (MA-0006 Rev.01):
- Items 4-5 already address MA-0007 — requesting CG approve look & feel now
- Item 6 argues Glasbau Hahn is sole approved specialist

Risk Register (PRR-PRC-05):
- Already recorded: Oddy failure + finish matching risk — Score 12 (Critical), Open

GBH's position (don't use patinated brass) contradicts CG's request (provide 2 alternatives).
What do you want to do?
```

### 6. Update CR sheet if needed

If the user decides to update the CR sheet:
- Add the subcontractor's letter as a supporting document reference
- Update the response text to reflect the subcontractor's position
- If proposing an alternative (e.g., PVD-coated), add it as a new commitment
- Bump the CR sheet revision number

### 7. Update risk register if needed

If the subcontractor's letter elevates the risk:
- Upgrade probability/severity scores
- Add the letter as an evidence source
- Update mitigation/controls with the new information
- Change status if needed (e.g., Open → Escalated)

## Pitfalls

1. **Scanned PDFs may be image-based** — pdftotext returns empty. Use sips + pytesseract, not pdftotext.
2. **tesseract /tmp path issue on macOS** — Copy to CWD or use Python pytesseract instead of CLI.
3. **CR sheet may be on OneDrive** — If locked, hydrate via `open` (Preview) first.
4. **Risk register may have multiple versions** — Use the REV00 master register, not older C09 or v2.0 copies.
5. **Subcontractor letter may contradict the CR sheet strategy** — Don't send the CR sheet as-is if the subcontractor's position has changed. Update first.
6. **GBH letter may be a scanned PDF from a Canon copier** — These are image-based (no text layer). Always verify with `pdfinfo` producer field: "Canon iR-ADV" = scanned, no text layer.
