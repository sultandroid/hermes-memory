# RMP-Specific CG Comment Response Patterns

## When CG Returns Code C on the Risk Management Plan

The RMP is a methodology document, not a data container. CG comments on the RMP typically fall into 5 categories:

| Comment | Valid? | Response Strategy |
|---------|--------|-------------------|
| Registers not attached | Valid | Add note: live registers in CDE, snapshot attached as appendix |
| Section 7 placeholders | Valid | Replace with deferral statement until BOQ finalised |
| Scoring scale inconsistency | **Push back** | User designed scales intentionally per PMBOK Ch. 11.3 — different risk types may use different scales. Document clearly in Section 6.5, no rescoring needed. |
| Schedule integration not shown | **Push back** | Plan is methodology, not a data register. P6 IDs and float values are operational data in the live PRR register. Add note confirming PRR entries include these columns. |
| Missing shipping/logistics risk | **Push back** | Risk factor belongs in Section 2 (Project Risk Profile) as a general reference. The detailed risk entry (PRR-PRC-07) with scoring and response plan belongs in the live PRR register. |

## Key Distinction: RMP vs Registers

- **RMP** = methodology (how risk management works)
- **Registers (PRR, DDR, HSE, AV)** = live operational data (what the risks are)
- CG often conflates them — the RMP should stand on its own as a methodology document
- Attach register snapshots as appendices, not the full live registers
- **When CG asks for operational data in a plan, push back** — the plan is methodology, the register has the data. This applies to: risk scores, P6 Activity IDs, float values, specific risk entries, and any other data that changes weekly.

## Scoring Scale Push-Back Pattern

CG may demand all registers use the same scoring scale (e.g., "standardise to 5x5"). **This is not a contractual requirement.** Per PMBOK 6th Ed Ch. 11.3, different risk types may use different scales appropriate to their nature.

| Register | Scale | Rationale |
|----------|-------|-----------|
| PRR (Master) | PxS 1-4 (max 16) | Project-level -- standard for commercial, programme, design, construction risks |
| DDR (Design) | PxI 1-5 (max 25) | 5-point impact scale for design-phase technical risks |
| HSE Register | CxL 1-5 (max 25) | Industry-standard 5x5 severity x likelihood |
| AV Register | PxS 1-4 (max 16) | Project-level -- consistent with PRR |

### Response to CG

> "Per PMBOK 6th Ed Ch. 11.3, different risk types may use different scales appropriate to their nature. The RMP methodology presents a unified reference framework in Section 6. Each register retains the scale most appropriate to its risk type -- HSE uses 5x5 (industry standard), PRR and AV use 4x4 (project-level PxS), DDR uses 5-point impact (design risks). All scales are clearly documented and cross-referenced in the RMP."

### Pitfall -- Don't Over-Comply

When the user designed the RMP with your guidance, you validated the approach (different scales per register is fine per PMBOK). When CG challenges it, **defend the original design decision** -- don't immediately change the plan to comply. The user will correct you if you flip positions. The correct response is:

1. Acknowledge CG's preference for consistency
2. Explain the PMBOK basis for per-register scales
3. Offer to document the scales more clearly (not change them)
4. No rescoring of existing risks required

## Live Registers Note Pattern

When CG asks for registers to be attached to the RMP, add this note in Section 9.1:

> **Note on live registers:** The registers above are live operational documents maintained in the project CDE and updated weekly. They are not static appendices of this plan. A snapshot of each register as of the submission date is attached as **Appendix A (PRR)**, **Appendix B (DDR)**, **Appendix C (HSE Register)**, and **Appendix D (AV Register)**. CG may request the latest version of any register at any time.

This satisfies CG's need to verify without turning the RMP into a static container for constantly-changing data.

## CRS Format for RMP

Two deliverables:
1. **CRS Excel** — Use the approved CG format (same layout as ZD-0086 CRS): header block (project name, CRS number, doc ref, title), legend (A/B/C/D codes), table (No. | Initial | Section | Code | Reviewer Comment | Originator Reply | Reply By | Status), signature block (SC / PMCM / MOC / Originator).
2. **CRS Markdown** — same content in repo-friendly .md with YAML frontmatter.

### Approved CRS Excel Template Structure

The CG-approved CRS format (from ZD-0086) has this exact layout:

| Section | Content | Notes |
|---------|---------|-------|
| **Row 1** | `MOC_HQ DESIGN & BUILD (FIT-OUT)` | Project header, navy text |
| **Row 2** | `COMMENTS RESOLUTION SHEET (CRS)` | Title, 16pt bold |
| **Row 4** | PROJECT NAME: [full project name] | Merged A-H |
| **Row 5** | CRS NUMBER: [ref] / Rev / DATE / DISCIPLINE | Merged A-H |
| **Row 6** | DOCUMENT No.: [ref] / Rev / DISCIPLINE | Merged A-H |
| **Row 7** | DOCUMENT TITLE: [title] / DOCUMENT TYPE | Merged A-H |
| **Row 8-9** | Legend: A=Approved, B=Approved With Comments, C=Revise and Resubmit, D=Rejected | Navy header cells |
| **Row 10** | Table header: No. | Initial | Section/Ref. | Code | Reviewer Comment | Originator Reply | Reply By | Status | Navy fill, white text |
| **Row 11+** | Comment rows | Each row: number, reviewer initials, section ref, code (C in red), comment, reply, reply by, status (Closed in green) |
| **After table** | Review Status Code legend | Merged A-H |
| **Signature block** | SC / PMCM / MOC / Originator columns | Name, Position, Signature, Date rows |
| **Disclaimer** | "*Approval status from the Reviewer shall be deemed as permission to proceed..." | Italic, 7pt |

**Key formatting rules:**
- 8 columns (A-H), widths: 5, 8, 12, 8, 45, 45, 15, 10
- Code C cell: red fill (`#B01E2F`), white bold text
- Status Closed: green fill (`#C6EFCE`), green text
- All cells: thin black borders, Calibri 9pt body, 10pt bold headers
- Row height: ~90 for comment rows (wrap text)
- Write values to cells BEFORE merging — MergedCell objects are read-only

### Pitfall — No Placeholders in Formal Submissions

**Never submit a plan with "To be recalculated", "To be confirmed", or any other placeholder text.** CG will flag it as incomplete. Either:
- Include real data, or
- Remove the section entirely and state clearly that it will be completed when inputs are available

The user explicitly corrected this: "ليه حطيتهم من الأول" — placeholders in a CG submission are worse than omitting the section. They signal the document was submitted before it was ready.

### CRS Classification Rules

| Classification | When | Colour |
|----------------|------|--------|
| **Comply** | CG comment is valid — contractual obligation, no cost/schedule impact | Green |
| **Justify** | CG comment is not valid — plan is methodology, register has the data; or per PMBOK different scales are acceptable | Amber |

### CRS Response Framing for RMP

- **Comment I (Registers):** "Noted. The registers are live operational documents maintained in the project CDE and updated weekly. A snapshot of each register as of the submission date is attached as Appendix A-D. CG may request the latest version at any time."
- **Comment II (Section 7):** "Noted. Section 7.3 revised. Quantitative analysis will follow once BOQ is finalised. Qualitative scoring governs until then."
- **Comment III (Scoring):** "Noted. Per PMBOK 6th Ed Ch. 11.3, different risk types may use different scales appropriate to their nature. Section 6.5 added documenting each register's scale and rationale. No rescoring required."
- **Comment IV (Schedule):** "Noted. The RMP describes the schedule-risk integration methodology in Section 5.1. Actual P6 IDs and float values are maintained in the live PRR register, updated weekly and available for CG review upon request."
- **Comment V (Shipping):** "Noted. The RMP identifies 'Middle East Shipping Disruption' as a Critical risk factor in Section 2. The detailed risk entry (PRR-PRC-07) with full scoring and response plan has been added to the live PRR register."

## Section 6.5 — Register-Specific Scoring Table

Add this table to the RMP when CG challenges scoring consistency:

> Per PMBOK 6th Ed Ch. 11.3, different risk types may use different scales appropriate to their nature. Each register uses the scale most suitable for its risk type:

| Register | Scale | Max Score | Rationale |
|----------|-------|-----------|-----------|
| Master Risk Register (PRR) | P x S 1-4 | 16 | Project-level PxS — standard for commercial, programme, design, and construction risks |
| Design Discipline Risk Register (DDR) | P x I 1-5 | 25 | 5-point impact scale for design-phase technical risks |
| HSE Risk Register | C x L 1-5 | 25 | Industry-standard 5x5 severity x likelihood for HSE risks |
| AV Risk Register | P x S 1-4 | 16 | Project-level PxS — consistent with PRR for AV-specific risks |

> All scales are clearly documented in their respective registers and cross-referenced in this plan. The scoring approach is consistent within each register, enabling reliable risk prioritisation and trend analysis.
