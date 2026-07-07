# Consultant/Vendor Proposal Evaluation

Standard workflow for evaluating consultant or vendor proposals against project contractual scope (SoW, ER, SMP) and creating structured comparison deliverables.

## When to Use
- User sends consultant proposals (PDF) and asks for evaluation
- User asks for comparison between multiple bidders
- User asks for technical + financial evaluation reports
- Any "evaluate this proposal" request

## Workflow

### 1. Extract Proposal Content
```bash
pdftotext -layout input.pdf /tmp/proposal.txt
```
Read the full text to understand scope, team, pricing model, exclusions, and validity.

### 2. Identify Project Scope Requirements
Reference these contractual documents (in order of priority):
- **SoW (Scope of Work)** — esp. sustainability sections (§13.9, §13.3, §13.12)
- **ER (Employer's Requirements)** — esp. sustainability clauses (§2.4D, §3.7)
- **SMP (Sustainability Management Plan)** — full deliverable list
- **Project-specific standards** — Mostadam, SBC, ASHRAE, Oddy

### 3. Build Evaluation Criteria
Evaluate each proposal against these dimensions:

| Dimension | What to Check |
|-----------|--------------|
| **Technical Scope** | Does it cover ALL project phases (design, materials, fabrication, construction, commissioning, handover)? |
| **Specialist Requirements** | Oddy testing, VOC, LCA, IAQ, BMS? |
| **Team** | Number of experts, named/unamed, location, site visit commitment? |
| **Pricing Model** | Lump-sum vs monthly? Fixed vs open-ended? |
| **Risk Allocation** | Does vendor guarantee certification? Who does engineering work? |
| **Exclusions** | What's NOT included that you'll need to procure separately? |

### 4. Create Evaluation Reports
For each proposal, write a structured markdown evaluation:
```markdown
# Evaluation — [Vendor Name]

**Reference:** [Proposal ref, date]

## 1. Technical Assessment
[Scope coverage per project phase]

## 2. Team Assessment
[Expert count, location, CVs provided?]

## 3. Financial Assessment
[Pricing model, total cost, hidden costs]

## 4. Risk Assessment
[What risks does this proposal carry?]

## 5. Overall Score
[Category scores + total /10]

## 6. Recommendation
[Recommended? With conditions?]
```

### 5. Create Comparison Excel
Use openpyxl with 3+ sheets:
- **Sheet 1: Comparison** — criteria × proposal matrix with winner column
- **Sheet 2: Cost Comparison** — estimated cost over different project durations
- **Sheet 3: Scope Matrix** — each SoW/ER/SMP requirement × coverage (✅/⚠️/❌)

### 6. Organize Files
File structure in the project's sustainability folder:
```
02.12_Sustainability_Strategy/
└── 08_Consultant_Proposals/
    ├── 01_[Vendor]_Proposal.pdf
    ├── 01_EVALUATION_[Vendor].md
    ├── 02_[Vendor2]_Proposal.pdf
    ├── 02_EVALUATION_[Vendor2].md
    └── 03_ASR-SAM-SUS-EVAL-001_Comparison.xlsx
```

### 7. Update Project Knowledge
- Save unified report to OneDrive project folder
- Add evaluation summary to Notion if meeting notes exist
- Register in Hermes memory if vendor details are durable

## Pitfalls

- **OneDrive deadlock** — PDFs under `OneDrive-SAMAYAINVESTMENT/` may be locked. Copy to `/tmp/` first, or work from Hermes cache (`~/.hermes/cache/documents/`).
- **PDF is image-based (scanned)** — `pdftotext` returns empty. Use `tesseract` OCR or `pymupdf` with image extraction + OCR. If low-quality scan (e.g., 72dpi table), inform user and ask for text version.
- **Scope requirements change per project** — don't reuse evaluation criteria from one project to another. Always check the actual SoW/ER for the specific contract.
- **Pricing model comparison is non-trivial** — monthly fee vs lump-sum: calculate break-even point at different project durations.
- **Exclusions are often hidden** — vendor says "comprehensive" but excludes: Oddy testing, laboratory fees, registration fees, travel, site visits. Always compare exclusions side-by-side.
