# Plan Document Folder Structure Standard

## Purpose
Standardized internal folder hierarchy for all plan/procedure documents under `02_Plans_and_Procedures/02.{NN}_{Name}/`. Derived from the established pattern in 02.2_BEP_MIDP_TIDP, 02.4_PQP, and other mature folders.

## Structure

```
02.{NN}_{Name}/
├── 00_Master_Index/          ← Index, version control, document register
├── 01_Source_Files/
│   ├── 01_HTML/              ← HTML-rendered master document
│   ├── 02_PDFs/              ← Signed/stamped PDF copies
│   ├── 03_Word/              ← Editable DOCX source files
│   └── 04_Assets/            ← Images, diagrams, logos
├── 02_CG_Responses/          ← CG review comments, response sheets, CG_STATUS.md
├── 03_Supplementary/         ← Supporting scripts, calculators, tools
├── 04_Registers/             ← Related registers, matrices, logs
├── 05_Compliance_Audit/      ← Compliance mappings vs contract/ER/SOW
├── 06_Legacy_Files/          ← Superseded versions & obsolete drafts
├── 07_Guidelines/            ← External standards, templates, references
└── README.md                 ← Folder map with purpose & key documents
```

## When to Apply

1. **New plan document folder**: Create all directories at setup time, even if empty. The folders serve as placeholders for content that will be added over the document lifecycle.

2. **Expanding a minimal folder**: If a folder only has `01_Source_Files/` (common for newly drafted plans), add the missing standard subfolders.

3. **Template reference**: Use the BEP (02.2) or PQP (02.4) folders as the canonical reference — they have the most complete implementation.

## Notes

- Folders with only `01_HTML/` under `01_Source_Files/` will have `aseer_{name}.md` as the markdown source and `aseer_{name}.html` as the rendered output.
- The numeric prefixes (`00_`, `01_`, `02_`, etc.) keep the folders sorted consistently in Finder/Explorer.
- `02_CG_Responses/` stores the contractor's review feedback — always copy CG reply PDFs here in addition to any sidecar status files.
