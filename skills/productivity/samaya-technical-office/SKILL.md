---
name: samaya-technical-office
category: project-management
description: "Samaya Tech Office / BIM Unit projects — issue tracking, sub creation, scope verification, schedule analysis, and management briefing"
---

# Samaya Technical Office / BIM Unit

## Scope
All Samaya Investment company projects managed by the BIM Technical Office:
- **Aseer Museum** (project 219 on Odoo) — interior architecture + scenography
- **Zamzam Visitor Center** — NWC project
- **Other BIM Unit projects** under Samaya Technical Office

## Samaya Logo — REPLACE NOTHING, USE THE REAL PNG

**CRITICAL — the user will correct you if you create fake SVG logo approximations.**

The official Samaya logo is at:
`_Style-Guides/logos archives/samaya-logo-trans.png`

- This is a bilingual Arabic/English logo (سمايا الاستثمارية + samaya investment)
- The wordmark is LOWERCASE "samaya" with red "a" — NOT uppercase "SAMAYA" with a diamond
- NEVER create inline SVG text approximations (uppercase "SAMAYA", diamond shapes, red letters, etc.)
- For dark backgrounds: use `<img>` tag with `style="filter:brightness(0) invert(1)"` to render as white silhouette
- For light backgrounds: use `<img>` tag with no filter, original colors
- Saved wrong logos in the archives folder must be immediately deleted (`rm -f`) — the user checks this and will correct you
- All party icons (cover bottom), page headers, and any logo display must use the real PNG file
- **Base64 fallback for local file:// CORS:** When the HTML is opened via `file://` protocol and logos don't load (CORS restrictions), embed the Samaya PNG as a `data:image/png;base64,...` data URI. This eliminates all file path and CORS issues. For 44+ page headers, embed ONCE in the `<style>` CSS as a `background-image` on a class to avoid duplicating the 68KB base64 string 44 times. For cover party icons (3 instances), direct base64 `<img>` tags are acceptable.
- **If the user says "wrong logo", act IMMEDIATELY:** Delete the wrong file from archives first, then fix the HTML. Do not ask questions — the user is telling you the exact problem.

Other project logos (official sources):
- RCRC: `https://www.rcrc.gov.sa/wp-content/uploads/2026/06/RCRC-logo-2.svg`
- BMA: `https://www.borismicka.com/images/logo-white.svg`
- These are REAL SVG files — download and embed directly

## Arabic Font — Use Cairo (NOT IBM Plex Sans Arabic)

When creating Arabic HTML documents:
- Primary Arabic font: **Cairo** (with weights 400-900)
- Google Fonts URL: `family=Cairo:wght@400;500;600;700;800;900`
- Chart/fallback font list: `font-family:'Inter','Cairo',sans-serif`
- DO NOT use IBM Plex Sans Arabic — user corrected this explicitly

### Critical: Add Cairo fallback to ALL font stacks

When working with an existing HTML document that uses separate font variables (--font-heading, --font-body, --font-mono), ensure Cairo is added as a fallback to ALL of them:

```
--font-heading: 'Montserrat', 'Cairo', sans-serif;
--font-body:   'Inter', 'Cairo', sans-serif;
--font-mono:   'Menlo', 'Monaco', 'Cairo', monospace;
```

Without this, any element with Arabic text using --font-heading or --font-mono falls back to the system's default Arabic font, causing visible inconsistency. The `--font-arabic` variable alone is not enough — most inline elements on the page use the other variables.

### Chart Design — Delegate to Claude

When a chart/timeline/visual needs to be created or redesigned in an HTML document:
- ALWAYS delegate chart work to Claude (the user explicitly requires this)
- Provide Claude with: exact file path, viewBox dimensions, brand colors, font requirements
- Claude should handle SVG design, text fitting, and visual balance
- After Claude completes, verify structural integrity (div/section balance)
- Verify the replacement didn't leave duplicated old content behind (check for double comments/wrappers)
- **Verify the chart is in the CORRECT section** — check the h2 title of the section the chart landed in. Common failures: AV System Architecture chart appearing in Section 14 (Joinery), Master Programme timeline appearing in Section 14 or 19 (Lighting), DALI/DMX chart appearing in Section 20 (Vitrines). If a chart title says "AV System Architecture" but the h2 says "Joinery & Manufacturing", the chart is in the wrong section.

## Cover/Design QC — Consult Kimi

When the cover page, visual layout, or any design-heavy element needs final review:
- Consult Kimi for QC inspection before finalizing (the user requires this)
- Provide Kimi with the file path and specific lines to review
- Kimi should check: text readability on dark backgrounds, color contrast, layout balance, Saudi tender conventions, print-readiness of font sizes
- Apply ALL Kimi's critical/high-priority findings before presenting to the user
- All text on dark navy backgrounds must pass the arm's-length readability test

## Cover Page Text Readability on Dark Backgrounds

When building cover pages with a dark navy background (`#0F172A`), ALL text must be clearly readable. The following minimum contrast rules apply:

| Element Type | Minimum Color | Weight | Example |
|---|---|---|---|
| Labels (Client, Project, Date, Rev) | `rgba(255,255,255,0.6)` | `font-weight:600` | Labels below the title |
| Data/Values (the actual content) | `#ffffff` | `font-weight:600` | "Royal Commission for Riyadh City" |
| Eyebrow / category (top subtitle) | `#7DD3FC` (bright sky blue) | `font-weight:600` | "عرض فني · TECHNICAL PROPOSAL" |
| English subtitle | `rgba(255,255,255,0.88)` | `font-weight:400` | Exhibition title |
| Contractor line (bottom text) | `#CBD5E1` (light slate) | regular | "المقاول الرئيسي / MAIN CONTRACTOR" |
| Main contractor badge | `#d91e2e` background, `#fff` text | `font-weight:700` | Red pill: "SUBMITTED BY — SAMAYA" |

**NEVER use** `rgba(255,255,255,0.5)` (50% white) for labels on navy — it is not readable at 0.48rem font size. Always go to 0.6 minimum. **NEVER use** `#0284C7` (sky blue) for eyebrow text — it's too close to navy and disappears. Use `#7DD3FC` (bright sky blue) instead. **NEVER use** `#94A3B8` (slate-400) for secondary text on navy — it's too dim. Use `#CBD5E1` (slate-300) minimum.

**Test rule:** If you need to squint to read text on the cover, the contrast is too low. Increase brightness until it's clearly visible from arm's length.

### Cover Page Party Icon Hierarchy

For tender proposal cover pages where Samaya is the main contractor:

| Position | Content | Size/Emphasis |
|----------|---------|--------------|
| **Top** | Client logo only (RCRC) + document ref | Full prominence — no contractor logo at top |
| **Middle** | Red badge: "مقدم من · SUBMITTED BY — SAMAYA INVESTMENT CO. · المقاول الرئيسي" | High visibility, directly below title |
| **Bottom** | Three-party icons: RCRC (0.7 opacity) · BMA (0.7 opacity) · Samaya (central, larger, bordered) | Samaya central, larger, with subtle border/background |

**Do NOT** add the Samaya logo to the top of the cover. The cover is a submission TO the client — the client's logo belongs at the top. Samaya is already represented 3× (red badge, central party icon, bottom text line). Adding a fourth reference at the top would over-brand and break the client-first hierarchy. Industry-standard proposal layouts consistently place the client at top and contractor at bottom.

For the bottom party row: RCRC and BMA rendered at reduced opacity (0.7), Samaya at full opacity with a subtle border card style (`border:1px solid rgba(255,255,255,0.2)` + `background:rgba(255,255,255,0.06)`) to visually anchor the page.

**Party icon container fix:** Remove `background:rgba(255,255,255,0.15)` from `.cover-party-icon` CSS class entirely — the logos should have zero background. Add `.cover-party-icon img{filter:brightness(0) invert(1)}` as a CSS rule so all three logos (RCRC SVG, BMA SVG, Samaya PNG) render white on the navy cover without individual per-image filter attributes. Do NOT use inline `style="background:transparent;width:auto;height:auto"` overrides — they break uniform container sizing.

## Proposal Section Design Patterns

### Proposal Section Design Patterns

See `references/html-proposal-page-separation.md` for the clean rebuild pattern when sections become mixed on shared pages after structural edits. **Updated with part divider footer fix**, continuation detection patterns, and blank-page prevention workflow.

### Formal Document Visual Style (Monochrome Grid)

For bilingual Arabic-English technical proposals submitted via email as A4 PDF:
- **Icons in tables**: Use monochrome only — navy `#0F172A` icons on light gray `#e2e8f0` backgrounds. No part-specific colors (no green, purple, red per-part badges). **NO EMOJIS** — emojis are NEVER acceptable in formal proposal tables. Use diverse geometric/symbol characters (◐▣✉☰✦◎⚜★☷⚍⬡⇄⛏⛓◇▤♢⚡▣⇌⇨◱✓⚠⛞⬠⌂⚙♻☐⍰∷ — these render reliably across fonts). Never use only 1-2 repeating icons across 30+ rows.
- **TOC icons per section type**: Use distinct icons for different categories so the TOC is scannable at a glance. 34+ unique types for a 36-row TOC is achievable.
- **Part/category badges**: All badges use navy `#0F172A` background with white text. Do not use per-part colors (gray, blue, green, red, purple).
- **SVG charts**: Use a restrained palette — navy `#0F172A`, dark gray `#475569`, dark navy `#1E293B`, white, and light gray `#E2E8F0`. Avoid `#16A34A` (green) and `#0284C7` (sky blue) in chart bars — they look informal.
- **Phase bands in Gantt charts**: Use **rectangular bars** (`<rect rx="2">`) NOT trapezoid polygons. Trapezoids reduce text space at the edges and cause overflow.
- **Short labels in narrow bars**: When a phase bar is under 120px viewBox width, use shortened single-word labels (e.g., "المخططات" not "المخططات التنفيذية"). Strip English subtitles from small bars.
- **Legend inside SVG**: Always include the legend as SVG elements inside the `<svg>`, not as HTML after `</svg>`. Prevents duplication when replacing the chart.
- **TOC: current section highlighted**: The current section gets a navy `#0284C7` icon badge and bold text.

### SVG Chart Text Overflow Prevention

General rules for all SVG charts in A4 documents:
- **viewBox height**: Always add 15-30% more height than you think is needed. Tight viewBoxes cause text clipping.
- **Two-line titles**: Split bilingual titles into two separate `<text>` elements (Arabic line + English line). Never use a single line with "·" separator.
- **Rectangular bars over trapezoids**: Use `<rect rx="2">` not `<polygon>` with slanted edges.
- **Single-language labels in narrow bars**: Under 120px viewBox width, use Arabic-only labels. Remove English subtitles.
- **Milestone diamonds → dashed vertical lines**: Replace diamond markers with full-height dashed vertical lines. Cleaner.
- **Legend inside SVG**: Embed the legend as SVG elements, not HTML after `</svg>`.
- **Font-size floor**: 7px for Arabic labels, 5.5px for English subtitles, 5px for legend text (at 840px viewBox width).
- **Remove redundant axis labels**: Drop week markers (W1, W13, etc.) from Gantt charts — month axis + English month codes (M1-M12) are sufficient.

### BMA Design Stage — Verify Before Writing

The BMA design stage varies by project. **Always verify the actual design status from project documents before writing.** Do not assume a standard stage.

- **Aseer Museum**: BMA completed Scenographic Design (RIBA Stage 3). Samaya's role: develop concept to IFC.
- **RCRC Exhibition (verified Dec 2025)**: BMA delivered **Detailed Design (RIBA Stage 4)** including scenography, CAD, AV BOQ/Specs/H&P, lighting schedules, material/furniture schedules, interior design. **MEP/ELV is outside BMA scope** — 22 systems (power, fire, security, IT, BMS) at USD 549K provisional sum need contractor design.
- **Key documents to check**: Look for filenames containing "DETAILED DESIGN", "SCENOGRAPHIC DESIGN", AV Excel files, lighting Excel files in the project directory.
- **Gap to flag in proposals**: When BMA design covers architecture/interiors/AV/lighting but NOT MEP/ELV, explicitly state: "مع فجوة تصميمية في أنظمة MEP/ELV (22 نظاماً) تقع على عاتق المقاول"
- **Correct proposal wording**: "التصميم التفصيلي (RIBA Stage 4 — Detailed Design) مُسلَّم [month year]" — NOT "قيد التطوير" or "المرحلة الثالثة" (Stage 3).

### Compliance Matrix — No ER/SOW References, Use Standards

When building or updating a Compliance Matrix (Section 34+) in a Samaya proposal:

- **NEVER reference Employer's Requirements (ER) or Scope of Work (SOW) documents.** Samaya authored the SOW and never received the ER — referencing documents we wrote ourselves as external requirements is circular and invalid.
- **Remove the ER/SOW column** from the compliance matrix table. Replace with either:
  - **Standards references** (preferred): Map each requirement to a relevant standard (SBC, ISO, NFPA, ASTM, SASO, ICOM, DALI/DMX, AWS, etc.) and label the column **المعيار**. This shows compliance against external benchmarks, not self-authored documents.
  - **Internal section references** (fallback): Point to internal proposal sections (ق.10, ق.14, etc.) with label **القسم المرجعي**.
- **Replace ER clause codes** (ER-1.1, ER-2.2, etc.) with the mapped standard code (e.g., "ISO 9001", "SBC 301 / AISC", "ICOM / ASTM E2018"). See `references/er-to-standards-mapping.md` for the full mapping used in the RCRC Exhibition proposal.
- **Section title**: "Compliance Matrix (clause-by-clause)" — NOT "vs ER and SOW."
- **Intro paragraph**: Describe the matrix as showcasing capabilities against standards, not as a response to ER/SOW. Say "تستعرض قدرات الشركة ومنهجياتها وفقاً للمعايير والمواصفات القياسية المعتمدة (SBC, NFPA, ASTM, ISO, SASO, ICOM)" not "تستجيب بنداً بنداً لمتطلبات كراسة الشروط (ER)."
- **Appendices reference**: Use "جميع بنود المصفوفة" or "جميع بنود المتطلبات مع المعايير القياسية" not "جميع بنود ER وSOW."
- **Pitfall — subagent rewriting can reintroduce ER/SOW or delete sections**: When a subagent (Claude, Kimi) rewrites a section (e.g., Section 36 Appendices or Section 8 cards), they may (a) reintroduce ER/SOW text that was already fixed, or (b) delete entire sections 9-36 beyond their scope. After any subagent modification, ALWAYS verify: (a) section count matches pre-delegation, (b) Section 34 has zero ER/SOW references (grep for 'ER-'), (c) pages 9+ are still present in Part 02. If sections are missing, restore from .bak and re-apply targeted fixes directly (not delegation).
- **Pitfall — base64 image bloating when sub-agent creates new pages**: When a sub-agent creates new page(s) for a section (e.g., expanding Section 8 from 1 to 3 pages), they should reuse the existing CSS class for the header logo (`<div class="samaya-header-logo"></div>`) — NOT embed a new base64 data URI. Each new base64 embed adds ~68KB. After sub-agent expansion, search for `data:image/png;base64` and count occurrences — should be 1 (in CSS) + up to 3 (cover party icons). More than that means the sub-agent embedded the logo in each new page. Fix: replace inline `<img src="data:image/png;base64,...">` with `<div class="samaya-header-logo"></div>`.

### Site Visit Section — No Personal Names, No Photo Specifics

When documenting a site visit (Section 33):

- **Do NOT name individuals** in the visit team strip or paragraph. Use "مدير فني (Technical Manager) + فريق فني مساعد" — not "سلطان عيسى (المدير الفني)."
- **Do NOT give specific photo counts** (e.g., "التقاط 12 صورة تغطي المداخل (6 صور)..."). Instead, say generically: "الملاحظات الميدانية الرئيسية التي شملت المداخل والواجهات."
- **Do NOT include a Photographic Record table** (33.1). Photographs are for internal use only — not a proposal deliverable.
- **Renumber** remaining subsections after removing 33.1 (33.2→33.1, etc.).

### CSS Rendering as Visible Page Text — Diagnosis & Fix

**Diagnostic checklist (in order):**
1. **Count `<style>` vs `</style>` tags.** Mismatch = orphan tag causing the browser to render CSS as raw text. Use `h.count('<style')` vs `h.count('</style>')`.
2. **Check for `</style>` wrapped inside HTML comments** (`<!-- </style> -->`). The `</style>` inside a comment is invisible to the parser — the previous `<style>` never closes, and everything after it until the next `</style>` (or end of file) is treated as CSS text content.
3. **Check for extra `</style>` after `<body>` open.** An orphan `</style>` at line 189 with no matching `<style>` open creates a phantom close — harmless but indicates structural debris from prior edits.
4. **Check for CSS code sitting in `<body>` without `<style>` wrapping.** Look for CSS rules starting with `.some-class` directly inside the body (no `<style>` tag before them). This happens when a file has two copies of the document (Part 01 + Part 02) and the second copy's CSS was never wrapped in `<style>` tags.
5. **Check `<head>`/`</head>`/`<body>` tag counts.** Each should appear exactly once. Duplicate `</head><body>` blocks cause nested <head> issues.

**Fixes:**
- Uncomment `</style></head><body>` if wrapped in `<!-- -->`. Remove the comment markers.
- Wrap orphan CSS blocks (between end of Part 01 and start of Part 02) in `<style>`...`</style>` tags.
- Remove duplicate `</head><body>` blocks that appear mid-file.
- Remove orphan `</style>` tags that have no matching `<style>` open.

**Verification:**
```
<style> opens: N
</style> closes: N  ✅
<head>: 1, </head>: 1
<body>: 1, </body>: 1
```

### Patching Duplicated Content (Part 01 + Part 02 Pattern)

When a file has two complete copies of the document (e.g., Parts 01 and 02 of a multi-volume proposal), the SAME text block appears twice. Simple `patch(mode='replace')` fails with "Found 2 matches."

**Strategy:**
1. **Use `replace_all=False` (default)** and include ENOUGH surrounding context to make the match unique. Look for unique page numbers ("صفحة 4 / 46" vs the Part 02 copy's different page number), or unique surrounding content.
2. **If both copies are identical** (same page number, same content), use `execute_code` with sequential matching:
   ```python
   first = h.find('target text')
   h = h[:first] + new_text + h[first+len(old):]
   # Then find and replace the second occurrence
   second = h.find('target text', first + len(new_text))
   ```
3. **Never use `replace_all=True`** on duplicated content unless you INTENTIONALLY want to update both copies identically.
4. **After any patch, always verify**: Div/section balance, no orphan tags, head/body/style structure intact.

### Print Readability Minimums

### Section 8 — Experience Cards: Use Real Website Photos

When designing the "Relevant Experience" (Section 8) project cards:
- **Use real photos from the company's official website** (samayainvest.com/our-work/), NOT AI-generated descriptions or text-only cards.
- Each card = image thumbnail (80px height, `object-fit:cover`) + project name + year badge + one-line description.
- Image URLs are available from the website's `wp-content/uploads/` directory (960x720px cropped versions).
- For current projects not yet on the website (e.g., Aseer Museum), use a dark gradient placeholder with the project name watermark.
- Structure cards in a 2-column grid grouped by category (Museums · Exhibitions · Permanent Installations).
- Always cross-reference every project against the website. Replace unverifiable "Private" client projects with actual website-listed projects.
- Add a photo credit footer: "جميع الصور من مشاريع سمايا المنشورة على الموقع الرسمي samayainvest.com"
- See `references/proposal-website-verification.md` for the full verification workflow.

**Table-matrix format (alternative for formal tenders):** When the evaluator is a Saudi government RFP committee that scores "relevant experience" heavily, replace the card grid with a 6-column table-matrix (Project · Client · Year/Value · Scope · Deliverables · Relevance to RCRC). This format enables rapid evaluator scanning, explicitly maps each project to RFP requirements, and fits 13 projects in 2 pages. Key columns: Contract Value (SAR), Client Entity (name the government body), and "Relevance to RCRC" (explicit mapping statement per project). Include a KPI summary dashboard bar at top (total projects, total value, years of experience). See `references/proposal-website-verification.md` for the full workflow.

### Team CV Section: Use Real KPR Data, Present for Current Project

When building the "Proposed Team (continued)" CV summary page:
- **Always use real names from the Key Personnel Register (KPR).** Never fabricate generic Arabic names like "أحمد السعيد" or "خالد العتيبي."
- Include: name, role, and a one-line summary of relevant experience.
- For specialist firms not yet formally approved for the project, add a qualifying footnote saying they've been approached and expressed readiness, with formal contracting post-award.
- **Frame the team as selected for THIS project** (e.g., "يضم فريق العمل المقترح نخبة من الكوادر المتخصصة التي تم اختيارها بعناية لهذا المشروع"). Do NOT say "this is the Aseer team" — the user explicitly rejected this framing.
- List 12-15 key personnel covering: management (PD, PM, BIM, HSSE), specialists (structural, MEP, lighting, AV, showcases, interactive, FLS, IT), and internal support (factory, graphics, document control).

### CSS Rendering as Visible Page Text — Diagnosis & Fix

When a browser shows CSS code as visible text instead of applying styles, this is nearly always an HTML structure issue.

**Diagnostic checklist (in order):**
1. **Count `<style>` vs `</style>` tags.** Mismatch = orphan tag. Use `h.count('<style')` vs `h.count('</style>')`.
2. **Check for `</style>` wrapped inside HTML comments** (`<!-- </style> -->`). The closing tag inside a comment is invisible — the previous `<style>` never closes, everything after it renders as text.
3. **Check for extra `</style>` after `<body>` open.** An orphan `</style>` with no matching `<style>` open is structural debris from prior edits.
4. **Check for CSS code sitting in `<body>` without `<style>` wrapping.** Look for CSS rules starting with `.class` directly in the body. This happens when a file has two copies of the document (Part 01 + Part 02) and the second copy's CSS was never wrapped in `<style>` tags.
5. **Check `<head>`/`</head>`/`<body>` tag counts.** Each appears exactly once. Duplicate `</head><body>` blocks cause nested head issues.

**Fixes:**
- Uncomment `</style></head><body>` if wrapped in `<!-- -->`
- Wrap orphan CSS blocks in `<style>`...`</style>` tags
- Remove duplicate `</head><body>` blocks that appear mid-file
- Remove orphan `</style>` tags with no matching `<style>` open

**Verification:** `<style>` opens = closes, `<head>` = 1, `<body>` = 1.

### Patching Duplicated Content (Part 01 + Part 02 Pattern)

When a file has two complete copies of the document (e.g., Parts 01 and 02 of a multi-volume proposal), the SAME text block appears twice. Simple `patch` fails with "Found 2 matches."

**Strategy:**
1. Use `replace_all=False` (default) and include ENOUGH surrounding context to make the match unique. Look for unique page numbers or surrounding content.
2. If both copies are identical, use `execute_code` with sequential matching: `first = h.find('target')`, patch first, then `second = h.find('target', first + len(new))`, patch second.
3. **Never use `replace_all=True`** on duplicated content unless you INTENTIONALLY want to update both copies identically.
4. After any patch, verify: div/section balance unchanged, no orphan tags, head/body structure intact.

### Page Renumbering for Two-Part Documents (Part 01 + Part 02)

When expanding a section in Part 02 (the second copy) that adds pages, ALL subsequent Part 02 page references must shift while Part 01 page numbers stay unchanged.

**Critical workflow:**
1. **Find Part 02 boundary** — locate the second `<section class="page page-cover">` in the file. This is where Part 02 begins.
2. **Split the file** — `part01 = h[:second_cover]` and `part02 = h[second_cover:]`. This guarantees Part 01 references are completely isolated from Part 02.
3. **Renumber Part 02 going BACKWARDS** — iterate from the highest page number down to prevent double-replacement:
   ```python
   for old_pg in range(46, 8, -1):  # backwards from last page to first shifted page
       new_pg = old_pg + N
       part02 = part02.replace(f'صفحة {old_pg} / 46', f'صفحة {new_pg} / {46+N}')
   ```
4. **Update the first expanded page** — e.g., change `صفحة 8 / 46` to `صفحة 8 / {46+N}` (the page number stays 8 but the denominator changes).
5. **Join back**: `h = part01 + part02`
6. **Verify**: Count all page refs, check sequence is monotonic, Part 01 pages unchanged, no gaps or overlaps.

**Common failure modes:**
- Going forward (e.g., `for pg in range(9, 47)`) causes cascade: `9/46→11/46`, then `10/46→12/46`, but the original `10/46` that should shift by +2 becomes `10/46→12/46` while the already-shifted `11/46` (originally 9) stays. Always go backwards.
- Global replace on unsplit file shifts Part 01 page numbers too. Always split first.
- Page references also appear in TOC `<td class="mono">XX</td>`. The split-file approach handles them naturally since they're in Part 02 text.

### Backup Before Sub-Agent Delegation

**CRITICAL — always create a backup before delegating to a sub-agent that will modify an HTML file.** Sub-agents (Claude, Kimi, Codex) can and WILL delete sections, overwrite content outside their scope, introduce duplicate base64 logos, and break page numbering.

**Workflow:**
```bash
cp "$FILE" "$FILE.bak"
```
Then delegate. After delegate returns, compare section count vs backup:
```python
import re
with open(file) as f: new = f.read()
with open(file + '.bak') as f: bak = f.read()
print(f"Before: {len(re.findall('<section', bak))} sections")
print(f"After: {len(re.findall('<section', new))} sections")
```

**Post-delegation verification checklist (run ALL):**
1. **Section count** — unchanged unless growth expected
2. **Div balance** — `<div>` opens == closes
3. **Page sequence** — monotonic, no gaps or jumps
4. **No ER/SOW text reintroduced** — `grep for 'ER-'` should return 0
5. **TOC page numbers** — still reference correct pages
6. **Head/body/style structure** — one `<head>`, one `<body>`, `<style>` opens == closes
7. **Base64 logo proliferation** — count `data:image/png;base64` occurrences. Expect 1 (CSS class) + up to 3 (cover party icons). More means the sub-agent embedded the 68KB logo in each new page instead of reusing the CSS class. Fix: replace inline `<img src="data:image/png;base64,...">` with `<div class="samaya-header-logo"></div>`.
8. **Subsequent sections not overwritten** — if sub-agent was told to modify Section 8, verify sections 9-36 still exist and have not been replaced.

**Recovery from destructive sub-agent edit:**
```bash
cp "$FILE.bak" "$FILE"    # restore immediately
# Then re-apply only targeted fixes directly (not via delegation):
# - find-replace on ER/SOW text
# - remove names, photo counts
# - patch specific sections with minimal changes
# Each fix applied via execute_code or patch, not delegation
```

**Sub-agent scope control:**
- Explicitly tell the sub-agent: "ONLY modify Section X. Do NOT modify any other section, page number, footer, TOC, or introduce new base64 images."
- After sub-agent returns, ALWAYS run the full verification checklist above.
- **Pitfall — expanding Section 8 to 3 pages destroys subsequent sections:** The most common sub-agent failure is deleting Part 02 sections 9-36 while building new pages for Section 8. Always restore from .bak instead of trying to fix in-place.

**Recovery from sub-agent corruption when .bak is stale:** If the .bak file was created after the sub-agent already corrupted the file (e.g., .bak was overwritten by a subsequent save), restore from the **git commit history** instead. Use `cd /tmp/<repo-name> && git checkout <commit-hash> -- <file>` to pull a clean version from before the corruption. Then re-apply only targeted fixes directly (not via delegation). This is faster than rebuilding the corrupted sections.

### Part Divider Pages — Make Visible, Not Blank

When a proposal has four part dividers (الجزء الثاني/الثالث/الرابع/الخامس), each gets its own `<section class="page">`. These pages contain only an h2 and look **blank/white**, causing users to think the document is broken or content is lost.

**Fix (additive only, never touch section tags):**
1. Add a **centered dark banner** before the h2: `<div style="display:flex;align-items:center;justify-content:center;min-height:200mm"><div style="text-align:center;background:var(--primary);color:#fff;padding:30px 60px;border-radius:8px">`
2. Close the wrapper divs after `</h2>`: `</div></div>`
3. Add a **footer** before `</section>` so the page doesn't look abandoned
4. **NEVER** delete the section tags or merge with adjacent sections — the structural edit risk always outweighs the cosmetic gain

### Blank Section Removal (Safe Method)

When extra blank sections appear (no h2, under 500 chars, caused by prior structural edits), remove them **back-to-front** to preserve byte positions:

```python
sections = list(re.finditer(r'<section class="page"[^>]*>', h))
to_remove = []
for i, s in enumerate(sections):
    start = s.start()
    end = sections[i+1].start() if i+1 < len(sections) else len(h)
    sec = h[start:end]
    if '<h2>' not in sec and len(sec) < 500:
        to_remove.append((start, end))
for pos, end in reversed(to_remove):  # back-to-front
    h = h[:pos] + h[end:]
```

**Never** iterate forward while removing — positions shift and wrong sections get deleted.

### "Ultra Think" Mode — Minimal Additive Changes

When the user says "ultra think" or has rejected multiple structural edits: **stop all tag manipulation.** Only make additive changes (CSS rules, content inside existing tags, styling attributes). Never touch `<section>`, `</section>`, or h2 boundaries. Never use regex find-replace on structural tags. The document is fragile — each structural edit cascades into new breakage.

### Print Readability Minimums

For any HTML document intended for A4 print:
- Minimum font size for body text: **0.44rem (≈7pt)** — anything smaller risks being illegible in print
- Party labels and metadata: **0.44rem minimum**
- Table cell text: **0.42rem minimum**
- SVG chart labels: **5.5px minimum** in SVG units (at 840px viewbox width)
- Green `#16A34A` on navy `#0F172A` for small text (<7pt) is unacceptable — use white-toned `rgba(255,255,255,0.85)` instead
- 50% white opacity (`rgba(255,255,255,0.5)`) on dark backgrounds is too dim for labels — use 78% minimum
- Saudi evaluation committees read printed copies under office lighting — anything below 7pt blurs

### Delegation Pattern: Kimi for QC, Claude for Charts

When redesigning any section of a proposal HTML:
1. **Charts/visuals → Claude.** Delegate SVG design to Claude with exact viewBox, colors, font requirements. Claude handles text fitting, visual balance, and styling.
2. **QC review → Kimi.** Before finalizing any redesigned section, consult Kimi for: text readability, color contrast, layout balance, Saudi tender conventions, print-readiness. Apply ALL critical/high-priority findings.
3. **After delegation, verify:** (a) structural integrity (div/section balance), (b) no duplicated old content left behind from partial replacement, (c) renamed/moved sections still have correct page numbers in TOC and footers.

## Core Principles

### 1. Project Separation Is Strict
- Aseer/Samaya ≠ Moqtana/Tqanny/Sada_Uhud
- Never cross-reference projects across entities
- Each project has its own submittal codes, registers, and correspondence

### 2. Execute Without Asking
- Contract baseline comes first, reality second
- Cross-check activities vs SOW/ER before adding work
- Update registers without asking
- Never ask permission for routine actions

### 3. Decision Style
- **Do NOT offer multiple-choice prompts.** Let the user say what they want to do.
- Present the situation clearly, then ask open-endedly "what do you want to do?"
- Exception: when the user explicitly needs options to choose from (e.g., procurement decisions), present a concise comparison table without asking "which one?"
- "Never ask permission" means: for routine updates (registers, Odoo, filing), just execute and report.
- **Always rewrite user prompts** into structured task specs before executing. Restate, clarify, and format the task. The user explicitly requires this for all work.

### 4. Output Standards
- English-only in ALL communication with the user. Never use Arabic unless the user explicitly asks for Arabic output. The user corrected this and requires strict English-only — this applies to conversation, explanations, summaries, and all responses.
- Formal letters as DOCX with Samaya branding (red accent, bilingual RTL) — use `samaya-docx-template` skill
- Excel: formulas, number formatting (never "SAR" text), navy/white/yellow palette, openpyxl
- Tables and bullets over paragraphs
- RTL Arabic content requires careful formatting
- **NO icons, emoji, or AI fingerprints in ANY generated document** — including submittal registers, plans, dashboards, or any deliverable. Not in headers, stage markers, status indicators, remarks columns, or Legend sheets. Use plain text only. Check ALL scripts in `_scripts/` for icon/emoji Unicode ranges (0x25A0-0x25FF, 0x2700-0x27BF, 0x2600-0x26FF, 0x1F000-0x1FFFF, 0x2500-0x257F, 0x2580-0x259F). Replace with ASCII equivalents (= for box-drawing, - for dashes, [OK] for checkmarks, BLOCKED for hourglasses, ## for block chars). Run compile() on all .py after cleanup.
- **Email drafts for forwarding review comments:**
  - Informal/collaborative tone for "review only" — not formal approval language
  - **Always draft from beginning** — write the complete email in one pass, not patch-style updates
  - Group comments by reference with "What's needed" action items
  - Include priority table (P0/P1/P2) with "Who" column
  - Emphasise ISO naming convention as a separate section

## Workflows

### Sister Companies Costing Reconciliation
Full methodology for classifying, grouping, reallocating, and finalizing costs across Samaya's stores, coffee shops, and visitor center projects. See `references/sister-companies-costing-methodology.md` for complete 10-step workflow. Also load the standalone `sister-companies-costing` skill for formula-based Excel building with openpyxl.

Key rules:
- **Stores and cafes only** — never mix museum/exhibition data (02 Holy Quran Museum, 07 Khair Al-Khalq Museum) with store data
- **Project by project** — work one project at a time from original to final
- **Rewrite prompts** — always restructure user directives into a formatted task spec before executing. The user explicitly requires this for all work.
- **One reference document** — each project gets a single comprehensive `_Final/{Code}_{Name}.xlsx` with all classifications, reallocations, and item types in numbered sections
- **Full original descriptions** — when moving items between projects, always retain the complete original Arabic description AND invoice/document number; never use summaries
- Equipment and operations items separate from construction costs
- Supervision 10% applied on FULL total (accounting + factory), not factory alone
- All totals formula-based, never hardcoded
- openpyxl: unmerge cells before clearing ranges; writing to MergedCell raises AttributeError
- **openpyxl `insert_rows()` is forbidden in formula-based sheets** — it silently corrupts cell references. Always rebuild clean from scratch instead of inserting.
- **Close before write**: always load → modify → save → close. Never modify a workbook that might have a stale open handle. If you get `AttributeError: 'MergedCell'`, you wrote to a merged cell — unmerge the range first.
- **Set `ws.sheet_view.rightToLeft = True` for Arabic sheets** — must be set on every new Arabic-language sheet.
- **Shared accounting statements**: When one Ibrahim statement covers multiple projects (e.g., Qahwatna+Hira), split by area percentage. Note the split ratio in the file header and section intro.
- **Target value fitting**: User provides budget targets. Distribute factory costs across Labor/Materials/Others to reach the exact target. Formula: `factory_needed = (target/1.1) - accounting`. Adjust `Others` line to fine-tune.
- **CRITICAL — Column header pattern**: NEVER put `r += 1` inside a `for ci, h in enumerate(headers)` loop. This scatters each column header onto a separate row. Use a `hdr(ws, r, cols)` helper function that writes all headers on row `r`, then increment r ONCE after the call. See `references/sister-companies-excel-pattern.md` for the exact code. User will reject files with scattered headers.
- **CRITICAL — No empty rows between headers and data**: After column headers, the next row is the first data row. No blank separator rows.
- **CRITICAL — `delete_rows()` breaks formulas**: Never use `ws.delete_rows()` on formula-based sheets — it silently corrupts cell references. Always rebuild clean from scratch.
- **CRITICAL — No duplicate items across projects**: Equipment items appearing in one project's construction or equipment tab must NOT be repeated in another project. Each item# exists at exactly one location (either full amount in one project, or split by area across exactly the shared set). See `references/sister-companies-excel-pattern.md` pitfall #8.
- **CRITICAL — Target mid-session changes**: When the user changes a project's target value, rebuild the file from scratch. Never patch factory values into cells identified by matching generic row content (\"1\"/\"2\"/\"3\") — they collide with accounting items and corrupt data.
- **CRITICAL — Area-split for shared museum+store projects**: When a store is physically inside a museum building (e.g., Khair Al-Khalq store inside 1,325 m² museum), items mentioning both \"معرض ومتجر\" (exhibit+store) are shared and must be split by area percentage. Items mentioning only \"متجر\" (store) stay at 100%. Add a merged note row below accounting total explaining the split with formula `SHARE = store_area / (store_area + museum_area)`.
- **CRITICAL — Source sheet precedence**: When reading `.xls`/`.xlsx` source files from Ibrahim, check ALL sheets. Sheet2 may contain filtered/extracted store-specific items while Sheet1 has the full museum+store list. The user knows which sheet to use — confirm before building.
- **Source files**: Always read data from the original Ibrahim email files (`.xlsx`, `.xls`, or PDF), not from previously restructured copies. User may delete intermediate files.
- **Section find must be scoped**: When searching for rows to update (e.g., factory values), never match generic values like "1"/"2"/"3" in column A globally — they collide with accounting items. Match against section context or use relative row finding from section headers.
- **Compact sections**: Sections with "لا توجد" (none) = ONE row only. No separate column headers. No blank rows between header and data.
- **"مهمل" forbidden**: Never write "مهمل" — use "محول من (source project code)" for transferred items.

### RACI-Driven Scope Realignment (CG Comment #4)

When CG returns a submittal with Code C and Comment #4 requiring a RACI matrix, use the dedicated workflow at `subcontractor-folder-setup/references/raci-scope-realignment-workflow.md`. Key principles:

- **Read the RACI first** — extract all R/A/C/I assignments per party before touching any scope document
- **Work per-party** — AD, ZNA, BMS/ICT, Namaa each get their own update pass
- **Remove, narrow, add** — three operations per sub: remove items that moved to other subs, narrow items where role changed, add new RACI-mandated items
- **ZNA gets a review document** (not a full rewrite) since they have a signed contract
- **BMS/ICT and Namaa get new scope documents** since they had none
- **Bump version** on updated scope documents (R01→R02) with RACI alignment note

### CG Response Triage & Coordination Workflow

See `references/cg-response-triage-workflow.md` for the full workflow: receive CG response → extract comments → verify against schedule data → coordinate with NRS → update Odoo/register/memory → draft formal response. Includes a worked example from the Arch Viz Package 01 submittal (C status, FI_ME_01 brass spec dispute, G7/G10/G13 scope exclusion).

### Scope Clarification Response (NRS vs SAMAYA)
When CG/PMC/NRS requests a breakdown of which specialist positions are covered by NRS vs SAMAYA (per SOW §5.5), follow `references/scope-clarification-response-pattern.md`. Workflow: cross-reference SMP Tier IDs + NRS Appendex A + subcontractor register → produce two-table reply with SMP refs.

### NRS Email Triage
See `references/nrs-email-triage-workflow.md` for reading NRS replies and triaging into: action items (✅ adopt), clarifications (✅ close), and risks (⚠️ record in Design Risk Register).
When the user references a previously identified problem and says "let's go back to it":

1. **Recall context** — use `session_search` to find the original discussion, status, and any recorded decisions
2. **Trace the evidence chain** — follow the issue through:
   - Email archive (e.g., `24.md` in `~/Documents/04_Outlook_Connection/mails/`)
   - PROJECT_MEMORY.md for current status
   - Filed deliverables (XER/XML/PDF schedules, submittals, correspondence)
3. **Cross-reference contractual constraints** — check SOW, ER, specifications, CG directives, approved DMP
4. **Determine current status** — is it open, resolved, escalated, awaiting direction?
5. **Present the situation** — structured summary with:
   - What happened and when
   - Current status
   - What's at stake (schedule, cost, compliance, relationship)
   - Open-ended question about next steps (not multiple choices)

### Quantity Surveying Baseline (7-Register Methodology)
When building a scope baseline and quantity register for a tender/pricing study from design documents, BoQ, RFQ drafts, and site reports — follow the full 7-register methodology: Document Register → Discrepancy Log → WBS (GROUP-ZONE-PACKAGE-SEQ) → Quantity Register → Open Items → Risk Register → RFI Register. See `references/qs-baseline-methodology.md` for the complete workflow with guardrails, classification codes, and cross-comparison checklist.

### Proposal Experience Verification
When Section 8 (Relevant Experience) of a proposal lists projects, cross-reference every claimed project against the company's official website (samayainvest.com) to verify credibility. Flag projects that don't appear on the website and recommend adding verifiable portfolio projects that are missing. See `references/proposal-website-verification.md` for the full workflow and Samaya's known portfolio.
### Design Schedule Constraint Compliance

When analyzing whether a design schedule meets consultant constraints:

1. **Identify the constraint** — e.g., CG 3-month design phase, specific milestone dates
2. **Collect schedule data** — XER, XML, critical path PDF from Planning Engineer
3. **Verify the finding** — confirm duration estimation methodology was sound (not just one person's opinion)
4. **Document the gap** — actual required duration vs constraint
5. **Determine escalation need** — does management direction or CG relaxation need to be requested?
6. **File all schedule artifacts** — XER, XML, critical PDF to `Design Files/00_Scope_and_Proposals/`

### CG Submission Schedule Planning (4-Category Method)

When CG (e.g., Mohammad Elbaz) requests a design phase schedule, they specify **4 categories** that must all be submitted AND approved within the deadline: DD Drawings, Material Submittals, IFC Drawings, and Coordination Drawings.

Key rules: Basement-first priority, staggered submissions (min 5 WD gap), review buffers based on complexity (Simple=7WD, Medium=14WD, Complex=14-21WD), and IFC depends on DD approval (not just submission).

See `references/cg-submission-schedule-methodology.md` for the full methodology with buffer rules, dependency chain, scheduling algorithm, and mitigation patterns when the deadline can't be met.

### Primavera P6 Schedule Audit (Progressive Deep-Dive)
When the Technical Office receives a contractor Primavera P6 schedule for review, use the progressive pass method:
1. **Pass 1 — Overall health**: structure, duration, unapproved start date, calendar
2. **Pass 2 — Targeted phase**: user directs focus (design, procurement, construction, handover)
3. **Pass 3 — Package details**: list items, cross-reference BOQ/registers for suppliers

See `references/schedule-audit-workflow.md` for the full workflow: PDF extraction, cross-referencing project data sources (Floor Finishing Detail, Materials Register, Procurement Tracker), output formats (HTML review report, Excel extraction), finding taxonomy, and typical museum fit-out schedule findings.

### Direct Work Requests to Design Consultant (Batch / Progress Instructions)

When requesting new deliverables from a design consultant (e.g., asking NRS to start Batch 2 of 3D visuals):

1. **Keep it short.** One paragraph with the ask and a line of context. No verbose breakdown of every element.
2. **Reference programme dates.** Say "per the programme schedule" or "per our dates" — do NOT ask the consultant what timeline works for them.
3. **Confirm reference material is ready.** Quick note like "stamped Stage 4 drawings on file" so they know they can proceed.
4. **Ask for their proposed start/timeline** — one line at the end.

See `references/direct-work-request-to-designer.md` for template.

### Forwarding CG Review Comments to Design Consultant

When CG returns review comments on a design submittal (DD/IFC) that needs to be relayed to the design consultant (NRS, ZNA, AD Engineering):

1. **Tone is informal/collaborative** — this is "review only," not formal approval. Use "still needs some work" / "what's needed" / "if that works?" not "must comply" / "deadline."
2. **Draft from beginning** — write the complete email in one pass. Do not send patch-style updates or incremental revisions.
3. **Structure** — group comments by CG reference, each with "What's needed" action. Include a priority table (P0/P1/P2 with "Who" column).
4. **Anticipate pushback** — if CG demands coordination data the designer hasn't received (e.g., MEP inputs for RCPs), acknowledge the gap and suggest a fallback (use tender/Stage 3 drawings).
5. **Emphasise ISO naming** — the drawing numbering convention (per DMP/BEP) gets its own section, not buried under title block.
6. **Split unrelated communications into separate emails** — when CG sends both review comments on a submittal AND a separate request (e.g., scenography drawings submission request), send them as distinct emails. First email = review comments on the submittal. Second email = forwarded request with its own context and ask.
7. **Flag Samaya-internal items clearly** — when CG asks for deliverables Samaya will produce in-house (e.g., materials selection presentation for 3D views), state explicitly in the email: "We'll handle this from Samaya's office; no action needed from your team." This prevents the consultant from duplicating work or pricing it.
8. **Pre-empt "already submitted" pushback on forwarded requests** — when forwarding a PMC request for new deliverables, ask the consultant to identify what's already been done vs what's new/outstanding. Phrasing: "review the scope and let us know if there are items that need to be prepared that we haven't already submitted in previous [packages]."
### 9. Finish/material CG disputes: sample first, render once

When CG rejects a specified finish (e.g., "color-coated not accepted, revert to patinated brass"):
- **Do NOT tell NRS to update renders immediately.** First, **search all schedule JSON files** under `data/schedules/*.json` (19+ files) to find the exact finish code and verify if the spec has sufficient detail (product code, RAL, supplier). Don't rely on memory or UI views — search raw data.
- If the spec says "TBC Locally Sourced" or lacks a product reference/RAL/sample, CG cannot demand a specific finish without providing it. The contractor's obligation is to source and submit a matching sample for approval, not to guess at an undefined product.
- **Source and submit a matching sample** for CG approval FIRST. Once the sample is approved, NRS renders once. No double work.
- **Email to NRS says:** "Hold on the [finish] — the spec lists supplier TBC with no RAL/sample. We're sourcing a matching sample and submitting it to CG for approval first. Will advise once approved, then render once. No point doing it twice."
- Do NOT add "check the approved spec and update if needed" — this delegates internal decision-making to the designer. Spec verification is Samaya's internal review, separate from the design direction.
- **Pitfall — don't assume "no match" based on browser/UI views.** The hotspot app table is virtualized; visible rows may not include all finishes. Always search the raw JSON files directly with grep/Python for terms like 'patinated', 'brass', 'bronze', 'copper' across ALL schedule types (finishes, setwork, showcase, graphic, wayfinding, etc.).
10. **Group comments by category for the designer** — Structure the NRS email as two sections: "Accept & action" (valid corrections: tile patterns, annotations, view improvements) and "Our position on other items" (push back: MEP in viz, missing scope items). This helps the designer prioritize and avoids them acting on items you plan to push back on.
11. **Flag Samaya-internal responses explicitly** — When CG asks for something Samaya will handle in-house (e.g., material board via hotspot platform), state clearly in the email: "We'll handle this from Samaya's office; no action needed from your team." This prevents the consultant from duplicating work or pricing it.

See `references/forwarding-cg-review-to-designer.md` for the full workflow and email template.

### Material Sample Submittal Folders

See `references/sample-submittal-system.md`. When creating physical material sample folders (48×23cm landscape cover) with QR codes for client/consultant submittal, load the `sample-submittal-system` skill. Key rules:
- Submittal ref format: `MOC-MUS-ASE-{ZONE}-{TYPE}-{NNNN}` (e.g., MA-0007 for Material Approval)
- Images must be embedded as base64 data URIs in `label.html` (OneDrive + file:// protocol don't support external image loading reliably)
- Template is `TEMPLATE-LABEL-24x33cm.html` (not A5)
- Register includes Project + Submittal Ref + Folder Size columns

### Document/Filing Rules
- Email attachments → classify by project → file under correct BIM subfolder
- Schedule files (XER/XML/PDF) → `Design Files/00_Scope_and_Proposals/`
- Correspondence → `05_Correspondence_Archive/`
- Update PROJECT_MEMORY.md with critical findings
- Log pipeline runs for audit trail
- **Standard logo treatment for cover pages** — When adding project party logos to any document/site, use the official transparent logos from `_Style-Guides/logos archives/`. Follow the Engineering Deck style guide's 5-party logo row format (MoC · PMC · CG · NRS · Samaya).
  - **Light-background pages** (inner pages, white background): Keep original brand colors — no CSS filters. Use `<img>` with no filter.
  - **Dark-background covers** (navy/primary background): Use `filter: brightness(0) invert(1)` so logos render white and are visible against the dark background. This is the correct treatment — the filter converts brand colors to white, which is needed for legibility on navy. Do NOT skip the filter on dark covers (logos disappear) and do NOT apply it on light pages (logos look inverted/negative).
- **CRITICAL — Never create fake/approximate SVG logos**: Always use the actual logo image files from `_Style-Guides/logos archives/`. Never create text-based SVG approximations, diamond+text wordmarks, or any other fabricated logo representation. The user explicitly rejects placeholder/recreated logos. For page headers where space is limited (e.g., 14px height bars), use `<img src="...path.../samaya-logo-trans.png" style="height:14px">` — not an inline SVG wordmark. The official Samaya logo is a bilingual (Arabic/English) PNG at `_Style-Guides/logos archives/samaya-logo-trans.png` (50KB, transparent RGBA). Other official logos: RCRC from rcrc.gov.sa SVG, BMA wordmark from borismicka.com SVG, stored in the same archives folder.
- **Samaya Formal Plan A4 Style Guide** — `~/OneDrive.../Technical Office/_Style-Guides/Samaya-Formal-Plan-A4-Style-Guide.md` is the canonical reference for multi-page formal plans (SMP, DMP, BEP, Resource Mgmt, etc.). Key rules: Montserrat (headings) + Inter (body) + Menlo (metadata) fonts — never Calibri. Colors: `--primary #0F172A`, `--secondary #0284C7`, `--pass #16A34A`, `--fail #B91C1C`, brown `#92400E`. 2px border-radius max. SVG charts: Inter font, → character arrows, white boxes with navy stroke, navy end boxes. See `references/style-guide.md` for the full sub-guide index.

### Workshop Purchasing Tracker

The Samaya Factory workshop purchasing tracker lives at:
`Orders/2026/0000 اداريات/شراء/ورشة المشتريات.xlsx`

- Auto-updated daily at 14:00 from Odoo (all POs for `SAMAYA WORKSHOP` buyer)
- Script: `~/.hermes/scripts/workshop_purchasing_update.py`
- Cron job: `fa074c0eb9dd` (no_agent=True)
- Columns: PO Ref, Vendor, Vendor Reference, Amount, Status, Receipt Status, Billing Status, Date, Notes/تحويل
- The Notes column is for manual entry of payment status based on transfer receipt (`صوره التحويل`) from Ibrahim Shaaban
- See `odoo-task-injection` skill's reference `references/odoo-po-export-cron.md` for the pattern

### Interactive 3D Material Hotspot Presentations
When building a web-based material/object review system on rendered interior/exhibition photos with hotspot markers:
- **See `references/interactive-hotspot-presentation.md`** for the full pattern — data model, hotspot system, PHP sync server for team collaboration, password-protected admin-gated editor, materials CRUD admin panel, Excel extraction from 17+ schedule files, source schedule attribution in tooltips, materials organized by schedule file, category→schedule navigation with 3D hover cards, paginated schedule page with tabs, edge-flip tooltip logic, mousemove throttling, hero page design, deploying to Hostinger, image path fix for subdirectory deployment, persistence with server-sync + localStorage
- Key constraints: percentage coordinates only, password-protected `?admin=1` gated editor, never fabricate data from non-existent Excel columns, edge-flip tooltip positioning, rAF-throttled mouse tracking, fix image paths when deploying to subdirectory, always copy sync.php to dist before deploy
- **Submission reference (subRef) badge**: Add a `subRef?: string` field to the `View` interface and each view entry. Display the full submission filename (e.g., `MOC-ASE-AR-ARC-BF-DDD-VIS001`) as a gold mono badge in the modal sidebar under the view description. This lets users see the official document reference without the hotspot data changing.
- **Image replacement preserving hotspots**: To replace a gallery photo without losing hotspot positions, upload the new image to the **same filename** on the server. The hotspot positions are tied to `view.filename`, not the image content. No code change needed — only add `subRef` if you want the new submission name displayed. See `references/image-replacement-workflow.md`.
- **Gallery counter must be updated**: When adding/removing views or galleries, search for and update the static text `"X annotated 3D views across Y galleries."` in `Gallery.tsx`.
- **Deploy via SSH pipe** (when SCP on port 65002 hangs): `cat file.tar.gz | ssh -p 65002 user@host "cat > /path/file.tar.gz"` followed by `ssh ... "cd target && tar xzf /tmp/file.tar.gz && rm /tmp/file.tar.gz"`. More reliable than SCP on some shared hosts.
- **Incremental deploy (changed files only)**: Build locally, tar only the changed files (`index.html`, new JS/CSS, `sync.php`), upload + extract. No need to redeploy all images/assets every time.
- 🔴 **Critical CSS**: hotspot pins must have `pointer-events: auto` (not `none`) — otherwise click handlers don't fire
- 🔴 **Critical sync**: store `hotspot-data/` OUTSIDE the deploy directory (`__DIR__ . '/../../hotspot-data'`) — otherwise `rm -rf appname` wipes all team hotspots on every deploy
- 🔴 **Critical data safety**: use `[key: string]: any` index signature on Material interface; guard all `.toLowerCase()` calls with null checks — undefined fields crash React render phase silently
- 🔴 **Tooltip pinning**: use `useRef` for pin state (not useCallback closure) to avoid stale event handlers after state updates
- 🔴 **Theme**: light/formal (#F5F1EB bg, #1A1D23 text, #C8A45C gold) for museum client presentations — user rejects dark themes

### Plan Synchronization (SMP-to-Downstream Plan)
When an authoritative stakeholder/org document is revised (SMP, KPR, Master Programme), all downstream plans need role-structure sync. Full workflow at `references/plan-synchronization-workflow.md`.

### Submittal Register Generation — Data Sourcing & Format Rules

When creating or updating a submittal register xlsx:
1. **Data sourcing priority** — Check actual subcontractor data first (24_Subcontractors/{Package}/*), then BOQ/Schedule files, then scope docs. Only fall back to generic templates if none exist.
2. **9-column format** — Ref #, Submittal/Deliverable, Discipline, 50%, 90%, 100%, IFC/AFC, Sub-Package, Remarks. No SOW/ER columns. Widths [7,50,14,14,14,14,14,22,28].
3. **Stage columns hold dates** — Each sheet shows only its own stage's date; others = em-dash. Stagger +7d per category/floor for review buffering.
4. **No icons/emoji anywhere** — Headers, status indicators, remarks, legend — all plain text. Check Unicode ranges 0x25A0-0x25FF, 0x2700-0x27BF, 0x2600-0x26FF, 0x1F000-0x1FFFF, 0x2500-0x257F.
5. **Graphics/Model Maker = no dates** — These registers use blank/em-dash stage markers only. Client RFI pending on research/data. Legend note: "Dates TBC - RFI raised to client for research/data."
6. **Drawing numbering (MOC format)** applies to Architecture register only: `MOC-ASE-AR-ARC-{Floor}-DDD-{Cat}-{Rev}`. System-based registers (MEP, Lighting, AV, FLS) keep simple prefix (ME-xxx, LI-xxx, AV-xxx, FL-xxx).
7. **Dependency logic**: Architecture is critical path. Landscaping starts after Arch 90% (29/07/2026). Level 0=Foundation (Arch, Structural, Oddy), Level 1=Needs Arch 50% (MEP, FLS, Lighting, AV, Showcase), Level 2=Needs Arch 90% (Landscaping, Interactives), Level 3=Needs client data (Graphics, Model Maker), Level 4=Close-out (QA/Commissioning).
8. **Generate to /tmp first**, then copy to OneDrive via Finder `duplicate` (not `cp`). OneDrive `cp` produces corrupt files. Verify with `xxd -l 8` — must start `PK\x03\x04`.

### Register Log Document Status Check
**Always check the Register Log before referencing any document status in a plan.** Never assume a document's current status from memory or prior session knowledge — statuses change (Code C → Code B → Under Review, etc.).

- **File**: `Docs/09_Registers/_Master_Register_Index/Register Log.xlsb` (master) or `Register Log (N).xlsx` (user-shared copy, same data, openpyxl-compatible)
- **Library**: Use `pyxlsb` (NOT `xlrd` — `.xlsb` is the binary Excel format, xlrd only supports `.xls`)
- **Install**: `pip install pyxlsb`
- **Sheets**: 30+ sheets covering different doc types (Document Submittals, Shop Drawings, RFI, Site Instruction, etc.)
- **Search ALL sheets** for the document number — a doc may appear in any sheet depending on its type
- **Excel date serials**: `datetime.date(1899, 12, 30) + datetime.timedelta(days=int(serial))` to convert
- **Status codes**: A=Approved, B=Approved as Noted, C=Revise & Resubmit, D=Under Review, E=Rejected, U=Under Review
- **Multiple submissions per row**: Each row has columns for R0/R1/R2/R3/R4 with Date Received / Forwarded to Client / Returned / Status / Days — read across all submission cycles to get the full history
- **OneDrive timeout**: Direct `openpyxl.load_workbook()` on OneDrive `.xlsb` files may timeout. Use `terminal` with `python3 -c` or `execute_code` with `from pyxlsb import open_workbook` reading directly from the OneDrive path.

Example: Master Programme MOC-ASEER-0PS-SH-006 was listed in the plan as "resubmitted after Code C" but the Register Log showed Rev.03 was submitted 09-May and is currently **Under Review** — a completely different status.

### PROJECT_MEMORY.md Maintenance
- Track critical issues in dedicated sections
- Use action items table with owner + deadline
- Rev versioning at header
- OneDrive files may hit "Resource deadlock avoided" — use `brctl download <file>` first or write update file side-channel

## BIM Unit Project Information Search

When the user asks about a project you don't have in memory, use `references/bim-unit-project-search.md` for the systematic search path through the BIM Unit folder structure. The key insight: email subject lines reveal project scope; design content lives in non-text attachments (PDF/DWG) that need OCR; the `.bak` backup may have zeroed-out files — prefer the live OneDrive path.

## Oracle Construction & Engineering (Aconex) Access

The project's CDE is Oracle Construction & Engineering (formerly Aconex). See `references/oracle-aconex-browser-access.md` for login flow, navigation, and known browser limitations.

**Key facts:**
- URL: `https://constructionandengineering.oraclecloud.com/idcsLogin`
- Modules: Home, Models, Documents, Mail, Field, Packages, Workflows, Directory, Insights, Setup
- Document register may be populated (Aseer Museum had 125 docs)
- Heavy SPA — slow in headless browser; content is in cross-origin iframes
- Best extraction: export via Reports → Excel, then process programmatically

## Pitfalls
- **Column cleanup must not match "Submittal / Deliverable (per SOW)"** — When removing SOW/ER columns from submittal register xlsx files, the header "Submittal / Deliverable (per SOW)" contains "SOW" as a substring. Naive matching (`'SOW' in val`) deletes the description column. Fix: match exact column names (`'SOW §'`, `'ER §'`, `'ER §b'`) only — never substring-match `'SOW'` or `'ER'`.
- **Regenerate from .py scripts, don't patch .xlsx** — Once columns are incorrectly deleted from .xlsx, it's faster to regenerate from the .py generator scripts than to try inserting columns back. The .py files are the source of truth. See `references/submittal-register-date-conversion.md` for the full regeneration pattern and date-conversion workflow.
- **Date columns instead of stage markers** — Stage columns (50%, 90%, 100%, IFC) can hold **planned dates** instead of blank/`—` applicability markers. Each sheet shows only its own stage's date; others shown as `—`. This is more useful for tracking than the old indicator format. See `references/submittal-register-date-conversion.md` for the staggered scheduling pattern (7d buffers between categories/floors).
- **Verify all registers after bulk regeneration** — After regenerating all 17 xlsx files, check: (1) column 2 = "Submittal / Deliverable", (2) stage columns contain dates not markers, (3) each sheet has correct item counts. OneDrive `cp` may produce corrupt files — use Finder `duplicate` via AppleScript.
- **Filename mismatch from subagents** — Subagents may generate files with different naming conventions (`FitOut_` vs `Exhibition_FitOut_`, `OddyTesting_` vs `Oddy_Testing_`). Always rename to match the folder name after copying.

## Pitfalls

...
- **User repeating instruction = go to source, don't guess** — If the user says the same thing 2+ times (e.g., "use same org chart as aseer"), you're getting it wrong. STOP trying to reconstruct from memory or adapt. Read the ACTUAL source document (Aseer HTML file or the specific referenced file) and replicate its exact structure. The source file path is in the conversation or session history — search for it. Never trust your memory of what the Aseer format looks like; trust what the file actually contains.
- **Team CV table: never fabricate names** — When building the "Proposed Team" CV summary for a proposal, do NOT invent generic Arabic names like "أحمد السعيد" or "خالد العتيبي". Read the actual KPR Excel and use real Samaya team members. The user explicitly corrected this and said "i dont know form where this team — use samaya team."
- **Team framing: "for this project", not "from Aseer"** — When describing the proposed team, present it as selected for the current project with proven museum experience. Do NOT say "this is the Aseer team" — the user rejected this and asked to reframe. Add qualification for specialist firms not yet formally approved for the new project.
- **Sub-agent content duplication check** — After any sub-agent (Claude, Codex, etc.) replaces/patches content in a large HTML file, always verify: (1) div/section balance, (2) no duplicate old SVGs, legends, or section wrappers left behind (search for old comment markers, `<!-- =====` patterns, repeated section headers), (3) the old content didn't leave orphaned `</div>` or extra `<section>` tags. Sub-agents patch exact text spans — anything outside the span (wrapper divs, adjacent comments) stays in the file and causes structural issues.
- **Arabic Unicode normalization** — When comparing filenames across systems, normalize Alef variants (أإآٱ → ا), Yeh variants (ىئ → ي), Teh Marbuta (ة → ه). Use NFC+lower+diacritic stripping before comparison.
- **OneDrive deadlocks** — PROJECT_MEMORY.md on OneDrive frequently returns "Resource deadlock avoided" via direct file reads. Try `brctl download` first, or write side-channel updates to `~/Documents/04_Outlook_Connection/mails/` and merge when sync clears.
- **Don't over-specify options** — Present the situation, not a multiple-choice menu. Ask "what do you want to do?" not "option A, B, C, or D?"
- **Entity isolation** — Never mix Aseer, Zamzam, Moqtana, Tqanny, or Sada_Uhud data in the same operation without explicit direction.
- **Dangerous UI actions must be hidden** — Reset/Danger buttons (like "Reset to Defaults") must be hidden by default or behind a confirmation dialog. Only show when the user explicitly asks for them. Users will accidentally click them.
- **Admin-only controls** — Any function that modifies data (edit hotspots, add materials, delete items) must be gated behind admin mode (`?admin=1` or similar). Regular users see view-only mode.
- **Document revision numbering** — Only count formal submissions to the consultant/CG. Internal drafts (QC iterations, interim refinements) do NOT increment the formal revision number. Always check the CG response folder for the last submitted version before assigning a new revision number.
- **Cover subtitle must match revision table** — The cover subtitle (e.g., "REV 02 · CG CRS Resubmission") must align with the revision history table description. Do not invent a generic subtitle like "Role-Based Update" — derive it from the actual revision table entry.
- **Never assume a name without email evidence** — Before populating any person's name in a register or plan, cross-reference against Outlook or formal correspondence. CV filenames and KPR originals are not sufficient evidence of formal appointment. Mark unconfirmed as "TBC" with a note.
- **Stale personnel data in responses** — When the user asks about a project document, plan, or personnel, do NOT rely solely on memory. Cross-reference BEFORE answering: (1) `session_search` for recent personnel changes in the last 2 weeks, (2) the KPR register Excel, (3) memory. Personnel turnover is frequent (new PD ~13 Jun, QA/QC left, etc.) and previous sessions always document these changes. A single session-search call is cheaper than a user correction.
- **KPR "Pending submission" ≠ vacant** — When aligning an HTML plan against the KPR, "Pending submission" means the person IS on board and working — their CV just hasn't been formally submitted to MoC yet. DO NOT blank out their names. Show the name with status "On board" (or no status label at all per user preference). Only blank out roles that are genuinely "Vacant" or "TBC / Not yet appointed."
- **No approval-status labels in org charts** — User explicitly does NOT want "pending MoC submission" or "Overseas" qualifiers next to personnel names in plan documents. Show the name only. The KPR is the authoritative source for approval status — the plan document doesn't need to restate it.
- **Entity name accuracy** — Always use the exact entity name from the KPR, not approximations or transliterations. Common errors: "Nama Al Amal" → should be "Nama Consulting"; "Glassbühne" → should be "Glasbau Hahn". When in doubt, read the KPR Excel directly.
- **Location filtering in plan documents** — Only mention Riyadh and Abha as locations in plan documents. Remove Dubai, London, Egypt, "Overseas", or any other non-project-site location qualifiers next to personnel or specialist firms. The location matrix has columns for HO Riyadh / Site Abha / Remote — that's sufficient. Don't add city names inline next to names or firms in org charts or role tables.
- **Code C phrasing** — When a role has "Code C — Revise and Resubmit" status in the KPR, the plan document should say "submission in progress" — NOT "Code C (revise & resubmit)" or "pending re-approval". The plan is a forward-looking document; CG review codes are KPR-level detail that don't belong in the plan narrative.
- **BIM Manager identity — project-specific** — Per-project, not universal:\n  - **Aseer Museum**: Dr. Waleed Abdelmabood Salah (BIM Manager, Riyadh HO, monthly site visits). Eng. Ali Abdelrahman Mostafa is Arch BIM Lead (on-site coverage). They are separate people — never merge or duplicate.\n  - **RCRC Exhibition**: Ali Abdelrahman (BIM Manager, Full-time). Update both the team table (role + name + status → Full-time) AND the CV section (name, role title, experience summary) when the BIM Manager changes. RCRC BIM Manager is NOT Dr. Waleed — do not copy Aseer's team member into RCRC proposals.<\｜｜DSML｜｜parameter>
<｜｜DSML｜｜parameter name="file_path" string="true">SKILL.md
- **table-layout:fixed for A4 HTML plans** — When an HTML plan has tables with `th style="width:X%"` column widths, add `table-layout:fixed` to the global `table` CSS rule + `word-wrap:break-word; overflow-wrap:break-word` to `td` and `th`. Without `table-layout:fixed`, browsers ignore width percentages and auto-size columns by content, causing overflow on A4. This one-line CSS fix handles all tables globally — no per-table fixes needed. Also convert any pixel-based column widths (`60px`, `22px`) to percentages — pixels work on screen but misalign on A4 print.
- **No PMBOK/methodology jargon in client-facing documents** — Remove "aligned to PMBOK practices", "PMBOK-compliant", "WBS", "RBS" abbreviations from section titles and descriptions. These are internal methodology references that mean nothing to CG/MoC. The plan document should state WHAT it does, not WHICH framework it follows. Also remove "aligned to [internal doc]" annotations (e.g., "aligned to SMP Rev 03") — internal cross-references are not useful to the external reviewer.
- **Zero internal commentary in CG submissions** — Never include: PD/HR action blocks, 'Hiring in progress', 'Pending submission', 'Not yet appointed' status labels, 'TBC — Code C', 'TBC — pending approval', ' — ⚠ CRITICAL PATH' warnings, 'Submission in progress' notes, or any self-incriminating language (urgent warnings, shortage alerts that could be read as failures). Plan shows firms/roles; KPR is approval authority. Vacant = honest, not missing.
- **Compact section redesign for overstuffed pages** — To fit a section on one A4 page: compress table padding to 1-2px, font-size 0.35-0.4rem, line-height 1.15; use single-row ribbon for cards (6 T1 cards in one row); group individual roles into tier rows with headcounts; use 2-column layout for related subsections; shrink SVG viewBox height. Scope overrides with .s3 class + !important.
- **No internal-only information in client-facing documents** — Remove internal change notes ("added Interactive Design, Lighting, ICT Security"), internal tool references ("Primavera P6", "QS_Template.xlsx" → use "QS Template"), and internal revision tracking annotations. The plan is for CG review — only include what CG/MoC need to see. If a note only makes sense to Samaya staff, remove it. **Companion documents section**: only list documents with formal Aconex doc numbers that CG can trace (e.g., KPR, DMP, BEP, HSE Plan, Master Programme). Remove internal tools and registers that have no Aconex number (e.g., "RACI Matrix maintained in EDMS", "QS Template", "Physical Resource Registers") — CG will question anything they can't look up in the system.
- **Materials lists from actual NRS exhibition schedules** — When populating a materials/resource section in any plan, pull from the actual NRS schedules at `Design Files/Package_Part 2/03_AS_Pre Design Pack_250313/03_AS_Pre-Appointment Exhibition Schedules_250313/Xcel/`. The finishes schedule alone has 84 entries across 13 categories with 16 named suppliers (Ceramiche Piemme, Concept Tiles, Domus, Tarkett, Asona, Knauf, Kvadrat, Clay-works, Corian, Hi Macs, Smile Plastics, Valchromat, Viroc, ARPA, GF Smith). Also check showcase_schedule, FF&E schedule, setwork_schedule, AV equipment schedule, and lighting_schedule. Do NOT use generic lists like "concrete, rebar, blockwork, steel, finishes" — the user expects specific named products and suppliers from the actual project data.
- **Include ALL named personnel in team/location lists** — When listing team members at a location (e.g., "Technical Office, Riyadh HO"), include ALL named personnel from the project, not a subset. The user noticed when Ali A. Mostafa and Mohamed Mostafa were missing from the BIM Modelers list. Cross-reference the KPR and project team memory to ensure no one is omitted from location-based team listings.
- **Location-based labels for Tier 1 cards** — When a person is based at Riyadh HO, show "Riyadh HO" as their status label (not generic "On board"). "On board" is for site-based or non-location-specific roles. The BIM Manager (Dr. Waleed) is Riyadh HO based with monthly site visits — his Tier 1 card says "Riyadh HO" and the location matrix shows HO Riyadh = ● (primary). This distinction matters to CG/MoC who need to understand the team's geographic distribution.
- **NRS exhibition schedules reference** — For the full inventory of all 21 NRS schedule files (finishes, FF&E, setwork, showcase, AV, lighting, etc.), their locations, structures, and named suppliers, see `references/nrs-exhibition-schedules-inventory.md`. This reference saves rediscovering the schedule file paths and data structures each session.
- **Appendix B is the authoritative specialist scope** — When listing specialist packages in any plan, follow ONLY Appendix B (`Subcontractors/_MANAGER_DASHBOARD/APPendix B.pdf`). Do not add roles from the KPR or other sources that aren't in Appendix B. If a KPR role is not in Appendix B, remove it from both the plan AND the KPR Excel (delete row, absorb scope into the relevant remaining entity, fix summary formula ranges). User directive: "we follow only the Appendix B — don't add extra work that isn't required." Example: Fire-Proofing Contractor was in KPR (ER §3.2.B.3) but not in Appendix B — removed from both, Nama Consulting absorbed fire-stopping scope. **Exception:** If CG formally requests a role via a site instruction (e.g., ICT Security System Integrator per `MOC-MUS-CG-ASE-1KN-PQ-013`), include it in both the plan and KPR with a remark citing the CG site instruction number. This shows CG it's their own request, not Samaya adding scope.
- **BIM Manager coordination description** — Use "weekly online coordination · monthly site visits" (NOT "daily online coordination" or "monthly site presence"). Include "on-site BIM support: Eng. Ali A. Mostafa" in the location matrix remarks column — Ali provides site BIM coverage when Dr. Waleed isn't physically at site. Dr. Waleed is Riyadh HO based (HO Riyadh = ● primary, Site Abha = ○ visits, Remote = —).
- **"appointed" vs "on-site" for non-site personnel** — When someone is assigned to the project but not physically at site, use "appointed" as their status label, not "on-site". "On board" is for site-based or non-location-specific roles. "Riyadh HO" is for head-office-based personnel.
- **Materials lists in plans: generic only, no brand names** — When listing materials in a plan document (not a procurement or specification document), use generic material descriptions only. Do NOT mention brand/supplier names (e.g., write "porcelain tiles" not "Ceramiche Piemme", "acoustic panels" not "Kvadrat", "solid surface" not "Corian"). Brand names belong in procurement schedules, material registers, and specification documents — not in high-level management plans. Exception: showcase/AV systems where the supplier defines the system (e.g., "AV hardware by Rawasen") — keep the supplier only, remove product model names.
- **No Junior Engineer names in org charts** — Remove any "Junior Engineers" row from tier tables in plan documents. The user explicitly rejects naming junior-level support staff. Only named personnel (senior/lead roles) and role-category rows (e.g., "BIM Modelers (3)") appear in org structures.
- **Never name unapproved consultants in plans** — Before listing any specialist/consultant by name in a plan document, verify they are formally approved (Code B or better in KPR, or signed contract). Unapproved candidates: (1) use generic role title only (e.g., "Sustainability Strategy" not "Dr. Ehab Foda"), (2) omit certification names that imply the project is committed (e.g., write "Sustainability Strategy" not "LEED / Mostadam" if LEED registration hasn't started), (3) mark the role as "—" or "submission in progress" — never the person's name. This applies to Sustainability, Interactive/Lumotion, and any other pre-qualification-stage consultant.
- **Mohamed Mostafa = Mechanical Engineer, not BIM Modeler** — Eng. Mohamed Mostafa is the Tech Office Mechanical Engineer (HO), listed under Tier 2 Full-Time Samaya. He is NOT a BIM Modeler. Double-check the tier assignment of any person whose role seems ambiguous — Tech Office engineers are Tier 2 FT, not Tier 3 BIM support.
- **Plans: don't mention certification names that aren't committed** — When a project hasn't formally registered for a certification (LEED, Mostadam, etc.), do not list the certification name in the plan. Use neutral terms like "Sustainability Strategy" instead of "LEED / Mostadam strategy" or "Mostadam compliance." Listing uncommitted certifications implies the project is contractually obligated when it isn't.
- **Procurement through Samaya ERP** — When describing procurement processes in plans, specify "Purchase Orders issued through Samaya ERP system" — not generic "approved vendors." This is the actual system Samaya uses.
- **Site office = existing building rooms, NOT portacabin** — Samaya does NOT build portacabin complexes at site. They use existing rooms in the building, furnished and equipped. Never write "portacabin office complex" or "site office shell delivered" in any plan. Use "existing building rooms — furnished and equipped."
- **Standard risk register format for plan documents** — Use a proper project management risk register table with columns: #, Risk Description, Category, Probability (1-4), Impact (1-5), Rating (P×I with color badge), Mitigation/Response Strategy, Owner, Status. Include scale legends below the table. Status values: Open / Tracking / Planned / Closed. Rating thresholds: 1-4 Low (green) · 5-9 Medium (amber) · 10-20 High (red). Do NOT use card-grid layouts for risk registers — the user explicitly rejected the card-grid design in favor of the standard PM table format. See `references/aseer-html-doc-standard.md` for the full table template.
- **Workflow charts in HTML plans** — Add compact inline SVG workflow charts to process sections (induction, replacement protocol, procurement lifecycle, monitoring cycle, change control) to make plans easier to read. Use the document's color palette (navy boxes, gray arrows, colored highlight boxes for critical steps). See `references/aseer-html-doc-standard.md` for SVG style guidelines and patterns.
- **TBC highlighting in KPR Excel** — When updating the KPR Excel, highlight all cells containing "TBC" (Name column, Authority Registration column) with light yellow fill (`PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')`). Only highlight cells where TBC is the primary content, not cells that merely mention TBC in a longer note.
- **KPR tier verification** — After any KPR Excel edit (row insert/delete), always print all rows with their Tier column to verify every role is in the correct tier. Check for: (1) caps glitches in role names (e.g., "CONSTRUCTION MANAGER" in all caps), (2) shifted columns from `insert_rows()` corruption, (3) incomplete rows missing discipline/status fields, (4) summary formula ranges that need adjustment after row count changes.
- **Sub-agent timeout on large HTML redesigns:** Delegating a full redesign of a 200KB+ HTML file as a single sub-agent goal almost always times out (600s+). Instead, break into verify→targeted-patch cycles. After timeout, check progress via file size change and grep for key terms; complete remaining work with targeted patches.
- **KPR insert_rows() is unreliable on OneDrive** — `ws.insert_rows()` may silently fail on OneDrive-stored .xlsx files — the row appears inserted in memory but is empty when re-opened. Always verify by reading back the row after save. If empty, write directly to the target row index instead of inserting.
- **FARO Focus Premium 200** — The project laser scanner is a FARO Focus Premium 200. Always use this exact model name in equipment lists, not generic "laser scanner."
- **Acting/behalf sign-off for vacant roles** — When a sign-off role is vacant (e.g., QA/QC Manager), another team member can sign on behalf. Format: "Eng. Mohamed Samir (acting)" with "(acting)" in smaller muted text. The role title stays as the formal title (e.g., "QA / QC Manager") — only the name column shows the acting designation. This applies to both the revision history sign-off table and the final document control block.
- **Appointed Acting role — update all 3 blocks in MOS/plan HTML docs** — When someone is appointed to a role as Acting (not just signing on behalf), the role TITLE changes (e.g., "Samaya QA/QC Manager" → "Samaya Acting QA/QC Manager"). Update ALL three distinct blocks in Samaya MOS/plan HTML documents:\n  1. **Cover page QC block** — uses `.role` / `.nm` / `.tt` HTML class structure\n  2. **Section 13 Approval page** — uses `.k` / `.v` + inline `div` structure\n  3. **Section 13 QC Sign-off** — uses `.role` / `.nm` / `.tt` class structure (same as cover, different section)\n  Use `search_files(pattern='Samaya QA/QC Manager')` or equivalent to find all occurrences before editing. Patch each block individually — the HTML class structures differ so a global find-replace on the name alone isn't sufficient. After editing, re-search to verify all blocks were updated. See `references/mos-person-assignment-update.md` for the worked example from this session (LiDAR MOS, Eng. Mohamed Samir as Acting QC Manager).\n\n### Key Personnel Kickoff Meeting
When a new key personnel member is approved (Sustainability Manager, BIM Manager, QC Manager, etc.) and needs onboarding, follow `references/kickoff-meeting-pattern.md` — 4-page HTML kickoff document with agenda, SoW table, certification credit pathway, 30-day task plan, and action items. Worked example: Aseer Museum Muhammad Fida Noor kickoff.

## GitHub Version Control\n\nUse GitHub for version control on all technical proposal HTML files, especially after major structural edits (expanding sections, removing duplicates, renumbering pages).\n\n**Setup (one-time):**\n```bash\nmkdir -p /tmp/<repo-name>\ncp "$FILE" /tmp/<repo-name>/\ncd /tmp/<repo-name>\necho "*.bak" > .gitignore\ngit init\ngit add -A\ngit commit -m "Initial commit: <Project> Technical Proposal"\ngit branch -m main\ngh repo create <user>/<repo-name> --private --source=. --remote=origin --push\n```\n\n**Work on /tmp, not OneDrive:** Git operations on OneDrive paths are extremely slow and timeout-prone. Always copy the HTML file(s) to `/tmp/<repo-name>/` for git operations, then deploy from there. The OneDrive path is only for the working copy.\n\n**Daily workflow:**\n```bash\ncp "$ONEDRIVE_FILE" /tmp/<repo-name>/\ncd /tmp/<repo-name>\ngit add <file>.html\ngit commit -m "Description of changes"\ngit push origin main\n```\n\n**When the file has duplicate content (Part 01 + Part 02):** Remove the duplicate Part 02 cover and sections 2-8 before the first commit. The git history should represent the clean, deduplicated version — not the raw export with two copies.\n\n**Commit messages:** Be descriptive about structural changes. Examples:\n- "Remove duplicate Part 02 cover and sections 2-8, renumber pages sequentially"\n- "Expand Section 8 from 1 to 3 pages with 13 project cards"\n- "Fix ER/SOW references in Section 34 compliance matrix"\n\n**Repo naming convention:** `<ProjectCode>-Proposal` (e.g., `RCRC-Exhibition-Proposal`). Repo is private.\n\n**Current repos:**\n- `github.com/sultandroid/RCRC-Exhibition-Proposal` — RCRC Exhibition Technical Proposal AR
