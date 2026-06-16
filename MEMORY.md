Aseer team: Sultan Issa (ID 151, PM), Mohamed Samir (ID 564, Procurement), Hesham (ID 163, Site/Docs), Ahmed Salah (ID 162, Project Coord), Ali (ID 160, Technical Office), Adel Darwish (ID 7, PM). CG: Hossam Mabrouk (hmabrouk@cg.com.sa), Mohammad Elbaz (melbaz@cg.com.sa). AD Engineering: Osama Abdel Shafi Moustafa (osama@adeng.com.sa, main), Info@adeng.com.sa, supervision@adeng.com.sa. Domain: adeng.com.sa. NTP 01-Dec-25, contract complete 07-Sep-26.
§
For Samaya DOCX generation, load samaya-docx-template skill first (it has SamayaDoc class with correct navy #1E293B, Calibri 11pt, A4 margins 2.5/2.0cm, proper header/footer). Using wrong styling gets corrected.
§
Project separation is strict: Moqtana/Tqanny ≠ Aseer/Samaya. Never cross-reference. User gives free-form task direction — don't prompt with multiple-choice, let them say what they want.
§
KSA weekend is Friday-Saturday. Never set deadlines on Friday (day off). When user says "before next Monday" and today is Monday, deadline is Thursday (end of work week).
§
Odoo task deadline dates must comply with baseline programme, not arbitrary far-off dates. Always set realistic/aggressive deadlines aligned to programme.
§
Odoo stage assignment: Stage 36 (DD) = design/engineering work only. Stage 39 (Procurement) = material samples, supplier submissions, procurement items. Stage 659 (Off-site Manufacturing) = production/manufacturing orders. Stage 40 (On-site) = construction/installation. Never put procurement or manufacturing items in DD stage.
§
Odoo→folders: 166=JabalOmarRetails01, 176=JabalOmarRetails02, 121=Zamzam-VC, 219=Aseer-Museum.
§
When writing to Excel with openpyxl, ensure file is closed first (not open in Excel). Verify by re-reading after save. Delete rows in reverse order (highest row number first) to avoid index shifts.