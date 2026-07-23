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
1. **CRS Excel** — 2 sheets: CRS (7 fields per comment) + Action Tracker
2. **CRS Markdown** — same content in repo-friendly .md with YAML frontmatter

See `risk-register-management` skill → `references/cg-comment-response-patterns.md` for the full worked example.
