# Subcontractor Scope Analysis & RFI Register Creation

## When to use

A subcontractor has been issued a scope-of-work request (SCOPE_REQUEST) but needs help understanding their full scope. You need to identify ALL RFIs / clarifications required to make their scope complete and clear for them to start work. The sub already has a numbered folder (e.g., `Subcontractors/08_Graphics_Contractor/`) — this is NOT about creating a new folder.

## Pipeline

### Step 1: Read the sub's existing scope documents

Start with what's already in the subcontractor's folder:

| Document | Location | What to extract |
|----------|----------|-----------------|
| SCOPE_REQUEST.docx | Sub root (e.g., `NN_Discipline/SCOPE_REQUEST.docx`) | What was asked of the sub, programme, deliverables |
| SITUATION_REPORT.md | `_MANAGER_DASHBOARD/SITUATION_REPORT.md` | Current status, known gaps, critical issues |
| Briefing Pack (if exists) | `02_Reference_Drawings/` or `03_Specifications_and_Standards/` | Full scope definition (NRS-sourced), RACI, sign-offs, adjacent trades |
| BOQ extract | `01_Schedule_and_BOQ/` | Quantities, ambiguous line items (TBD dimensions, nr items) |
| Print Materials Spec | `08_Material_Submittals/01_NRS_Specs/` | Material compliance requirements, tiered cert matrix |
| RFI Register | `06_RFIs/RFI_Register.xlsx` | Already-asked questions (likely empty for new subs) |
| Email Database | `Email_Data_Extraction/` | Prior correspondence, design-stage discussions |
| Contract / SOW extracts | `03_Specifications_and_Standards/` | Contractual basis for the scope |

### Step 2: Read the project's governing documents

Cross-reference the sub's scope against the project baseline. This is the step most often missed — the scope document alone is insufficient:

| Document | Location | Key sections for scope analysis |
|----------|----------|--------------------------------|
| **SOW (Contractor's Scope of Work)** | `Docs/01_Contracts_and_ER/01.3_Contractors_SOW/` | §2.2 Scope exclusions, §8.14 Graphics artwork, §6.22.1 Graphic Design, §8.1 Mock-ups/samples |
| **ER (Employer's Requirements)** | `Specs & Datasheet/Project Codes/` | §2.2 Design life, §12 Wayfinding, Scenographer's Documentation coordination |
| **Communication Plan** | `Correspondence/` (doc code PL-0018) | Submittal workflow (material submittals BEFORE shop drawings), escalation matrix, stakeholder inclusion |
| **Stakeholder Management Plan** | `Correspondence/` (doc code PL-0020) | T2 allocation table — who is contractually responsible for what |
| **DMP (Document Management Plan)** | `Docs/02_Plans_and_Procedures/` (PL-0029) | Submission sequence rules, doc numbering, CDE protocol |

### Step 2b: Create/update the project document index

After reading any governing document, immediately update `_Project_Memory/DOCUMENT_INDEX.md` with extracted key clauses. This is NOT optional — without it, every future session re-extracts the same PDFs.

The index captures **extracted knowledge** (not file listings) organized by:

| Section | Contents |
|---------|----------|
| Contractual baseline | ER, SOW, Main Contract — key sections, clauses, numbers |
| Management plans | DMP, Comm Plan, Stakeholder Plan — status (Code A/B/C/D), key rules |
| Package-specific docs | Briefing Pack, Scope Request, Specs, BOQ |
| Recent correspondence | Last 2 weeks — doc code, subject, status, date, location |
| Key people & roles | Names, organizations, contacts |
| Project codes & zones | Doc numbering conventions (e.g., `1A0` = architectural) |
| Key dates | Milestones, TOC, install windows |
| Adjacent subcontractors | Number, name, scope, status |

**Output format:** Generate both markdown (`DOCUMENT_INDEX.md`) and Excel (`DOCUMENT_INDEX.xlsx`) versions. The Excel version should have separate sheets per category with navy headers, alternating row colours, and wrapped text. Use openpyxl.

The markdown version is for quick agent reference; the Excel version is for human stakeholders who prefer spreadsheet navigation.

Format per document entry in markdown:

```markdown
### [Doc Title]
| Field | Value |
|-------|-------|
| **File** | [relative path] |
| **Rev** | [rev, date] |
| **Key extracted content** |

| § | Topic | Key content |
|---|-------|-------------|
| [section] | [topic] | [summarised clause — not verbatim] |
```

**Pitfall:** Skipping this step looks efficient in the moment but creates repeated work. The user will explicitly require it if you don't do it — and they'll be frustrated that you didn't think of it.

### Step 2c: Extract key clauses from PDFs efficiently

Use `pdftotext` with targeted `grep`/`sed` to extract relevant sections without reading entire documents:

```bash
# Find relevant sections by keyword
pdftotext -layout "path/to/doc.pdf" - | grep -n -i "keyword1\\|keyword2" | head -30

# Read specific page range
pdftotext -layout "path/to/doc.pdf" - | sed -n 'START,ENDp'

# Extract from first N pages only (-l flag)
pdftotext -l 10 "path/to/doc.pdf" - | grep -n -i "keyword"
```

Key keywords to grep for: `graphic`, `wayfinding`, `signage`, `label`, `bilingual`, `typeset`, `fabricate`, `panel`, `donor`, `sponsor`, `directory`, `tactile`, `braille`, `exclusion`, `scope`, `exhibition text`

### Step 3: Phasing assessment — what to raise NOW vs WAIT

**Before categorizing RFIs, assess which project stage you're in.** Not all RFIs are actionable at once. Raising RFIs at the wrong time wastes everyone's time and looks unprepared.

| Project Stage | What's actionable | What to hold |
|---------------|-------------------|--------------|
| **Pre-DD / DD not submitted** | MoC content (independent of design), scope boundaries, trade coordination, commercial/pricing | Design clarifications (DD will answer), material submittal protocol (premature without approved design) |
| **DD submitted, awaiting CG review** | MoC content, scope boundaries, trade coordination — all still valid | Material approvals, submittal protocol (needs design approval first) |
| **DD approved / IFC stage** | Design clarifications (gaps not in DD), material certifications, submittal protocol | — |

**How to check the project stage:**
- Look at `09_Correspondence/` for recent submittal codes — DD/IFC packages will have a doc code and status
- Check `_Project_Memory/PROJECT_MEMORY.md` for status updates
- Ask the user if unsure: "What stage is the design at? Has DD been submitted?"

**Pitfall:** Raising design-related RFIs before DD submission signals you don't expect the design to answer those questions — which undermines confidence in the design package. Let the design speak for itself first.

### Step 4: Categorize RFI types

Organize identified gaps into standard categories:

| Category | Description | Example |
|----------|-------------|---------|
| **MoC Content** | Information only MoC can provide | Exhibition text delivery date, content format, translation |
| **Scope Boundary** | Unclear who does what between trades | Housing split (Sub-08 vs Sub-06), artwork development responsibility |
| **Design Clarifications** | Missing/ambiguous design info | TBD dimensions, unresolved finish decisions, missing elevation plans |
| **Adjacent Trade Interfaces** | Coordination points with other subs | Showcase dimensions (Sub-02), housing clearances (Sub-06), Oddy testing (Sub-10) |
| **Material Approvals** | Compliance certs and approval process | Tier-A cert matrix, sample submittal protocol, AVL |
| **Submittal Protocol** | How to submit and get approval | RACI confirmation, DMP sequencing, proofing workflow |
| **Programme & Logistics** | When and where to work | Site access dates, production timeline, install logistics |
| **Commercial & Contractual** | Pricing, warranty, variations | Pricing confirmation, defects liability, change mechanism |

### Step 5: Cross-reference SOW exclusions against scope

SOW §2.2 lists items **excluded from Contractor scope** — these become RFIs to MoC (not to the sub). Examples:
- "Exhibition text and object label text to be supplied by MoC" → RFI: when is text ready?
- "Additional content research to be supplied by MoC" → RFI: what research deliverables?
- "Copyright and licensing of imagery to be supplied by MoC" → RFI: when are images provided?

### Step 6: Identify contract/SOW obligations the sub may not know

SOW clauses often impose requirements the SCOPE_REQUEST didn't communicate:
- SOW §8.1: 200×200mm samples of all visible materials + 1:1 scale samples of all graphic types + 3 sets of sample boards
- SOW §8.14: Minimum 3 rounds of review for MoC approval
- SOW §8.14: Signage pedestals and rails in Contractor's scope

Cross-check each SOW obligation against what the scope request covers.

### Step 7: Produce the RFI register

Save to `_MANAGER_DASHBOARD/GRAPHICS_RFIS_REQUIRED.md` with format:

```markdown
# Sub-NN — RFIs Required to Clear Scope

**Contractor:** [Name]
**Date:** [date]
**TOC:** [date]

---

## RFI Register

| # | RFI Topic | Question to Ask | Target | Priority | Unlocks | Ref |
|---|-----------|----------------|--------|----------|---------|-----|
| 1 | [topic] | [question] | CG/MoC/Internal | 🔴 High | [dependency] | [doc ref] |

## Priority Summary

### 🔴 High Priority
Items that block the critical path — must answer before work can start.

### 🟡 Medium Priority
Needed for detailed planning, can run in parallel with high-priority items.

### 🟢 Low Priority
Can be answered later — commercial/contractual details.

## Key Findings from Reference Documents

Summarize the most important extracted clauses from ER, SOW, Comm Plan, etc.

## Next Steps

| Step | Owner | Timeline |
|------|-------|----------|
| 1. Review register with PM | Tech Office + PM | Today |
| 2. Raise RFIs to CG/MoC | Tech Office | This week |
| 3. Raise internal RFIs to adjacent subs | Tech Office | This week |
```

### Step 8: Draft the actual RFI documents

After producing the RFI register, **draft the actual RFI documents for the actionable items**. The register identifies what needs asking — the RFI documents are the formal communication.

Create files in the sub's `06_RFIs/` folder:

| Type | File naming | Audience | Content |
|------|-------------|----------|---------|
| Internal RFI | `INTERNAL_RFI_NNN_Topic.md` | Samaya team / sister companies | Has all questions but informal — can be email or Teams message |
| Adjacent trade memo | `INTERNAL_RFI_NNN_Adjacent_Trades.md` | Other subcontractors (via Samaya) | Interface coordination — dimensions, dates, responsibility split |
| Formal TQ/RFI to CG | `FORMAL_RFI_NNN_CG_Topic.md` | CG / PMC / MoC | Structured for Aconex submission — formal tone, doc refs, response deadline |
| MoC content RFI | `FORMAL_RFI_NNN_MoC_Content.md` | MoC (via CG) | SOW §2.2 excluded items — content delivery, format, timeline |

Each RFI document should include:

| Field | Description |
|-------|-------------|
| **Header** | Date, target, from, CC, related RFI register reference |
| **Subject** | Clear one-line summary |
| **Background** | Context — 2-3 sentences max |
| **Questions** | Numbered, specific, actionable |
| **Priority** | 🔴 High / 🟡 Med / 🟢 Low |
| **Requested response** | Reasonable deadline (5–15 working days depending on urgency) |

**Flag draft documents clearly:** If a draft is prepared but not yet for submission (e.g., waiting for DD), append `_DRAFT` to the filename and add a **⚠️ HOLD** notice at the top.

### Step 8b: Convert formal RFI drafts to HTML

After drafting in markdown, convert **formal RFIs** (to CG, PMC, or MoC) into proper HTML using the approved template format. Internal RFIs can stay as markdown.

See the full style guide at `samaya-technical-office/references/rfi-html-format-guide.md` and the blank template at:
`_Style-Guides/samaya-rfi-style-guide/templates/RFI_TEMPLATE.html`

**Key rules for formal HTML RFIs:**
- Monochrome only (black/white/grey) — NO navy, gold, or brand colors
- RTL layout (`dir="rtl"`, `lang="ar"`) — Arabic primary, English secondary
- Fonts: Noto Naskh Arabic (Arabic) + Carlito (English) via Google Fonts
- Include logo-strip (4-party: Samaya, CG, PMC, MoC), dc-block, qc-block
- Evidence quotes in `.callout` blocks with thick left border + doc references
- Alignment: English-only → LTR (`.en-block`), Arabic-only → RTL (`.ar-block`), bilingual → RTL with Arabic leading (`.bi-block`)
- A4 printable with proper `@page` CSS
- DO NOT include "Response Requested" section (user explicitly rejects)
- Logo path from `06_RFIs/`: `../../../../../_Style-Guides/samaya-rfi-style-guide/assets/logo.png`
- Always use relative paths, never absolute `/Users/mohamedessa/...`

**After generating HTML, verify in browser:**
- All images load (check browser_console for 404s)
- English blocks are left-aligned, bilingual blocks right-aligned
- Zero JS errors

### Step 8c: Draft PM summary email

After drafting all RFI docs, write a summary email to PM (Mohamed Samir, Adel Darwish) covering:
1. What was prepared (RFI register + drafted docs)
2. Why urgency matters (TOC date, production lead time)
3. What action PM needs to take (review with sub, approve formal RFIs, push for dedicated personnel)
4. Risks if delayed (scope gaps, compressed production, TOC at risk)

Save to `_MANAGER_DASHBOARD/DRAFT_EMAIL_PM_Action.md` for review before sending.

### Step 9: Clean up, generate branded docs, and finalize

After drafting all RFI docs and the register:

1. **Clean up the subcontractor folder:**
   - Remove duplicate files (e.g., same styleguide PDF in two places)
   - Fix corrupted files (e.g., SCOPE_REQUEST.md with broken encoding)
   - Add/update README.md with folder map and key docs index
   - Update the RFI_Register.xlsx with the new RFI rows
   - Remove empty `SCOPE_REQUEST.md` placeholders if superseded by .docx

2. **Generate a Samaya-branded SCOPE_REQUEST.docx** using the `SamayaDoc` template:
   ```python
   from samaya_doc_template import SamayaDoc
   doc = SamayaDoc()
   doc.create_header(project_name, doc_ref, doc_type, revision, date)
   doc.create_footer(doc_number, confidential=True)
   doc.add_h1('SCOPE OF WORK — ...')
   doc.add_h2('1.0', 'SECTION')
   doc.add_body('...')
   doc.add_table(headers, rows, col_widths_cm=[...])
   doc.save(path)
   ```
   The branded .docx replaces any earlier generic SCOPE_REQUEST.docx.

3. **Update the register's status** in RFI_Register.xlsx after each RFI is sent or answered.

## Revision history

| Date | Change | Trigger |
|------|--------|---------|
| 2026-06-09 | Added Step 2b (document index), Step 3 (phasing by design stage), Step 8 (draft RFI docs), Step 9 (cleanup + branded docs). Added pitfalls for design-stage phasing, document index, draft-vs-ready flagging, and HTML format for formal RFIs. | Scope analysis for Sub-08 Graphics (Graphit) — user corrected approach to include document index and design-stage phasing. |
| 2026-06-09 | Added Step 8b (HTML conversion), Step 8c (PM email), reference to rfi-html-format-guide.md, alignment rules, monochrome template format, no-Response-Required rule. | User corrected alignment (English-only LTR), removed Response Requested section, pointed to specific ARM-SIC-MOC-LET-006 template format. |

## Pitfalls
- **SOW §2.2 exclusions are NOT in the sub's scope** — items excluded from Contractor scope are MoC responsibilities, not gaps in the sub's understanding. Route these as RFIs to MoC (via CG), not to the sub.
- **Communication Plan status matters** — if the Comm Plan is Code C (Revise & Resubmit), the submission workflow isn't approved yet. Flag that the submittal protocol is still being finalised.
- **DMP sequencing rule** — material submittals must be finalised BEFORE shop drawings and IFC. This affects the sub's submission sequence.
- **Adjacent trade coordination needs formal RFIs** — don't assume the sub can coordinate with Sub-02/06 on their own. Privity rules mean all coordination goes through Samaya.
- **Use document codes in RFI register ref column** — this makes findings traceable and verifiable.
- **TOC drives everything** — the installation date (TOC–21d) is immovable. Every RFI should include a programme impact assessment.
- **Bilingual AR/EN is not just translation** — Arabic is primary, requires named native typographer, 3 rounds of review minimum. Ensure the RFI addresses the review cycle.
- **Phase RFIs by project stage** — don't raise design clarifications before DD is submitted. The DD may answer them, and premature RFIs look like you don't trust the design. Always check: what stage is the design at?
- **Draft RFI docs in the sub's 06_RFIs/ folder** — don't stop at the register. The register identifies what to ask; the actual RFI documents are what gets sent. Draft them in full so they're ready for review and submission.
- **Document index is NOT optional** — the user will explicitly require it if you don't do it proactively. After any document analysis session, update `_Project_Memory/DOCUMENT_INDEX.md` with extracted knowledge so future sessions don't re-read PDFs.
- **Flag draft vs ready in RFI filenames** — use `_DRAFT` suffix and a clear HOLD notice for documents not yet for submission. Prevents accidental early submission.
- **Alignment rules are non-negotiable** — English-only content MUST be LTR, Arabic-only MUST be RTL, bilingual MUST follow Arabic lead (RTL). The user will catch and correct every misaligned block. Use `.en-block`, `.ar-block`, `.bi-block` classes consistently.
- **Formal RFIs must be HTML not markdown** — the user requires proper HTML with logos, DC block, QC block, and callout evidence boxes for any document going to CG/MoC. Markdown drafts are acceptable for internal prep only.
- **Monochrome only for formal letters** — no navy, gold, or brand colors. The approved template is black/white/grey (per ARM-SIC-MOC-LET-006). The SamayaDoc template (navy/gold) is for internal/management documents only.
- **No "Response Requested" section** — the user considers this obvious and removes it. End formal RFIs at the Priority section.
- **No "Programme Impact" or "Critical Path Note" sections** — the user removes these ("no need to add"). Programme context belongs in the email to PM, not in the formal RFI to CG/MoC.
- **Email PM after drafting** — always draft a summary email to PM with what was prepared, urgency, and required actions. Save to `_MANAGER_DASHBOARD/DRAFT_EMAIL_PM_Action.md`.
