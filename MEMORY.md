Aseer Museum: PD M.Waris Khan. MEP scope: power to specialist systems only. Namaa FLS: P01167 (SAR70k safety), P01449 (SAR23k survey). Not full FLS design. Task 3050 in Initiation.
§
Samaya Odoo PO cashout: state=purchase/done, exclude full-received <1K SAR. Paid: P00893,P00744,P01154,P01331,P01289,P01227,P01222,P01023,P00908,P01587. Supplier 1224=Saba Najad — vendor accounts Samaya owes, not cash.
§
Deploy: build with `node node_modules/vite/bin/vite.js build` (npm run build times out). Then tar index.html+assets/+sync.php, SSH pipe to samaya-factory.com:65002 as u517606786 to build/aseer/. Admin: ?admin=1, pw aseer2026. Fix public/aseer/images symlink if OneDrive resets it.
§
OneDrive macOS: Never write files directly to OneDrive path (CloudStorage or Group Containers) — both produce corrupt/placeholder files. Stage to /tmp, then AppleScript `duplicate src to dest with replacing` via Finder. Verify with `xxd -l 8` (must start PK\x03\x04).
§
SAMAYADOC RULE: For any .docx, load samaya-docx-template skill first, then use SamayaDoc class. NEVER hand-craft styles. NEVER use § symbol — write "Section X.Y". add_h2(number_str, text). add_table(rows, headers) WITHOUT col_widths_cm. Run via terminal(), copy to OneDrive via AppleScript. Always check project plans (Comm Plan 02.7, Stakeholder Plan 02.13) before creating docs — align coordination/ reporting sections with them.
§
Aconex CDE: URL=constructionandengineering.oraclecloud.com, acct=sultan@samayainvest.com. Aseer Museum on KSA1. Monitored via Outlook notifications (sender: "Aconex Notification") + browser. Daily 9AM cron checks for new transmittals, submittals, RFIs, SIs, Code responses.
§
Samaya logo: Always use the real bilingual PNG from _Style-Guides/logos archives/samaya-logo-trans.png (lowercase "samaya" with red "a" + "investment"). Never create fake SVG text approximations (uppercase wordmarks, diamond accents, etc.). For small headers use `<img>` with the PNG, not inline SVG.
§
RCRC Exhibition project uses ACC (Autodesk Construction Cloud) as CDE platform, NOT Aconex. Workflow: Revit → ACC Docs → Navisworks clash detection → ACC Review/Transmittal → Approval → Publish.