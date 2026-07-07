# Aseer-Style 3-Tier Org Chart Format

This reference documents the exact org chart format the user requires for technical proposal Section 9 (Organization & Team). The user will reject simplified/adapted versions.

## Structure

### Tier Diagram (3 colored cards at top)
```
[TIER 1 — Leadership]  [TIER 2 — Specialists]  [TIER 3 — Support]
  Navy background        Sky background          Amber background
  White text             White text              White text
```

### Tier 1 — Management Table
| Column | Content | Format |
|--------|---------|--------|
| ROLE | English role title (e.g. Project Director) | Bold, 0.48rem |
| NAME | Person name (e.g. Eng. Waris Sultan) | 0.48rem |
| LOCATION | Site Office / Riyadh HO | 0.44rem, centered |
| STATUS | Active / Remote / Pending / Vacant | 0.44rem, centered |
| NOTES | الملاحظات | 0.44rem, centered |

5 columns, navy header row, alternating row backgrounds.

### Tier 2 — Specialists Table
| Column | Content | Format |
|--------|---------|--------|
| TYPE | Badge: FT (navy) / SP (sky) / INT (gray) | 0.32rem |
| SPECIALTY | Role description (e.g. Lead AV Engineer) | 0.46rem bold |
| FIRM/PERSON | Company or person name | 0.44rem |
| SCOPE | Short scope description | 0.42rem gray |

Grouped by sub-headers: Full-Time Samaya / Specialist Firms / Samaya Internal

### Tier 3 — Support Staff Table
| Column | Content | Format |
|--------|---------|--------|
| TYPE | Badge: FT (navy) / SP (sky) / INT (gray) | 0.32rem |
| ROLE | Role title | 0.46rem bold |
| PERSON | Person or "Samaya" | 0.44rem |
| NOTES | Details | 0.42rem gray |

Grouped by sub-headers: Installation & Technical / Factory & Finishing / Project Admin

## Code Pattern

Use `display:grid;grid-template-columns:1fr 1fr 1fr` for the tier diagram.
Use `<table>` with `border-collapse:collapse` and navy `<th>` headers for the tier tables.
Use inline styles throughout — do NOT use CSS classes for the org chart.

## Badge Colors
- FT (full-time Samaya): `background:var(--primary)` navy
- SP (specialist firm): `background:var(--secondary)` sky
- INT (Samaya internal): `background:var(--text-muted)` gray

## Team Sheet from KPR — Building Section 9.3 (CV Summary)

When building the "Proposed Team (continued)" CV table for a new proposal:

1. **Read the Aseer KPR Excel** at `13_Key_Personnel_Register/Aseer_Museum_Key_Personnel_Register.xlsx` — extract Key Personnel sheet rows.
2. **Map relevant roles** — keep all Tier 1 management, core specialists, and Samaya internal. Adapt role titles per project scope.
3. **Use real names from the KPR** — do NOT invent generic Arabic names (e.g. "أحمد السعيد", "خالد العتيبي"). Every role gets the actual person/firm from the Aseer KPR. This was a user correction — fabricated names will be called out.
4. **CV table columns**: Name, Role, Relevant Experience (bilingual — Arabic lead, English parenthetical).
5. **Closing note phrasing**: Present as "carefully selected for THIS project with extensive museum/exhibition experience" — do NOT say "this is the Aseer team" (user rejected this framing). Add: "Firms named (ZNA, Rawasen, Glasbau Hahn) have been approached and expressed readiness — formal contracting post-award."
6. **Reference KPR**: mention full CVs are in the project's Key Personnel Register.

### Specialist Firms — Qualified Disclosure

For specialist firms not yet formally approved for the new project:
- KEEP them named by firm — they signal quality and proven track record
- ADD a qualifying footnote: "subject to formal subcontracting post-award"
- Do NOT switch to generic role descriptions — Saudi tenders award points for named teams
- Only omit names for roles that are genuinely TBC in the source KPR
