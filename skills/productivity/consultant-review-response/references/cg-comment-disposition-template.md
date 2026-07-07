# CG Comment Disposition Table — Template

Insert as §1.5 (CG Comment Disposition) in the Document Control section of any project management plan document receiving consultant review.

## Standard Table Structure

```html
<div class="sec-banner"><b>1.5 CG Comment Disposition</b><span>response to CG review of [DOC-REF] Rev.XX ([DATE])</span></div>
<table class="eng-table">
  <thead>
    <tr>
      <th style="width:38px;">#</th>
      <th style="width:130px;">CG Comment</th>
      <th>Resolution &amp; Section Reference</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="mono">1</td><td><b>[Brief comment title]</b></td><td>&sect;X.X — how it was addressed with specific section reference.</td></tr>
    <!-- Repeat for each comment -->
  </tbody>
</table>
<div class="spec-strip" style="border-left-color: var(--accent); background: #F0FDF4;">
  <div class="spec-hdr" style="color: var(--accent);">Code [B/C] Compliance</div>
  <div style="font-size: 0.48rem; color: var(--text-muted); line-height: 1.45;">
    CG review [DOC-REF] Rev.XX returned Code [C] on [DATE] with [N] comments ([REVIEWER NAME], [ROLE]).
    All [N] are dispositioned above. This Rev CXX addresses each comment and is submitted for Code A/B approval.
  </div>
</div>
```

## Common Comment Categories (with typical resolutions)

| Category | Example CG Comment | Typical Resolution |
|----------|-------------------|-------------------|
| **Compliance** | "Provide formal compliance statement addressing all comments from REV00" | §1.5 Disposition table (this table) + reference to approved roadmap |
| **Flow sequence** | "MPR flow must be CG→PMC→MoC in sequence" | Update report recipient field to use → arrows instead of · parallel lists |
| **Stage order** | "Material submittal stage must be finalized before shop drawings" | Restructure §7.0 submission sequence flow-row |
| **Responsibility** | "SAMAYA remains contractually responsible" | §1.2 Document ID + §8 RACI with liability preservation statement |
| **Missing matrix** | "Clear detailed escalation matrix required" | §9 Escalation ladder (5 tiers, triggers, SLAs) |
| **Clarity** | "Distribution & record sequences not clear" | §11 CDE Protocol + §12.5 Distribution Protocol + §13 Phase-Gate Matrix |
| **Completeness** | "Stakeholder matrix too generic, missing specialized entities" | §3.1 with specific authorities/entities named |
| **Lifecycle** | "Plan does not specify how/when it will be reviewed as project phases transition" | §12.2 PDCA loop with quarterly KPI review, refresh trigger, lessons-learned |

## Example from Aseer Museum CRP (C01→C02)

| # | CG Comment | Resolution |
|---|-----------|-----------|
| 1 | Compliance statement + REV00 comments | §1.5 (this table) formally dispositions all 8 CG comments. Approved Project Delivery Roadmap governs submission sequence (§7.0) and distribution protocol (§12.5). |
| 2 | MPR flow CG→PMC→MoC | §5.1 R-04 recipient updated to sequential flow: Samaya PMO → CG → PMC → MoC. |
| 3 | Material submittal before shop drawings | §7.0 revised: Step 01 Design Package → Step 02 Material Submittals → Step 03 Shop Drawings → Step 04 Method Statements → Step 05 WIR → Step 06 T&C. |
| 4 | SAMAYA contractual responsibility | §1.2 lists SAMAYA as D&B Contractor. §8 RACI across 4 roles. RACI load distribution does not reduce contractual liability. |
| 5 | Escalation matrix | §9: 5-tier ladder (L1–L5) with 8 auto-fire triggers, conflict rules, 27-WD SLA. |
| 6 | Distribution & record sequences | §11 CDE Protocol + §12.5 Distribution Protocol + §13 Phase-Gate Matrix. |
| 7 | Stakeholder matrix too generic | §3.1: 6 statutory authorities listed with NOC routing. All key roles named. |
| 8 | Living document mechanism | §12.2 PDCA: quarterly KPI review, plan refresh trigger (≥1 KPI red 2 quarters), lessons-learned feedback. |
