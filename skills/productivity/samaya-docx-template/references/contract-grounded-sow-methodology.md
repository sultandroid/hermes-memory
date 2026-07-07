# Contract-Grounded SOW Methodology

## When to use
Writing a Scope of Services (SOW) for a contractor/consultant/in-house role where every statement must be verifiable against the contract (SoW + ER).

## Workflow

### 1. Copy PDFs from OneDrive to /tmp
Terminal cp produces zero-byte placeholders. Use AppleScript:
```applescript
tell app "Finder" to set f to POSIX file "/path/to/OneDrive/Sow_p063_SoW-§13.9.pdf" as alias
tell app "Finder" to duplicate f to (POSIX file "/private/tmp" as alias) with replacing
```

### 2. Extract contract text via PyMuPDF
```python
import fitz
doc = fitz.open("/tmp/SoW_13.9.pdf")
for page in doc: print(page.get_text().strip())
```

Check sections: SoW §13.x (especially 13.3, 13.9, 13.12), ER §3.7.XIII (codes), ER §2.4D (materials).

### 3. Map each proposed task to a contract clause
| Task | Contract ref | Verdict |
|------|-------------|---------|
| Sustainability Plan | SoW §13.9 | ✅ Keep |
| Silver rating/45+ pts | None | ❌ Remove |
| Mostadam credits mgmt | ER §3.7.XIII (listed as reference only) | Rephrase to "review codes" |

### 4. Dispatch labors for cross-verification
Before finalizing, delegate to Kimi/Codex/Claude in parallel with source PDFs:
"Read these PDFs and confirm: does the contract require task X?"

### 5. Generate with SamayaDoc, deploy via AppleScript
Same as standard DOCX workflow.

## Common contract traps for sustainability SOWs
- Adding certification targets (Silver/Gold/points) — ER lists Mostadam Manual as a reference code, not a mandate
- Assigning designer tasks (energy modelling, daylight sim) to the contractor's review role
- Including CESMP, IAQ plan, waste diversion, commissioning support — not in SoW §13.9
- Referencing SBC 701/702 — only SBC 601/602 in ER §3.7.XIII
- Post-occupancy monitoring (TOC+6m) — no contract clause
- Using `§` in text — write "Section 13.9" instead (Samaya style guide rule)
- Leaving references in default black — must apply halftone style (#64748B 9pt)

## Communication Plan alignment (mandatory for coordination/reporting sections)

Read `04_Docs/02_Plans_and_Procedures/02.7_Communication_Plan/01_Source_Files/01_HTML/Aseer_Communication_Plan_RevC02_Comprehensive.html` before writing any coordination or reporting section.

**Key tables to extract:**
- Table 9 (Party Contact Matrix): Project parties, roles, signatories, primary technical contacts
- Table 13 (Report Cadence): What reports exist (MPR, WCR, DPR), originators, recipients, doc-types
- Table 31 (Document Distribution Matrix): Review/approval routing for each document type

**Routing rule:** MoC is never accessed directly. All communication routes: Samaya → CG → PMC → MoC. Any direct MoC reference in your document is wrong.

**Example (Sustainability SOW reporting section):**
- The Monthly Progress Report (MPR) per Table R-04 originates from Samaya PMO, reviewed by Samaya PD, approved by CG, distributed to PMC and MoC via Aconex Folder 07 (REP-MPR type)
- The Sustainability Plan (management plan type) routes per Table 31: Originator (Samaya PMO) → Reviewer (Samaya PD) → Approver (CG) → PMC → MoC via Aconex Folder 02 (PL type)

**Pitfall:** If you write a coordination table without checking the Communication Plan, you will invent party names, routing, or report types that contradict the project's approved document. The user will correct you. Always reference the Communication Plan by document number in the governance references section.
