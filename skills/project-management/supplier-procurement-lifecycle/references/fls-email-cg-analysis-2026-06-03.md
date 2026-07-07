# FLS Email & CG Analysis — 03 June 2026 Session

Real-world example of CG comment process-gate analysis from the FLS subcontractor dossier build.

## The Hidden Gate in CG Code C

**Situation:** IFC-0004 Life Safety Drawings submitted Rev.00 → Code C. Resubmitted Rev.01 → still Code C.

**Surface reading:** "Project Design Drawings must be approved first" (the PDD-first rule).

**Deep reading of the full email chain:** Maged Zamzam's internal review (23-Apr) and Mohammad Elbaz's formal response (25-Apr) both stated: *"cannot be reviewed in isolation without reference to and approval of the **Project Design Drawings** and **Fire & Life Safety Consultant approval**."*

**This revealed a hidden requirement:** CG expects the FLS Consultant (Nama) to endorse/stamp the life safety drawings before CG will review them. This means:
- It's not just about PDD approval sequence
- Nama must produce FLS design deliverables and stamp them
- Without Nama's formal engagement, IFC-0004 cannot progress regardless of PDD status

**Lesson:** Always read the full CG comment email chain, not just the transmittal form or Code letter. The "why" in CG's language often reveals additional process requirements beyond the stated code reason.

## Email Body Extract Locations

The most reliable source of email body text was NOT Email_Archive/ (where individual email .md files don't exist):

| Location | Contents |
|----------|----------|
| Scripts/output/email_bodies/ | Full email chain .txt extracts with headers (From/Date/Subject/Body) |
| Scripts/output/email_bodies/cg_responses/ | CG-specific response chains (IFC reviews, SI responses) |
| Email_Archive/hesham_archive_may2026.md | Summary of 40 Hesham emails (metadata only, no body text) |
| Email_Archive/CG_comprehensive_document_status_mapping.md | CG submission/response status mapping |

## Contractor Engagement Status Pattern

When assessing a subcontractor's engagement level:

| Pattern | Found for Nama | Interpretation |
|---------|---------------|----------------|
| MoC pre-approval exists | PQ-0025 (Feb 2026) | Authority vetting passed |
| Site work performed | IR-0001 (May 2026) | Physical presence at site |
| Formal contract signed | Not found | Legal engagement not formalised |
| Design deliverables produced | 0% | Design work not started |
| CG has interacted with them | Sundus Alfeer responded to survey | CG acknowledges their role |

Implication: A contractor can be "active" (survey done, MoC-approved) but "0% productive" (no design deliverables). The blocker is the unsigned SoW, not the contractor's capability.

## Source Discovery Order (FLS Run)

1. SCOPE_REQUEST.md -> define scope + deliverables
2. PROJECT_MEMORY.md -> identify open issues, IFC references, org structure
3. RFI_REGISTER.md -> find discipline-specific RFIs
4. PROJECT_EMAILS.md -> identify relevant submission emails
5. Scripts/output/email_bodies/ + cg_responses/ -> full email chains with CG language
6. Docs/02_Plans/02.1_DMP/04_Discipline_Files/ -> governing discipline file
7. Submittals/ -> actual submittal packages
8. Docs/03_Submittals/ -> IFC packages + CG comments
9. Docs/07_Reports/ -> discipline studies/reports
10. As-Built Docs/ -> existing record drawings
11. Completed Tender Package From NRS/ -> stamped approved drawings
12. Specs & Datasheet/ -> specifications
13. Design Files/ -> design PDFs and CAD
