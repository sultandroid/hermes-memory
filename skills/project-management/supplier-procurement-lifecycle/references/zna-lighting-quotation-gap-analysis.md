# Worked Example — ZNA Lighting Designer Quotation Gap Analysis

**Context:** Studio ZNA (London) sent a fee proposal and scope for lighting design consultancy at Aseer Museum. Samaya had already prepared Rev 01 of the SOW (closing gaps in ZNA's original 01-Jun scope). The quotation arrived via Mohammed Hakami on 14-Jun-2026.

**Project Docs:** `Aseer-Museum/Subcontractors/02_Lighting_Designer/`

---

## Discovery Flow

1. **Find yesterday's email** — SQL query on Outlook joining `Mail` + `folders`, filtered by `date(..., 'localtime') = '2026-06-14'` and subject containing "Lighting" or sender "Hakami"
2. **Extract attachments** — AppleScript `message id` loop with `touch`-before-`save` pattern → 6 files (2 PDFs + 1 JPG per email)
3. **Read PDFs** — `pdftotext` on fee proposal, scope of works, and payment schedule
4. **Read project baseline** — ER extract, SOW extract (§6.22.3, §8.8), DMP reference, Samaya Rev01 SOW
5. **Build gap matrix** — compare each ZNA scope item against project requirements

---

## Gap Matrix Structure

| Requirement | Source | ZNA Covers? | Gap |
|---|---|---|---|
| [Specific deliverable] | SOW §X.X | ✅ Yes / ❌ No / ⚠️ Partial | [What's missing] |

**Severity:**
- 🔴 **CRITICAL** — Missing mandatory scope that blocks contract (e.g., site focusing mandated by SOW §8.8)
- 🟠 **HIGH** — Missing major deliverable class (Stage 6 handover, BIM)
- 🟡 **MODERATE** — Missing detail or insufficient specificity (conservation dose, UV/IR numeric spec)
- 🟢 **LOW** — Minor omission (O&M data, spares schedule)

---

## Key Findings from This Session

1. **Scope creep in the gap-closed SOW** — Samaya's Rev 01 SOW added 8+ deliverables (lux-hour dose, UV/IR spec, BIM/LOD, daylight study, O&M data, conservation dataset, site focusing, Stage 6). ZNA's £21,227 was based on their original scope, not ours. The fee needs re-baselining.

2. **Stage 5 listed as OPTIONAL** — SOW §8.8 says "final light balancing and focusing by lighting specialist consultant" as mandatory. ZNA listed Stage 5 (shop drawing review) as optional and didn't include site focusing at all.

3. **Stage 6 completely absent** — as-built verification, commissioning witness, POE, DLP are all missing. SOW §11 and ER §2.7 require them.

4. **No BIM commitment** — project BEP requires authored model at LOD 300 + TIDP. ZNA only offers PDF/DWG.

---

## Recommended Reply Structure

1. Acknowledge receipt
2. Summarise scope gaps (use the matrix table)
3. Request ZNA to:
   - Confirm Stage 5 as FIRM + add site focusing direction as quoted line
   - Add Stage 6 (as-built, commissioning witness, aftercare)
   - Add BIM authoring at LOD 300 per project BEP
   - Add conservation deliverables (lux-hour dose, UV/IR spec, conservation data-set)
   - Add O&M data + 1-year spares schedule
   - Provide revised fee reflecting the full scope
   - Confirm controls boundary and emergency authority interface
4. Indicate intent to proceed to contract once revised proposal aligns with project requirements

---

## Pitfalls

- ZNA's scope (01-Jun) predates Samaya's Rev 01 SOW (05-Jun). Always check the chronology — you may be comparing against a refined scope the subcontractor hasn't seen.
- Payment milestones in the quote may not match project submittal register stages (50/90/100/IFC). Flag the mismatch early.
- Controls boundary exclusion ("strategy only") may be correct per the interface matrix, but needs explicit acceptance so the MEP/EBMS integrator knows they own detailed engineering.
- Civil Defence emergency lighting ownership is a gap ZNA won't fill without being told. Default: Designer produces approvable design, D&B Contractor lodges.
