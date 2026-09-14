# Returned-revision review checklist (SOW / scope documents)

Run this before telling the user a revision is issue-ready. Read the document text first
(`word/document.xml` → strip tags, or the extracted text), then check each block.

## 1. Edit-point coverage
Build the list of planned edits from the edit guide / CRS replies, then mark each:
applied / missing / wrongly applied. Expect partial application — the Revision field and
revision-history row are usually done while the substantive sections are not.

## 2. Response tables (RFI / comment / CRS tables)
- Read as **question → answer pairs**. A one-row shift makes every question carry its
  neighbour's answer; this is the most damaging defect because the reviewer spots it instantly.
- Row IDs should match the source document's own numbering (e.g. NRS RFI refs 1.1–1.12),
  not a fresh 1–N series; renumbering looks like the source was altered.
- The intro sentence must agree with the table: if it says "nine design intent / three client
  input", the table must show exactly that split, and must not also say "items 10–12 remain open".
- One source question = one row. Splitting a compound question into two rows changes the count
  and breaks the reconciliation with the reviewer's document.

## 3. Numbers and dates
- Cross-version counts ("nine (9) items" left over from a table with twelve).
- Issue Date and Revision History: both must carry the **resubmission** date, not the superseded one.
- Any `[__]` / `[TBC]` placeholder still in the text is an unissued field.

## 4. Document control block
- Document Ref field must hold the document number, not a revision value.
- Revision / Revision History consistent with each other and with the cover filename.
- Prepared / Reviewed / Approved names match the current project register (never invented).

## 5. Section numbering collisions
When the reviewer cites a section of a *different* document that collides with a number in ours
(e.g. "Section 5.5 of the Contractor's Scope of Works" vs our own 5.5), resolve it in the CRS
reply text — do not insert a numbering-note or cross-reference paragraph into the SOW.

## 6. Ambiguous matrix cells
A single cell holding two roles (e.g. "R/A") is ambiguous in a responsibility matrix — split the
row or separate the values, and confirm the Contractor row shows the contractor's own role
("Samaya (Contractor)"), never "Client".

## Reporting
Give the user a three-part result: **missing**, **errors**, **fix order** — and ask before editing
the document, even for mechanical fixes.
