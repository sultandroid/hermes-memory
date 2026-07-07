# Proposal HTML Development Guide for Samaya

## Toolchain
- **Design/restructure** → delegate to Claude Code (big patches, CSS, page reordering)
- **Deployment** → Surge.sh via `surge /tmp/deploy-dir/ <domain>.surge.sh`
- **Excel BOQ** → system Python 3 + openpyxl (sandbox Python does NOT have openpyxl; run via `python3 /tmp/script.py`)
- **PDF extraction** → `pdftoppm -jpeg -r 150` (convert to JPG), `sips -Z <size> -s formatOptions <quality>` (compress)
- **Document analysis / QC review** → delegate to Kimi (`kimi -p`) or Codex (`codex exec`)
- **SVG charts (Gantt, diagrams, workflows)** → delegate to Claude

## Critical Conventions

### Content rules (Samaya proposals)
1. **No galvanizing** — steel structure uses Epoxy paint system (Jotun Epoxy Mastic ≥200µm DFT)
2. **No specific HSS profile dimensions** — steel section depends on structural calculation; say "HSS (حسب التصميم)"
3. **Technical Specs + Material Datasheets = ONE section** — never split them
4. **Cement Board 12mm** is the rigid substrate/cladding; PVC Flex banner mounts ON the cement board surface
5. **Gates break continuity** — vehicle gate (6m×8m) and pedestrian gate (1.2m×2.1m) are not clad; LED count deducts for gate openings
6. **Column spacing** — defaults to 3m unless specified; columns = (fence length − gate width) / spacing + 1

### Compliance Matrix Rules
7. **Never reference self-created documents** — Samaya authors the SOW (Scope of Work) and ER (Employer's Requirements) internally. Do NOT reference these documents in the compliance matrix or anywhere in the proposal. Only reference external standards (ISO, SASO, SBC, NFPA, ASTM, ICOM, etc.).
8. **Compliance matrix column** — replace "المرجع (ER/SOW)" with "القسم المرجعي" pointing to the proposal's own section numbers (e.g., ق.10, ق.14, ق.18). The requirement column should reference a standard, not an internal document.
9. **Compliance matrix intro** — do NOT say "تستجيب بنداً بنداً لمتطلبات كراسة الشروط (ER) ونطاق العمل (SOW)". Instead say "تستعرض قدرات الشركة ومنهجياتها المقترحة لكل مجال من مجالات العمل" or similar, focusing on the proposal's own content.

### Site Visit / Field Observation Sections
10. **Do NOT name individuals** — never include personal names like "سلطان عيسى (المدير الفني)" or "مهندس محمد عيسى". Use generic titles: "مدير فني (Technical Manager)" or "فريق سمايا الفني".
11. **Do NOT include photo quantities** — avoid "التقاط 12 صورة" or detailed photo counts per location. Keep as "توثيق الملاحظات الميدانية التي شملت المداخل والواجهات".
12. **Do NOT include photographic registers** — remove the entire "سجل الصور الفوتوغرافية" subsection with its photo-by-photo breakdown. Not appropriate for a formal proposal.

### Table of Contents (TOC) Design
13. **Use diverse icons** — each section type should have its own icon. Do NOT repeat the same icon (▶ or ◆) for every entry. Use at least 20 unique symbols across 35+ entries.
14. **Monochrome palette** — all icons should use the same color scheme (gray background `#e2e8f0`, text `#475569`). Do NOT use different colors per part. The part badge uses Navy `#0F172A`.
15. **Categories** — Project Introduction, Technical Scope, Execution Plan, Understanding & Capabilities, Procurement & Execution, Testing & Handover, Compliance
16. **Clickable `href="#page-N"` anchors** — preserve `text-decoration:none;color:inherit`

### Cover Page Design
17. **Cover logos = no background** — the `.cover-party-icon` container MUST NOT have a background color (remove `background:rgba(255,255,255,0.15)` or similar). Set `background:transparent`.
18. **Invert for dark covers** — use `filter:brightness(0) invert(1)` on all logo images inside `.cover-party-icon` to make them white-on-transparent against the navy (or any dark) cover background. This works for both SVG and PNG images.
19. **Never use CSS custom properties with url() for cover photos** — set `background-image` directly via inline `style` on the target element. CSS custom properties with `url()` resolve relative to the CSS file, not the HTML file, and break in some rendering contexts.

### Design Status Claims (VERIFY Before Writing)
20. **Always verify design delivery status against project files** — before stating what RIBA stage a designer (BMA, etc.) has delivered, read the actual project documents and check:
    - File dates (are they Dec 2025? Mar 2026?)
    - File names (do they say "Concept Design" or "Detailed Design"?)
    - Content (does the BOQ have Stage 4 detail like manufacturer model numbers, or Stage 3 concept-level specifications?)
21. **Delegate document analysis to Kimi/Codex** — these agents can read PDFs, Excel files, and CAD metadata in bulk. Give them the file paths and ask specific questions (dates, stage, systems covered, gaps). Do NOT rely on assumptions from filenames alone.
22. **Document the gap** — if MEP/ELV systems are NOT in the designer's scope, state that clearly. BMA delivered Detailed Design (Stage 4) for architecture/interiors/AV/lighting/scenography in Dec 2025. MEP/ELV (22 systems) were NOT in BMA's scope — they require contractor design (provisional sums).

### Formal Document Style
23. **Monochrome palette for icons and charts** — this is a formal technical proposal. Use at most 2 accent colors (Navy `#0F172A` and Sky `#0284C7`). Avoid green `#16A34A`, amber `#F59E0B`, and multiple accent colors in charts. Use gray tones (`#e2e8f0`, `#f1f5f9`, `#64748b`) for backgrounds and borders.
24. **SVG charts** — should use Navy + light gray + white. Avoid colored phase bars. Keep legends monochrome.
25. **Tables** — Navy header row, alternating white/light-gray rows, no stripe colors.

### BMA Design Fact (Verified Dec 2025)
- BMA delivered: Scenographic Design (Dec 2025), Detailed Design CAD (Dec 2025), AV BOQ/Specs/H&P/Cable Schedule (Dec 2025), Lighting Schedules (Nov 2025), Material & Furniture Schedules (Dec 2025)
- Stage: RIBA Stage 4 (Detailed Design) — NOT Stage 3 (Concept)
- NOT in scope: MEP/ELV (22 systems, $549K provisional sum) — contractor to design
- Correct proposal language: "التصميم التفصيلي (RIBA Stage 4 — Detailed Design) مُسلَّم ديسمبر 2025"
- Incorrect: "المرحلة الثالثة (RIBA Stage 3) مكتملة / المرحلة الرابعة (Stage 4) قيد التطوير"

### Page structure best practices
- Pages 1: Cover (client name, location)
- Pages 2: TOC with categories + icons + anchor links
- Pages 3-5: Executive Summary, Scope, Capabilities
- Pages 6-10: Technical Specifications overview table + ALL datasheets (Banner, Cement Board, Jotun Epoxy, LED, Technical Drawings)
- Pages 11+: BOQ, Methodology, Timeline, Company Docs, Payment, Terms, Signature

### Deployment
- **NEVER deploy from OneDrive path** — Surge fails. Copy to `/tmp/surge-full/` first
- **Samaya-factory.com (shared hosting)**: SSH port 65002, user u517606786, host samaya-factory.com
  - Web root: `/home/u517606786/domains/samaya-factory.com/public_html/build/`
  - Upload via SSH pipe (SCP hangs): `cat file.html | ssh -p 65002 -o BatchMode=yes u517606786@samaya-factory.com "cat > /remote/path/file.html"`
  - Always set permissions: `chmod 755` on directories, `chmod 644` on files
- Keep assets in `proposal_assets/` subfolder (fonts.css, logos, reference images)
- `index.html` is the entry point
- After deploy, verify with `curl -sI` and check all assets return 200

### Surge auth
- Credentials: mohamedsultanabbas@gmail.com
- If token expires/invalidated: re-login then deploy from `/tmp`
