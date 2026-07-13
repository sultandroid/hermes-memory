# Stakeholder Plan Data Conciseness — Rules for SMP-Style Documents

## When to use

When generating or updating any Stakeholder Management Plan, CG-facing document, or project register where the user has corrected you about verbose/stale/internal detail.

## Core Rules

### 1. Stakeholder descriptions — no internal tracking detail

Every stakeholder cell in a register must answer only: **who they are, what they do, their status.** No procurement, fee, CV, or register-reference detail.

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| AD Engineering — PO issued Jun 21 - kick-off Jun 25 - agreed 18-May-26 | AD Engineering - MEP Design |
| Studio ZNA — Fee 40,527 approved - Julie Riley | Studio ZNA - Lighting Designer |
| TBC - Target: CP-2 Decision - Per KP Register Rev C02 | TBC |
| Eng. Ahmed Gad - CV submitted | TBD |
| Samaya Factory - Pending - waiting object research from client | Samaya Factory |
| Muhammad Fida - CV approved by CG Jun 24 - PO SAR 12,000/month | Muhammad Fida |

**Strip from all stakeholder entries:**
- CV status (submitted, via DS, approved)
- PQD status (submitted, under submission, to be submitted)
- PO / fee / contract details
- Target gates/decisions ("CP-2 Decision", "CP-1 Mobilisation")
- Register references ("Per KP Register Rev C02")
- Internal notes ("waiting object research from client", "pending CG/MoC approval")
- Sub-contractor references like "Radiance Group" (use Dr. Waleed only)

### 2. CG comments go in the CR sheet — not the plan

Never embed full CG comment-by-comment disposition tables in the plan document. Replace with a 4-row summary:

```
Round 1:      8 comments (9-Mar-26) — Closed in Rev 02
Round 2 CRS:  17 comments (2-Jun-26, Code C) — Closed in Rev 02
CG Approval:  ZD-0020 Rev.02 approved by CG (Jun 18-24)
Reference:    Full disposition per attached CR sheet
```

### 3. Verify every name against the repo before writing

The authoritative sources for Aseer Museum personnel are (in order):
1. `Technical_Office/Specialist_Management/specialist_register.md`
2. `03_Plans/10_Resource/resource_management_plan.md`
3. `99_Archive/00_Project_Overview/PROJECT_MEMORY.md`

Verified names as of July 2026:

| Role | Name | Source |
|------|------|--------|
| Project Director | Eng. Waris Sultan | specialist_register.md |
| BIM Manager | Dr. Waleed Salah | specialist_register.md |
| Technical Office Manager | Eng. Mohamed Sultan | specialist_register.md |
| HSSE Manager | Eng. Mohamed Ahmed | specialist_register.md |
| QA/QC Manager | Vacant (Samir acting) | specialist_register.md |
| Site/Construction Manager | Mohamed Samir | task_mapping.md |
| Procurement Manager | Hani Alghamdi | resource_management_plan.md |
| Document Controller | Eng. Hesham Abdelhamid | resource_management_plan.md |
| Sustainability Specialist | Muhammad Fida | specialist_register.md |
| MEP Design | AD Engineering | specialist_register.md |
| Lighting Design | Studio ZNA | specialist_register.md |
| AV/IT Systems | Rawasin | specialist_register.md |
| Showcases | Glasbau Hahn | specialist_register.md |
| Interior Architect | Ali Abdelrahman | resource_management_plan.md |
| Interactive Design | TBD (Lumotion declined) | specialist_register.md |
| Scenographer | NRS | specialist_register.md |
| Graphics | Samaya-Graphic (Approved) | specialist_register.md |
| BIM Consultant | Dr. Waleed (not Radiance Group) | specialist_register.md |
| Structural Engineer | TBD | specialist_register.md |
| IT/Data Authority Liaison | TBD | user correction |
| Cafe Sunshade | Samaya Factory (fab) / NRS (design) | specialist_register.md |
| Models & Props | Samaya Factory | specialist_register.md |

### 4. QC sign-off roles — use correct titles

| Role in register | Correct title | Person |
|-----------------|---------------|--------|
| QC-01 | Technical Office Manager | Eng. Mohamed Sultan |
| QC-02 | Document Controller | Eng. Hesham Abdelhamid |
| QC-03 | QA/QC Manager | Mohamed Samir (on behalf) |
| QC-04 | Project Director | Eng. Waris Sultan |

### 5. Revision history — formal submissions only

Only include revisions formally submitted to CG. Internal drafts between submissions must not appear. Each entry needs real names, not "Samaya PMO".

### 6. Section symbols and AI fingerprints

- Replace all `§` / `&sect;` with "Sec."
- Replace all em-dash (—), en-dash (–), middle dot (·) with plain hyphens
- Replace smart quotes with straight quotes
- Remove AI-sounding phrases: "seamlessly", "utilize", "leverage", "robust", "holistic", "innovative", "bespoke", "cutting-edge", "state-of-the-art", "synergistic"
- Remove meta-commentary: "as shown above", "it should be noted", "the following sections"
- Write like an engineer: short sentences, active voice, no filler
