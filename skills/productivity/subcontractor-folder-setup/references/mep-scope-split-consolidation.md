# MEP Scope Split — Designer vs Contractor (Consolidation Pattern)

## Background

On the Aseer Museum project, MEP works are split across two distinct roles:

| Role | Folder | Scope |
|------|--------|-------|
| **MEP Designer** | `18_MEP_Designer/` | Engineering consultant — IFC drawings, load calculations, BIM modelling (Revit MEP LOD 300+), coordination |
| **MEP Contractor** | `12_MEP_Contractor/` | Single entity for supply + installation — HVAC, Electrical, Plumbing, Fire-Fighting, BMS (5 sub-trades) |

## The trap: 3 folders for MEP

The initial filing had **3 folders** for MEP when only 2 were needed:

1. `12_MEP_Installation` — created first (2026-05-10), comprehensive scope doc
2. `14a_MEP_Contractor` — added later (2026-06-07), brief scope doc
3. `18_MEP_Designer` — design consultant

The `14a` entry (suffix between 14_Rigging and 15_FFE) signals it was a **late addition** after the initial numbering was locked. It was created because someone distinguished "installation" from "contractor" as if they were separate entities — but on this project they are the **same entity**.

## Consolidation procedure

When you find duplicate discipline folders:

1. **Verify with project docs** — read both SCOPE_REQUEST.md files. Do they describe different contractual scopes or the same scope?
2. **Check file contents** — if one folder has richer content (detailed SCOPE_REQUEST, filed documents), keep that one
3. **Rename** — update the survivor's folder name to reflect the consolidated role (e.g., `12_MEP_Installation` → `12_MEP_Contractor`)
4. **Delete** — remove the duplicate folder
5. **Move misfiled offers** — `09_Offers/` in the contractor folder may contain **design consultancy proposals** that belong under the Designer folder. Always verify before moving or deleting.

## Cross-folder offers check

Proposal PDFs in `09_Offers/` may belong to a *different* discipline than the folder they're in:

- `260520_ASIR_MUSM_3343_Design Consultancy Proposal.pdf` — the file name says "Design Consultancy" but was filed under `12_MEP_Contractor/09_Offers/`. This belongs under `18_MEP_Designer/09_Offers/`.
- Always check: read the filename, title page, or metadata to confirm the actual scope before deciding.

## Prequalification ≠ Offers (separate phases)

Prequalification documents (company profiles, qualifications, capability statements, ISO certificates, financial statements) are **not offers** and must **not** be filed inside `09_Offers/`. They go in `00_Prequalification/` at the subcontractor folder root.

Rule of thumb:
- **00_Prequalification/** — "can they do the work?" (qualifications, experience, capacity)
- **09_Offers/<Company>/** — "how much will they charge?" (priced proposals, BOQ, commercial offer)

Each company gets its own subfolder in **both** `00_Prequalification/` and `09_Offers/`:

```
00_Prequalification/
├── AD_Engineering/         (21 prequal files)
└── SG_Group/               (qualifications PDFs)

09_Offers/
├── AD_Engineering/
│   └── Technical_and_Financial_Offer.pdf
├── BluHaus/
│   └── 260520_ASIR_MUSM_3343_Design Consultancy Proposal.pdf
├── SG_Group/
│   └── Aseer Museum Quotaion.pdf
└── MEP_Design_Offer/       (if company unknown, use descriptive name)
```

## Duplicate file detection

When a new file arrives (e.g., from WhatsApp or email attachment), check if it's already on file before copying:

```bash
md5 "/path/to/new/file.pdf" "/path/to/existing/file.pdf"
```

If MD5 hashes match, it's a duplicate — skip the copy and report to the user.

## WhatsApp attachment sourcing

Files arriving from WhatsApp land under temp UUID paths:

```
~/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/<UUID>/filename.pdf
```

Always copy (cp) instead of mv from these paths — the WhatsApp container may still need the original. Delete from Downloads/WhatsApp tmp only after confirming the copy landed correctly.

## Arabic-language documents → rename to English

KSA subcontractors commonly submit Arabic-named files. **Do not keep Arabic filenames** — rename them to descriptive English names reflecting the document content, using the same numbering prefix.

Translation guide for common Arabic document names found in MEP subcontractor submissions:

| Arabic filename | English rename |
|---|---|
| `العرض الفني والمالي.pdf` | `Technical_and_Financial_Offer.pdf` |
| `بروفايل الشركة.pdf` | `00_Company_Profile.pdf` |
| `نموذج التقييم الفني - شركة X.pdf` | `01_Technical_Evaluation_Form_X.pdf` |
| `معلومات عن الشركة والأجهزة والبرامج.pdf` | `02_Company_Info_Equipment_Software.pdf` |
| `الهيكل التنظيمي لشركة X.pdf` | `03_Organizational_Structure_X.pdf` |
| `الالتزام بتنفيذ الأعمال بالمشاريع.pdf` | `06_Project_Execution_Commitment.pdf` |
| `نموذج استطلاع رأي المالك مشاريع التصميم.pdf` | `06_Owner_Satisfaction_Survey_Design_Projects.pdf` |
| `شهادات الإنجاز لمشاريع سابقة.pdf` | `07_Completion_Certificates_Previous_Projects.pdf` |
| `شهادات الأيزو.pdf` | `08_ISO_Certificates.pdf` |
| `شهادة التوطين - قوى.pdf` | `09_Saudization_Certificate_Quwa.pdf` |
| `نموذج التأهيل .pdf` | `1.1_Qualification_Form.pdf` |
| `الشهادات والوثائق الرسمية للشركة محدثة - X.pdf` | `1.2_Official_Company_Certificates_Updated_X.pdf` |
| `خطة التدريب ونقل المعرفة.pdf` | `1.3_Training_and_Knowledge_Transfer_Plan.pdf` |
| `خطة إدارة الجودة.pdf` | `1.3_Quality_Management_Plan.pdf` |
| `خطة إدارة المخاطر والطوارئ والأزمات.pdf` | `1.3_Risk_Emergency_Crisis_Management_Plan.pdf` |
| `خطة نظام البيئة والأمن والسلامة.pdf` | `1.3_Environmental_Health_Safety_Plan.pdf` |
| `منهجية شركة X في تصميم المشاريع.pdf` | `1.3_X_Design_Methodology.pdf` |
| `نموذج الخبرات السابقة في مجال التصميم.pdf` | `1.4_Previous_Design_Experience.pdf` |
| `خطاب ترسية المنافسة N مشروع X.pdf` | `1.5_Award_Letter_N_X.pdf` |
| `عقد دراسة وتصميم X بعد التوقيع.pdf` | `1.5_X_Study_Design_Contract_Signed.pdf` |
| `نماذج السير الذاتية المقترحة لفريق العمل.pdf` | `1.6_Proposed_Team_CVs.pdf` |
| `شهادة التصنيف - شركة X.pdf` | `10_Classification_Certificate_X.pdf` |
| `شهادة الإلتزام - التأمينات الإجتماعية.pdf` | `11_Social_Insurance_Compliance_Certificate.pdf` |

Rules:
- **Keep numbering prefix** (e.g., `00_`, `1.3_`) to maintain sort order
- **Use underscores** between words, not spaces
- **Keep existing English-only files as-is** (e.g., `00 AD Engineering Company Profile .pdf`, `04 Financial Statements - 2024 - 2023 - 2022.pdf`)
- **Company names within filenames**: keep as suffix (e.g., `_AD_Engineering`)
- After renaming, verify no Arabic characters remain in filenames

## Result after consolidation

```
12_MEP_Contractor/     ← Contractor (supply + installation, 5 sub-trades)
18_MEP_Designer/       ← Design consultant (engineering design only)
```

## README update

After consolidation, update the register table in `Subcontractors/README.md`:
- Change discipline name from "MEP Installation" → "MEP Contractor"
- No need to remove the 14a row if it was never listed in the README (it was an orphan folder)
