Aseer Museum (project 219 on SAMAYA Odoo). NRS (A2742)=interior arch+scenography. Rawasin=AV/IT/interactives per T2-09. Subcon19 (Interactive Des). CG PM: Elbaz. Contract: MoC×Samaya, lump-sum, to 2026-09-30. Subcon RFI Reg: Docs/09_Registers/Subcontractor_RFI_Register/.
§
BIM Unit projects: Aseer-Museum/ (Design Files, 07_Daily_Reports, 09_Correspondence, Subcontractors, Contracts/01-08, Docs/02_Plans_and_Procedures, Docs/03_Inspection_Requests), Zamzam -Visitor Center/ (Submittal's, Docs). Doc prefixes: MOC-MUS-ASE (Aseer), ZAM-NWC (Zamzam).
§
Submittal registers: spec-first, Excel from spec. 50/90/100/IFC stages. Appendix B only. Odoo (proj 219): main=package (00-NN), subtasks=deliverables. State: 1_done/03_approved/02_changes_requested/01_in_progress. progress 0.0-1.0. Always date_assign+date_deadline. Kanban filter parent_id=False. Assign user_ids: [(4, uid)]. tag_ids for categories. Stage IDs: 35=Init, 36=DD, 39=Procurement, 659=Mfg, 40=Site. Non-DD pkgs skip 50/90/100/IFC stages.
§
Aseer team: Sultan Issa (ID 151, PM), Mohamed Samir (ID 564, Procurement), Hesham (ID 163, Site/Docs), Ahmed Salah (ID 162, Project Coord), Ali (ID 160, Technical Office), Adel Darwish (ID 7, PM). CG contacts: Hossam Mabrouk (hmabrouk@cg.com.sa), Mohammad Elbaz (melbaz@cg.com.sa). Baseline NTP 01-Dec-25, contract complete 07-Sep-26.
§
Shared memory repo: github.com/sultandroid/hermes-memory — cron sync every 2h via memory_github_sync.sh. User verifies work was actually done in Odoo after updates. Prefers one-task-at-a-time with action prompts.
§
For Samaya DOCX generation, load samaya-docx-template skill first (it has SamayaDoc class with correct navy #1E293B, Calibri 11pt, A4 margins 2.5/2.0cm, proper header/footer). Using wrong styling gets corrected.
§
Project separation is strict: Moqtana/Tqanny ≠ Aseer/Samaya. Never cross-reference. User gives free-form task direction — don't prompt with multiple-choice, let them say what they want.