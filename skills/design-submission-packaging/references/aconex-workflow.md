# Aconex Upload & Transmittal Workflow

How to upload design drawing packages to Oracle Aconex and create formal Transmittals for CG review.

## Prerequisites

- Aconex/Oracle C&E login (URL: https://constructionandengineering.oraclecloud.com)
- Project: Aseer Museum (KSA1 region)
- Drawings prepared in packages (see SKILL.md)

## Browser Login Flow

1. Navigate to https://constructionandengineering.oraclecloud.com/ui/v1/login
2. Enter username → click Next
3. Enter password → click Sign In
4. Accept cookie policy if prompted
5. Click on the project row → either click the application element directly or use "Action" → "Open in Application"

## Navigation

- Home tab: Dashboard showing Mail/Documents/Packages counts per user
- **Documents tab**: Document Register (125 docs as of Jun 2026) — search, filter by status/type/discipline
- **Packages tab**: Submittal packages with review workflows
- **Mail tab**: Project correspondence / transmittals

## Uploading Drawings to Document Register

1. Navigate to **Documents** → **Document Register**
2. Click **Add or Update Documents** (button in the search results toolbar)
3. Select files to upload
4. Fill metadata: Document No, Title, Type (Design Drawing), Discipline, Revision, Status
5. Submit

## Creating a Transmittal for CG Review

1. Navigate to **Mail** → **New Mail**
2. Select recipients (CG reviewers: Mohammad Elbaz, Maged Zamzam, etc.)
3. Attach drawings from Document Register
4. Set workflow: Samaya review → CG review (set review period per complexity)
5. Submit

## Limitations

- The Aconex SPA inside an iframe is cross-origin — JavaScript cannot read document data from outside the iframe
- Bulk export: Use Reports → Export to Excel for offline analysis
- Snapshot tool captures visible grid content but truncates large datasets (>~100 rows)

## Importing Aconex Export into Submission Plan

The ExportDocs Excel contains: File, Document No, Revision, Version, Title, Type, Review Source, Status, Review Status, Discipline, Created By, Revision Date, Date Modified, Related Items, Size, Lock

To reconcile against the submission plan:
1. Match by Document No (MOC-MUS-ASE-xxxx) or by Title+Discipline for short codes
2. Update submission plan Status column with Aconex Review Status
3. Update Actual Date with Aconex Revision Date
4. Flag items in Aconex but not in plan (and vice versa)