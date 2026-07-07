# Subcontractor/Consultant Appointment Review

Review a subcontractor/consultant's response to a CG-approved Scope of Work, evaluate their fee proposal against CG requirements, and produce a negotiation position.

## Trigger

CG approves a SOW with Code B (Approved with Comments). The subcontractor/consultant submits a fee proposal and reply. User asks to "check the reply" or "review their proposal".

## Workflow

### 1. Map the Thread

Find the relevant email thread. The pattern is usually:
1. **Sultan/PM → internal coordinator**: instruction to send documents and initiate appointment
2. **Coordinator → subcontractor**: sends CG-approved SOW, requests draft contract
3. **Subcontractor → coordinator**: acknowledges receipt
4. **Subcontractor → coordinator**: substantive reply with comments, counter-proposal, attachments

**Check attachments** — Outlook's `Message_HasAttachment=1` flags inline images (signatures, screenshots) as attachments. First list what's actually attached before assuming documents are there:
```applescript
set atts to (every attachment of theMsg)
repeat with att in atts
    set attName to name of att
    set attType to content type of att
end repeat
```

### 2. Locate the Contract Drafting Folder

Subcontractor/consultant folders live under:
```
.../Subcontractors/{NN}_{Discipline_Name}/
```

The contract drafting subfolder is `08_Contract_Drafting/` containing:
- `Aseer 2026 FEE PAYMENT SCHEDULE_*_StudioZNA.pdf` — their payment schedule
- `Aseer 2026 FEE PROP_*_StudioZNA.pdf` — full fee proposal
- `MOC-MUS-ASE-XXXX-ZD-00XX_reply.pdf` — CG Code B response
- `Lighting_Submittal_Register.xlsx` — deliverables register
- Supporting docs (DMP, CG responses, etc.)

**Pitfall:** The folder may not exist yet if the appointment is new. Check the parent subcontractor folder for existing structure.

### 3. Collect Three Sources of Truth

| Source | Document | What It Contains |
|--------|----------|-----------------|
| **CG's requirements** | CG Code B response (ZD-00XX_reply.pdf) | CG comments on the SOW. Each comment is a contractual requirement the subcontractor must comply with. |
| **Subcontractor's proposal** | Fee proposal PDF | Their proposed scope, fees, payment schedule, T&Cs, day rates, exclusions |
| **Subcontractor's reply** | Latest email in thread | Their acceptance/objection to each point, counter-proposal, scope clarifications |

### 4. Build a CG Compliance Cross-Reference

For each CG comment, check across all three sources:

| # | CG Comment / Requirement | In Sub's Proposal? | In Sub's Reply? | Verdict | Action |
|---|--------------------------|--------------------|-----------------|---------|--------|
| 1 | Requirement text | ✅ Covered / ⚠️ Partial / ❌ Missing | ✅ Accepted / ❌ Rejected / ⚠️ Conditional | **Gap** / **Compliant** / **Needs negotiation** | What to do |

**Common gap patterns (recurring with lighting/specialist consultants):**

| CG Requirement | Typical Subcontractor Pushback | Verdict |
|----------------|-------------------------------|---------|
| Exit signage / emergency lighting | "Not in our scope" | ❌ Gap — push back or reassign to MEP |
| Showcase lighting design | "Coordination only" | ❌ Gap — CG requires full design |
| Elevations & sections on lighting plans | "Won't issue" | ❌ Gap — standard design deliverable |
| Dated action plan | "Need a programme from you" | ⚠️ Conditional — provide programme then demand action plan |
| Attend meetings / site visits | "Not costed" / "Optional" | ❌ Gap — CG requires attendance; must be in base fee |
| RCP coordination with other services | "Not our scope" | ❌ Gap — coordination is a standard consultant duty |
| Cabling information | "That's M&E scope" | ⚠️ Ambiguous — clarify scope boundary with M&E contractor |
| Lighting control engineering | "Strategy only" | ❌ Gap — CG rejected this limitation in comment |
| Samples & mock-ups list | "Will issue in spec at 100%" | ⚠️ Partial — acceptable timeline but confirm scope |

### 5. Evaluate the Payment Schedule

Compare their proposed schedule against your counter-proposal:

| Milestone | Sub's Proposal | Your Proposal | Delta |
|-----------|---------------|---------------|-------|
| Mobilisation | X% | X% | +0% / -X% |
| 50% | X% | X% | Front-loaded? |
| 90% | X% | X% | Check cumulative |
| 100% | X% | X% | Retention? |
| IFC/AFC | Optional: £X | X% | Optional = price risk |
| Stage 6 / Final | Not costed | X% | Must define or exclude |

**Red flags:**
- Front-loaded payment schedules (>50% before 90% delivery)
- Optional stages that CG will require (IFC/AFC, site supervision)
- Exclusions that contradict CG comments
- 15-day payment terms with work stoppage threat
- Withholding tax exclusion (check if it's included in their base or on top)

### 6. Evaluate Day Rates (for future variations)

If the proposal includes day rates:

| Role | Rate | Market Benchmark | Verdict |
|------|------|------------------|---------|
| Director | £1,200/day | High for KSA projects | Negotiate |
| Senior Designer | £725/day | Reasonable | Accept |
| Technician | £650/day | Above market | Negotiate |

**Note:** London-based consultants charge higher rates. Factor in whether they have KSA presence.

### 7. Produce the Negotiation Summary

Format:

```
## Appointment Review — [Company Name] — [Role]

**Reference:** MOC-MUS-ASE-XXXX-ZD-00XX (Code B, DD-Mon-YYYY)
**Base Fee:** £XX,XXX (Stage X)
**Optional:** £XX,XXX (Stage X — TBC)

### ✅ Scope Items — Compliant
[Table of items where sub agrees with CG]

### ❌ Gaps to Resolve Before Appointment
[#|CG Requirement|Sub's Position|Risk|Action]

### 💰 Payment Schedule — Counter-Needed
[Table comparing proposals]

### 📋 Next Steps
[Ordered actions, who does what]
```

### 8. Note Leave / Availability

Check the contact person's availability. If they're on leave, set expectations on response timing.

## Pitfalls

- **Inline images show as attachments** — Outlook flags signature logos and screenshots as `Message_HasAttachment=1`. Always list what's attached before extracting.
- **PDF text extraction from bilingual docs** — Arabic/English PDFs may produce jumbled text with `pdftotext`. Search for English keywords (comments, scope, code) rather than trying to read line-by-line.
- **OneDrive locks** — If the contract drafting folder is on OneDrive (`Library/CloudStorage/OneDrive-*/`), locked files cause `EDEADLK`. Read with `pdftotext` since PDFs are usually cached locally.
- **Fee amounts may have typos** — ZNA's proposal said "twenty two thousand, two hundred and twenty seven" but the numeric figure was £21,227. Always verify text vs numbers.
- **Payment schedules may not match the email reply** — The PDF may be their original proposal while the email contains their counter. Always compare both.
- **Baseline = submitted/CG-approved scope, NOT internal revisions** — The user will be frustrated if you compare the subcontractor's proposal against an internal enhanced SOW that was never submitted to CG. Always use the SOW that CG approved (even if Code B with comments) as the gap-analysis baseline. Internal revisions that were never sent are not the contractual baseline.
- **Designer vs Installer split is not a gap** — If a designer says "design only" and an installation contractor exists, the split is correct. Only flag as a gap if BOTH parties exclude the item or if BOTH point at each other.
- **Stage 5 (IFC/AFC) as optional at 50% of design fee is excessive** — The actual effort is a watching brief: review shop drawings, respond to RFIs, witness mock-ups. No new design production. Push back to include it in the base fee or negotiate down to 10-15% of design fee.
- **When the user asks "what efforts will they do in Stage 5?" — give a concrete activity list** — Not percentages or abstract descriptions. List the actual tasks: review shop drawings, respond to RFIs, review substitutions, attend mock-up, witness commissioning.
