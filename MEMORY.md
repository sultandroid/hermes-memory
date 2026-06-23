Aseer: PD M.Waris (m.waris@samayainvest.com), NOT Adel Darwish. Adel is Projects Director support role. QC Mgr: Abd Elmohaymen Medhat. QA/QC Mgr: same person.
§
Sheet numbering: ID treated as architectural sub-discipline — use AR code for all interior design/fit-out/exhibition drawings. No separate ID code. BEP Table 30 codes mandatory. 3-digit sequential numbering. Type system 0-6 (US NCS). Confirmed with Tech Office Mgr.
§
CG doc rules: cite only ER/SOW/DMP — no PD/internal sources. No invented tiers. KPR-approved names only. Tiers per DMP. No status commentary on TBC/Vacant roles (no 'pending submission', 'in progress', 'Code C'). Firm-assigned roles get factual status (e.g. 'Rawasen — pending approved'). Page balance: compact CSS first. Compact redesign: compress table padding 1-2px, font 0.35-0.4rem, single-row ribbons for cards, group roles into tier rows, 2-col layout. Electrical Eng. labeled on site, not HO.
§
Design Risk Register: 06_Design_Risk_Register/Aseer_Museum_Design_Risk_Register.xlsx. Columns B-K (B=Risk ID, C=Category, D=Description, E=Consequences, F=P, G=I, H=PxI, I=Owner, K=Mitigation). New entries match existing formatting: purple fill #F3E5F5, thin borders, wrap text, bold risk ID in col B. Last entry row 79 (COM-CM-004). New: CO-X-003 (light box/acoustic baffle gap between NRS S2, Museum Studio S3 visuals, ZNA — no detail coverage), CO-X-004 (BF/LGF/GF/FF numbering overrides 1000 sequence).
§
CV pack workflow: Document Control block — empty Doc No./Rev/Date/Status (for DOC to fill), only Distribution pre-filled. QC Approved by = PD Muhammad Waris Sultan Khan, never Adel Darwish.
§
Odoo PO tracker: live via JSON-RPC. Exclude: receipt=full, draft/cancel state, invoice=invoiced, posted bill with payment=paid. Check account.move for real payment. receipt_status: bool False=Not Recorded, str 'pending'=Not Received. buyer_id field blocked. Factory projects: 244,302,315. Exclude Mada Aljezera & Saba Najad vendors.
§
Always delegate heavy data extraction to sub-agents (delegate_task with terminal/file toolsets) rather than using execute_code or inline Python for large Excel/PDF reads. Mentioned explicitly: "all alwayes delegate to labors."