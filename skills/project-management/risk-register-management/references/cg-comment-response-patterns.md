# CG Comment Response Patterns — RMP

## Comment I — Live Registers vs Static Plan

When CG asks to attach risk registers to the RMP:

- The RMP is a **methodology document** — it defines *how* risk management works
- The registers (PRR, DDR, HSE, AV) are **live operational documents** updated weekly
- Attaching live registers to a static plan is unusual — they'd be stale by the time CG reviews
- **Correct response:** Add a note in Section 9.1: "The registers above are live operational documents maintained in the project CDE and updated weekly. They are not static appendices of this plan. A snapshot of each register as of the submission date is attached as Appendix A-D. CG may request the latest version of any register at any time."
- Do NOT embed the full live registers as static appendices — include a snapshot only

## Comment II — Quantitative Analysis Deferral

When CG says Section 7 has placeholder text:

- CG is correct — "To be recalculated" / "To be confirmed" are not actionable
- EMV needs firm BOQ cost inputs that don't exist yet in a D&B fit-out with lump-sum packages
- **Correct response:** Replace placeholders with: "Quantitative risk analysis (EMV, Monte Carlo) will be performed once the BOQ is finalised and firm cost inputs per risk are available. Until then, qualitative scoring (P x S) governs all risk assessment and response planning."

## Comment III — Scoring Scale Consistency

When CG asks to standardise scoring scales across all registers:

- **Different scales per register is acceptable per PMBOK 6th Ed Ch. 11.3** — different risk types can use different scales
- HSE follows industry-standard 5×5 (severity × likelihood)
- PRR and AV use 4×4 (appropriate for project-level risks)
- DDR uses 5-point (appropriate for design discipline risks)
- The user designed these scales intentionally — do not change them without user direction
- **Correct response options:**
  - **Push back:** State that each register uses the scale appropriate to its risk type per PMBOK. Consistency across registers is not a requirement of the standard.
  - **Compromise:** Standardise only the registers CG specifically flagged (PRR, AV) to 5×5, leave HSE and DDR as-is
  - **Comply fully:** Only if the user directs it — rescoring ~150 risks is significant effort
- **Pitfall:** Do NOT tell the user "this is wrong" when they designed the scales. The user explicitly corrected: "لما صممنا البلان فعلا كل ريجيستير ليه سكيل مختلف وانت الي قولتلي ان دا عادي" — meaning the agent originally said different scales were fine, then contradicted that when CG commented.

## Comment IV — Schedule Integration Worked Example

When CG asks to demonstrate P6 linkage:

- The RMP mentions schedule risk analysis but provides no worked example
- The risk register lacks P6 Activity ID and float columns
- **Correct response:** Add a worked example table in Section 5.1 showing: Risk ID → P6 Activity ID → WBS → Total Float → Schedule Impact. Add P6 Activity ID and Float columns to the PRR register template.

## Comment V — Middle East Shipping/Logistics Risk

When CG flags missing procurement/logistics risk:

- PRR-PRC-06 exists (imported long-lead items, FX, sole suppliers) but scores low
- Current Red Sea / Middle East shipping disruption directly affects German showcases (14-week lead), UK-sourced elements, and patinated brass from overseas
- **Correct response:** Add a new risk PRR-PRC-07 scored P=4, S=3, Score=12 (Critical). Update Section 2 (Project Risk Profile). Rescore PRR-PRC-06 to reflect current situation.

## General Rules

- **All 5 comments on ZD-0093 were valid** — no push-back items identified
- **CRS Excel format:** Two sheets — (1) CRS with 7 fields per comment (CG Comment, ER Ref, Obligation, Cost, Schedule, Action, Response), (2) Action Tracker with assignments and target dates
- **CRS Markdown companion:** Same content in repo-friendly .md format with YAML frontmatter
- **RMP Rev 01 changes:** Frontmatter → Rev 01, date → 23 Jul 2026, Section 6 → 5×5, Section 7 → deferral, Section 5.4 → P6 example, Section 2 → shipping risk, Section 13 → updated register summary, Section 9.1 → live register note
