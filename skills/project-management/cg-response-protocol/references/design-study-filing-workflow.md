# Design Study Filing Workflow

When NRS submits a design study in response to CG/Ministry object schedule requests:

## Folder Structure

```
Aseer-Museum/
└── 12_Design_Studies/
    ├── 01_Object_List/          (object schedule files from email thread)
    ├── 02_New_Study/            (future studies)
    └── 03_Study_01/             (per-study folder, increment serial)
        ├── MOC-ASE-AR-ARC-GEN-DDD-DS01-00_DRAFT.pdf   (NRS study PDF)
        ├── G12_Structural_Assessment_Template.docx     (team action templates)
        └── G12_Logistics_Method_Statement_Template.docx
```

## Object List Subfolder Organization

```
01_Object_List/
├── 01_Emails/              (email transcripts from the thread)
├── 02_Mapping/             (Object_to_Showcase_Mapping.xlsx)
├── 03_Drawings/            (LGF drawings, showcase plans, RFI refs)
├── 04_Showcase_Refs/       (showcase type drawings, e.g. DT_4005-Type 5A)
└── 05_Reference_Images/    (screenshots, lighting refs, videos)
```

## Extraction Workflow

1. Find the email thread via Conversation_ConversationID in Outlook SQLite
2. Extract attachments from key emails (your request, NRS replies, internal replies)
3. Save email bodies as .txt files with prefix `email_{id}_{sender_description}.txt`
4. Organize attachments by type into subfolders
5. Copy the study PDF into the study folder

## G12 Team Action Templates

When NRS proposes structural changes (e.g. 3-4 ton stone on open plinth), generate Samaya-branded DOCX templates for the team:

### Structural Assessment Template
- Object details table
- Loading assessment checklist (slab capacity, screed, tiling, point load, safety factor, reinforcement)
- Plinth design requirements (dimensions, spreader plates, connection detail, vibration)
- Findings & recommendations section
- Approval block (Prepared/Reviewed/Approved)

### Logistics Method Statement Template
- Object details table
- Access route checklist (entry point, clearances, obstructions, floor loading)
- Lifting equipment table (crane, forklift, spreader beam, rollers)
- Handling procedure (5 blank steps)
- Safety considerations checklist
- Required approvals table
- Approval block

Generate via SamayaDoc class from `samaya_doc_template.py`. Save to both:
- `11_Standards_and_Skills/03_Templates/Structural/` (reusable)
- `12_Design_Studies/03_Study_01/` (alongside the study PDF)
