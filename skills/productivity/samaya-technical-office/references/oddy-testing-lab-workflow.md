# Oddy Testing Lab — Key Session Learnings

## Supplier-Provided Cert vs Independent Oddy Test

This distinction applies across all subs, not just Oddy:

| Evidence type | What it is | Does it replace BM 3-month Oddy? |
|--------------|------------|----------------------------------|
| Greenguard Gold cert | Low-VOC emission certificate from manufacturer (e.g., Kvadrat Hallingdal 65) | ❌ No — it's low-VOC evidence, not material-suitability for object contact |
| Manufacturer Oddy light-fastness | Fabric fading/light resistance test from supplier (e.g., Creation Baumann Ultra V) | ❌ No — light-fastness ≠ off-gassing/corrosion. Must be independent BM 3-month Oddy |

**Rule:** Any material that contacts or shares atmosphere with museum objects must pass independent BM 3-month Oddy (60°C, 100% RH, copper/lead/silver coupons). Supplier certs are supporting evidence only.

## Duplicate Approval Docs

`07_Approvals/` often contains the same PDF under two names:
- Original-received: `2026-05-08_GGG_1000_SGreenguard-Certificate.pdf`
- Project-registered: `MOC-ASEER-MS-FB-001_KvadratHallingdal65_GreenguardGoldCert_Rev00.pdf`

**Fix:** Compare MD5 hashes. Keep project-registered version only. Remove original-received duplicate. Verify no broken references after removal.

## SOW Reference-to-File Verification

The SCOPE_REQUEST.md §6 (Reference Files) section MUST only list files that actually exist in the subfolder. After authoring, walk through every path and confirm the file is present. Missing files = invalid SOW. Copy them in or remove the reference.

## Samaya Standard SOW Format (10-Section)

| Section | Content |
|---------|---------|
| Metadata block | Project, Issuer, Issued to, Issue date, Reply by, Discipline, KPR ID, Subcontractor Register ID |
| Privity note | Blockquote — no privity with MoC/PMC/CG/NRS |
| §1 Purpose | Why this specialist is needed, authority basis |
| §2 Programme | Milestone table with calendar dates |
| §3 Scope of Work | Category tables, test specifications |
| §4 Deliverables | Per-stage deliverable table |
| §5 Submission Requirements | Numbered list of what bidder must provide |
| §6 Reference Files | Table mapping folder paths to content descriptions |
| §7 Workflow & Communication | SPOC, CDE, naming convention, RFI process |
| §8 Sign-offs | Table: sign-off, owner, trigger |
| §9 Commercial Terms | Payment, currency, confidentiality, IP |
| §10 Action | Confirm receipt + proposal deadline |
| Footer | Drafted by, Issue date, Linked Plans |
