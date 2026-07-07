---
name: proposal-evaluation
description: "Evaluate vendor/consultant technical and commercial proposals against project scope (SoW, ER). Extract PDFs, cross-reference scope items, score weighted criteria, generate markdown evaluations and Excel comparison files with exact source citations. Includes VAT/tax verification for non-KSA entities, AI-generation detection, critical contradiction analysis, and field presence verification."
version: 1.0.0
author: agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [procurement, evaluation, vendor, proposal, scope-analysis]
    related_skills: [samaya-technical-office, nrs-scope-report, bi-directional-odoosync]
---

# Proposal & Vendor Evaluation

Evaluate technical and commercial proposals against project contractual scope. Produces structured markdown evaluations per proposal plus a multi-sheet Excel comparison file.

## When to Load

- User sends PDF proposals/quotations and asks for evaluation
- User asks "قيم العرض دا" / "compare these proposals"
- User wants vendor comparison against SoW/ER requirements

## Workflow

### 1. Extract Proposals

```bash
pdftotext -layout "path/to/proposal.pdf" /tmp/proposal.txt
```

Read the full text to understand scope, pricing model, team, exclusions.

### 2. Identify the Reference Scope

Determine the scope baseline to evaluate against:
- **SoW (Scope of Work)** — sections like §13.9 Sustainability, §13.3 IAQ, §13.12 Materials
- **ER (Employer Requirements)** — sections like §2.4D, §3.7
- **SMP / Project Plan** — Rev reference (e.g., Rev C04)
- **Contractual pages** the user extracted earlier

### 3. Build Evaluation Criteria

Evaluate each proposal against:

| Category | What to assess |
|----------|---------------|
| **Project Understanding** | Does the proposal demonstrate understanding of this specific project (museum, heritage, challenges)? |
| **Scope Coverage** | Does it cover all required phases (design, procurement, fabrication, construction, commissioning, handover)? |
| **Methodology** | Is it advisory-only or hands-on? Site visits? Field presence? |
| **Team** | Number of experts, named CVs, location, commitment |
| **Commercial** | Fixed vs monthly, predictability, what's included/excluded |
| **Risk** | What risks fall on the contractor vs the vendor |

### 4. Site Visit Verification — CRITICAL

When making claims about field presence/site visits:
- **Search** the exact proposal text for keywords: site, visit, field, trip, travel, mobilization
- **Quote** the exact sentences with page/section numbers
- **Show the proof** of attendance commitment — don't assert without evidence
- If a proposal has zero mentions of site presence, state that explicitly

### 5. Certification Caveat

If the user says "الشهادة غير مطلوبة" (certification not required):
- Remove certification/rating guarantee from evaluation criteria
- Focus evaluation on: practical scope coverage, field presence, understanding of project-specific challenges
- Do NOT deduct points for lacking certification guarantees

### 6. Generate Outputs

#### Per-Proposal Markdown Evaluation

Structure:
```markdown
# Evaluation — [Proposal Name]

## 1. Project Understanding
(table: criterion | rating | detail)

## 1b. Site Presence — Citations from Document
> **Section/Page X:** *"exact quote from proposal"*
> **Section/Page Y:** *"exact quote"*

## 2. Detailed Scope Coverage
(break down by phase, each with ✅/⚠️/❌ + explanation)

## 3. Team Assessment

## 4. Commercial Assessment

## 5. Overall Score & Recommendation
```

#### Multi-Sheet Excel Comparison

Use openpyxl to create an Excel file with:
- **Sheet 1** — Scope Understanding Comparison (understanding depth per criterion, each agent rated)
- **Sheet 2** — Detailed Scope Matrix (every scope item, check per proposal with RAG coloring)
- **Sheet 3** — Recommendation (final verdict, conditions, risk notes)
- **Sheet 4** — Cost Comparison (optional): When comparing fixed vs monthly pricing, add a Cost Comparison sheet showing total cost at multiple project durations (3, 6, 9, 12, 18, 24 months) and calculate the **breakeven point** where the fixed proposal becomes cheaper. Use green fill for the cheapest option at each duration.

Use green (`C6EFCE`) for ✅, red (`FFC7CE`) for ❌, yellow (`FFEB9C`) for ⚠️.

### 7. Citation Rule

Every comparative claim MUST cite the source:
- Page number ✓
- Section heading ✓  
- Exact quote from the proposal ✓
- If supporting documents are OneDrive-locked, extract from what you have and note the limitation

### 8. Critical Review (When User Asks for Weaknesses/Contradictions)

If the user says "طلع منه نقاط الضعف والخلل والتناقض":

1. **Extract contradictions** — find places where the proposal contradicts itself:
   - Pricing model (lump-sum vs time-based in same paragraph)
   - VAT treatment (include vs exclude in same table — this is a common AI error: one row says "All prices include VAT at 15%" while another says "All amounts exclude VAT")
   - Scope claims vs assumptions (says A but exclusions say ¬A)
   - Numerical errors (wrong totals, missing digits, misplaced commas)
   - **Currency cross-check**: verify SAR to USD conversion (rate = 3.75). Check that the total matches the sum of line items. Missing digits like 16,3013 instead of 163,013 are common AI artifacts.

2. **Identify AI-generation markers**:
   - Generic company name (e.g., "Sustainability Consultancy" instead of a real firm)
   - Placeholder names ("Expert 1", "Expert 2")
   - AI-typical phrasing ("Our engagement secures to deliver", "comprehensive", "robust", "seamless", "end-to-end", "holistic")
   - Perfect formatting with shallow content
   - No CVs, no team details, no office location
   - **No legal entity name** — cannot sign a contract
   - **First sentence grammatical errors** coupled with perfect structure later (sign of AI glue + human data)

3. **Verify VAT/Tax validity** (critical for KSA projects):
   - Is the vendor based in Saudi Arabia? If not, **they cannot charge Saudi VAT**
   - Individuals/non-VAT-registered entities cannot issue Tax Invoices
   - If they list VAT but are non-KSA → the VAT line is fraudulent or mistaken
   - Result: client cannot claim Input Tax Credit → the VAT amount is lost money
   - **Double-check**: if "Basis of Pricing" says "all amounts exclude VAT" but the Fee Summary includes VAT — contradiction. Note it.
   - **Even more suspicious**: if the same table row says "All prices include VAT at 15%" AND another row says "All amounts exclude VAT" — this is a strong AI error signal.

4. **Check travel cost attribution** — who pays for site visits?
   - If travel is "arranged and paid by the Contractor" → site visits add $10-15K to total cost
   - If travel is included in the fee → genuine field presence commitment
   - If no travel mentioned → likely remote-only
   - **Critical addition**: if the user says site meetings should be online-only, remove travel from expectations and recalculate cost downwards

5. **Assess team credibility**:
   - Named experts with CVs → high confidence
   - "Expert 1 / Expert 2" → placeholder, low confidence
   - No company legal name → cannot contract
   - **Location matters**: if based outside KSA with no KSA office, factor in coordination overhead

6. **Document in a separate file**: `04_CRITICAL_REVIEW_ProposalName_Weaknesses.md`

7. **Contradiction severity classification** — when reporting, categorize each:
   | Level | Label | Examples |
   |-------|-------|----------|
   | 🔴 High | تناقضات صريحة | lump-sum vs time-based, VAT include vs exclude, wrong totals |
   | 🟡 Medium | تناقضات الـ Scope | Oddy managed but excluded, trips mandatory but negotiable |
   | 🟢 Low | تحريرية | typos, extra punctuation, missing table columns |

## Pitfalls

- ❌ **Don't evaluate against certification standards if user says they're not required** — ask first
- ❌ **Don't claim site presence without quoting the proposal text** — user will verify
- ❌ **Don't use different evaluation criteria across proposals** — same matrix for all
- ❌ **Don't mention Mostadam/SBC credits if scope is advisory-only** — focus on practical work
- ❌ **Don't overlook VAT legality** — non-KSA consultants cannot charge Saudi VAT. Verify the vendor's tax status before accepting VAT line items
- ❌ **Don't assume "lump-sum" means fixed price** — some proposals claim lump-sum but are actually time-based with a cap
- ❌ **Don't assume site visits are a benefit** — verify who bears the travel cost. If contractor pays, it's an additional expense, not a vendor commitment
- ⚠️ **OneDrive deadlocks** — use `kill -9 $(pgrep OneDrive)` to release locks, or read from cache copies
- ⚠️ **Some PDFs are image-based** (scanned) — OCR may fail; note the limitation instead of forcing bad data
- ⚠️ **AI-generated proposals** are increasingly common — check for contradictions, unnamed entities, and generic language

## Output File Naming

```
03_ASR-SAM-SUS-EVAL-00N_Scope_Analysis.xlsx           (Excel: 3 sheets — Scope Understanding / Detailed Scope / Recommendation)
01_EVALUATION_ProposalX_ShortName.md                    (full evaluation with citations)
02_EVALUATION_ProposalY_ShortName.md                    (full evaluation with citations)
04_CRITICAL_REVIEW_ProposalName_Weaknesses.md           (optional: contradictions, AI markers, VAT issues)
```

## Excel Sheet Structure

When generating `.xlsx` with openpyxl:

| Sheet | Content | RAG colors |
|-------|---------|------------|
| **Scope Understanding** | Compare understanding depth per criterion across proposals | ✅ green / ❌ red / ⚠️ yellow |
| **Detailed Scope** | Every scope item mapped to each proposal | Same |
| **Recommendation** | Final verdict, conditions, risk notes | Bold text |

Use these exact hex fills:
- ✅ Green: `C6EFCE`
- ❌ Red: `FFC7CE`  
- ⚠️ Yellow: `FFEB9C`
- Section header: `D6E4F0`
- Table headers: white text on `1E3A5F`
