---
name: cg-warning-reply-letter
title: CG/Ministry Warning-Letter Reply — Samaya Projects
description: Reply to formal CG/PMC/Ministry warning letters, delay notices, and breach notifications on Samaya projects — strategy levels, claim verification (three-source rule), evidence chains, and official HTML letter styling.
---

# CG/Ministry Warning-Letter Reply — Samaya Projects

Class of work: drafting formal replies to consultant (CG) / PMC / Ministry warning letters, delay notifications, or breach notices. Proven on Aseer Museum LT-08.02 / LT-0010 (Sep-2026).

## When this triggers
- A warning/إنذار letter arrives from CG, PMC, or a Ministry office citing contractor delay or breach.
- The reply requires factual rebuttal, contractual citations, and escalation decisions.

## 1. Choose the strategy level WITH the PM first

| Level | Posture | When |
|---|---|---|
| **A — Reply to consultant (soft)** | Acknowledge + corrective plan + reserved rights | Warning procedurally valid |
| **B — Escalate to Ministry/Owner** | Address the Employer-side PM; challenge consultant's authority + facts; request owner intervention | Warning procedurally defective |

Level B (the LT-0010 pattern — stronger): procedural challenge first (no contract article cited, no reference programme, issued same-day without right of reply, representative authority per Art. 3/Sec. 3 + Art. 18 + Art. 1(f)), then factual chronology table, then quantified counters (e.g. design weight in price schedule vs claimed progress %), then numbered asks to the Ministry, then full reservation of rights. CEO-signed for weight.

## 2. Verify EVERY claim — three-source rule (CRITICAL)

Never write a date, code, or doc number into the letter without checking ALL available sources. If sources conflict, resolve BEFORE sending:

1. **Contract text** (`00_Project_Charter/contract.md`): every article cited. PITFALL: this file is OCR'd Arabic with reversed character order and disconnected letters (صالحات not صلاحيات) — grep with OCR-tolerant patterns or locate the parallel English text. PITFALL: DUPLICATE article numbers across sections exist (two "Article Eighteen" — Waiver of Rights AND Partial Withdrawal) — confirm which section.
2. **Aconex export** → query `08_Document_Index/submission.db` (latest-revision-wins per AGENTS rule 10a). Col 11 = submitted date, col 12 = last-update timestamp (= CG response date).
3. **Outlook SQLite**: direct letters (LT-xxxx) NEVER appear on Aconex — they are email/paper. Query the `Mail` table (Message_NormalizedSubject, Message_TimeSent, Message_DisplayTo, Message_Preview). Timestamps are plain unix — `datetime.fromtimestamp(raw)` works; do NOT add epoch offsets blindly.
4. **Registers**: letters_register + risk_register distinguish formal submission vs revised copy dates (e.g. LT-0007 formally submitted 11-Aug per risk register + original Outlook email 09:39 AM; 13/14-Aug was the revised/signed copy).

## 3. PM standing rules for these letters

- **Never restructure the PM's/received draft** — it is the vehicle. Additions go in as clearly-marked proposed additions; content edits only after discussion and explicit approval.
- Arabic replies for Arabic letters; natural engineer language, no AI/template phrasing.
- No monetary values in the body when the point is fact-statement — "records held, shown upon request" keeps the value internal for EOT/VO while preserving the implicit threat.
- Remove details irrelevant to the recipient (internal cost studies, pricing mechanics) — the Ministry cares about contract facts.
- Rebut misleading claims by reframing single incidents as a **pattern of conduct** (e.g. "وهذا النمط في التعامل — إعادة التقديمات النشطة للتعديل بتوسيع نطاقها، في الوقت الذي يُتَّهم فيه المقاول بالتأخر في التعاقد...").
- Scope-expansion rebuttal formula: "no contractual reason the designer must be the supplier — and the condition was imposed during the design stage, a gratuitous expansion at the wrong time."

## 4. Evidence-chain narrative (the winning pattern)

Build the chain from Aconex + Outlook + meeting minutes, then narrate linearly. Model (disproved "did not contract a landscape specialist"):
PQ approval (Code B, dated) → kick-off meeting with consultant personally invited (calendar invite from Outlook) → SOW submitted on Aconex ONE DAY BEFORE the warning letter → consultant returned Code C with scope expansion (dated) → design review meeting with CG present → milestone granted.
Key moves: "the consultant was personally invited" kills denial of knowledge; "one day before his own letter" turns their evidence into yours; close with "the contract is in place, meetings held, consultant present, SOW submitted — what blocked closure was their expansion demand, not any contractor default."

## 5. Official HTML letter styling (Samaya)

- Copy the style block **VERBATIM** from `03_Plans/02_Stakeholder/MOC-ASEER-SIC-1K0-PL-0020_Rev04_Stakeholder_Management_Plan.html` (fonts link + :root vars + .page pattern). Do NOT hand-write CSS approximations — the PM rejects them.
- Arabic body: `text-align: right`, NOT justify (justified Arabic creates whitespace "rivers").
- Fonts: Inter + Montserrat + IBM Plex Sans Arabic (same Google Fonts link as the Stakeholder Plan).
- Pagination: one flowing document + `@page { size: A4; margin: ... }` with header/footer via @page margin boxes; `table { break-inside: avoid }`; `h2 { break-after: avoid }`. Do NOT hard-split into fixed .page divs (causes overflow + cut tables).
- Header meta block: ONE solid bordered block (ref+date row / addressee bold / cc muted / project+subject). No blank `[__]` fields at publish time.
- End with 5-logo strip (Client MoC / PMC / CG / NRS / Samaya) + doc-control block.
- PITFALL: converting DOCX→HTML can leave BOTH styled and raw docx-paragraph versions of the header in the page — the raw one renders below and looks broken. Remove duplicates.
- Deploy to surge for live review; readers need Ctrl+Shift+R to bust cache.

## 6. Process rules

- Re-verify draft numbers against fresh data (session caught: "135 submissions" stale → actual 800+; "21 events" → 20 rows; hijri month wrong 03→04; contract number missing a digit 10003521→0010003521).
- Sep-2026 = Rabi' al-Akhir 1448 (month 04).
- If a date/claim can't be verified: remove it or soften to an internal reservation — never guess into a legal letter.
- File everything: discussion file + letters_register row + action items + GitHub issue; publish live draft to surge; commit + push after each change.

## References
- `references/cg-warning-reply-letter-pattern.md` — condensed session detail: verification recipes, OCR contract pitfalls, evidence-chain examples.