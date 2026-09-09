# Material Submittal Code C Resubmission — CRS Strategy

Session-derived playbook for responding to a CG **Code C (Revise & Resubmit)** on a material submittal (e.g. MA-0007 Patinated Brass). Use when the user says "prepare the resubmission for the Code C material submittal" or "generate CRS sheet".

## 1. Pull the authoritative status first
- Query the submission DB (single source of truth per AGENTS.md rule 10a):
  `sqlite3 08_Document_Index/submission.db "SELECT s.doc_no, s.title, s.revision, st.code, st.label, s.is_latest FROM submission s JOIN status st ON s.status_id=st.id WHERE s.doc_no LIKE '%<REF>%' ORDER BY s.revision;"`
- The DB shows the CURRENT code (C/D = open risk; B = practical approval). Do NOT trust `materials.json` or stale registers for codes.

## 2. Build the CRS on the OFFICIAL template
- Fetch `https://samaya-factory.com/assets/templates/CRS_Template_MOC_HQ.xlsx` (MOC_HQ Comments Resolution Sheet). Do NOT build a custom Excel CRS from scratch.
- Fill header block (doc no, rev, title, date, discipline) + one comment row per CG requirement.
- Columns: No. | Initial | Sheet | Reviewer Comment | Originator Reply | Reply By | Reply Status by Reviewer.
- **Reply Status by Reviewer is filled by CG, not us** — we put a provisional Closed/Open, CG sets the final.

## 3. Classify each CG requirement into a status
| Status | Meaning | Example |
|--------|---------|---------|
| **COMPLIED** | Evidence in hand | Oddy test PASS, chemical composition datasheet, manufacturer details |
| **PENDING** | Supplier lead-time, follow as Rev.02 addendum | VOC, off-gassing, fire-rated, MSDS |
| **PARTIAL** | One of several items done | 2 alternatives: Option A submitted, Option B in development |

## 4. Challenge over-requested certificates (don't blindly comply)
Not every CG requirement is technically justified. Classify each:
- **Oddy test** — legitimate for museums (protects artifacts from corrosive emissions). The decisive one.
- **Chemical composition** — legitimate; a manufacturer datasheet (e.g. KME CuZn37/C27200) satisfies it.
- **MSDS** — legitimate, easy (a document, not a test).
- **VOC** — only matters for sealed/closed spaces (showcase interiors); metals themselves don't emit VOC — the lacquer/coating does. Can be scoped to closed spaces only.
- **Off-gassing** — REDUNDANT with Oddy (Oddy already confirms no corrosive emissions). Challenge as duplication.
- **Fire-rated** — OVER-REQUESTED for metal (non-combustible). Challenge with technical note.
- **2 alternative manufacturers** — may be IMPOSSIBLE if single-source (e.g. Glasbau Hahn confirmed only one global supplier). Document the single-source constraint (supplier letter) and offer supplementary options instead.

Framing: "We present the passed Oddy test + composition + MSDS now; the remaining certs follow as Rev.02 addendum within 30 days. We request Rev.01 approval on the strength of the Oddy pass so the programme is not delayed." This puts the delay risk on CG if they refuse.

## 5. The Oddy-pass is the decisive fix
When a test report arrives (e.g. NonaChem T2607222, rated P = Permanent on Ag/Cu/Pb), it directly clears the highest-risk item that drove the Code C. Lead the resubmission with it. Update the risk register (e.g. PRR-PRC-05) — a passed Oddy lowers probability; per AGENTS.md rule 10, Code B closes the risk.

## 6. Deploy the template + reference it
- Upload the template to `samaya-factory.com/assets/templates/` (SSH pipe + chmod 644).
- Add a row to the repo `AGENTS.md` style-guide table so every agent knows the public URL.
- Save the filled CRS to the OneDrive submittal folder (e.g. `.../MA-007 Rev01/20260908_MA-0007_Rev01_CRS.xlsx`).

## Pitfalls
- **OneDrive deadlock** ("Resource deadlock avoided") blocks reading/writing OneDrive files. Quit OneDrive, wait ~30s, retry; or copy via `cat` to /tmp. Do not fabricate file contents.
- **Verify against the approved PDF, not just materials.json** — materials.json can be missing items that ARE in the approved schedule (e.g. FI_GR_11 Wayfinding Signage was in the PDF but absent from materials.json). When the user says "double check is this all", re-read the approved PDF.
- **Thickness is application-dependent** for finish/look-and-feel samples — do not hardcode one gauge.
