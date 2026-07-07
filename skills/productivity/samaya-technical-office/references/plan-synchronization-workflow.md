# Plan Synchronization Workflow

## When to use
An authoritative stakeholder/org document (SMP, KPR, Master Programme) has been revised and a downstream plan (RMP, Communication Plan, Risk Register, etc.) needs to reflect the new structure.

## Workflow

### 1. Extract authoritative role data
From the source document (e.g. SMP Rev 03), extract:
- **Tier classification** — which roles are Tier 1/2/3
- **Full role list** — every named role with its tier
- **Named persons** — who holds each role
- **Reporting lines** — who reports to whom

### 2. Map against target plan
For each section of the target document:
- **Org chart / hierarchy** (§3.0) — compare grid cards vs authoritative tier list
- **Role definitions** (§2.3) — update Tier 1/2/3 descriptions
- **Role schedule** (§5.2) — add missing rows, remove obsolete
- **Location matrix** (§6.1) — add missing rows
- **Risk register** (§8) — update entries that referenced old role structure
- **Cross-references** (§10) — verify all doc refs still current

### 3. Identify gap types
| Type | Example | Action |
|---|---|---|
| **Missing role** | T&C Manager not in RMP | Add grid card + role row + location row |
| **Wrong tier** | HSSE Lead in Tier 2 → should be Tier 1 (HSSE Manager) | Promote: move card, update all text refs |
| **Name mismatch** | QA/QC Manager: RMP says Ali → SMP says Abdelmohaimen | Fix name in grid card + sign-off |
| **Missing section reference** | Caption omits new Tier 1 roles | Rewrite caption with full role list |

### 4. HTML editing approach
The target plan is typically a single self-contained HTML file. Use **find-and-replace** for text changes, and **insert** for new cards/rows:

- **Grid cards** — insert a new `<div style="background:white;border:1px solid var(--accent)...">` block after the correct neighbor card
- **Role schedule rows** — insert a new `<tr style="background:#F0F9FF;">` row with `<span class="tag-new">NEW</span>`
- **Location matrix rows** — same pattern as role schedule
- **Text replacements** — use `content.replace(old, new)` for caption/description updates
- **Bulk text refs** — replace all instances of old role title (e.g. "HSSE Lead" → "HSSE Manager") across entire file

### 5. Verification checklist
- [ ] All authoritative roles present in target plan
- [ ] Tier classifications match (T1 = Key Personnel)
- [ ] Grid card count matches expected (e.g. 10 for 10 Tier 1 roles)
- [ ] Role schedule has rows for all new/promoted roles
- [ ] Location matrix has rows for all relevant roles
- [ ] All "Lead" → "Manager" upgrades done consistently
- [ ] Caption/description paragraphs reference the correct SMP version
- [ ] Risk register entries updated for role-structure changes
- [ ] QC sign-off table names match authoritative source (or flag discrepancy)
- [ ] Headcount/capacity numbers adjusted if new roles added
- [ ] Cross-reference table SMP version number correct

## Content rules when syncing personnel data into plans

- **Show names for on-board personnel** — "Pending submission" in KPR means the person IS on board. Show their name with "On board" status (or no status label). Only blank out roles that are genuinely "Vacant" or "TBC / Not yet appointed."
- **No approval-status qualifiers** — Don't add "pending MoC submission", "Overseas", or any KPR approval status next to names in plan documents. The KPR is authoritative for approval status; the plan doesn't restate it.
- **No non-project locations** — Only Riyadh and Abha appear in plans. Remove Dubai, London, Egypt, "Overseas", etc. from name annotations and location matrix notes. The matrix columns (HO Riyadh / Site Abha / Remote) are sufficient.
- **Code C → "submission in progress"** — When KPR shows "Code C — Revise and Resubmit", the plan says "submission in progress". Never write "Code C" or "revise & resubmit" in plan content.
- **One person per role card** — Each Tier 1 grid card shows exactly one role holder. Don't add sub-lines for deputies or leads under a manager's card (e.g. don't list Arch BIM Lead under BIM Manager).
- **Entity names from KPR** — Use exact KPR entity names: "Nama Consulting" (not "Nama Al Amal"), "Glasbau Hahn" (not "Glassbühne").
- **"appointed" for non-site personnel** — When someone is assigned to the project but not physically at site, use "appointed" as their status label, not "on-site". "On board" is for site-based or non-location-specific roles. "Riyadh HO" is for personnel based at the head office.
- **BIM Manager location & coordination** — Dr. Waleed is Riyadh HO based (not remote). Location matrix: HO Riyadh = ● (primary), Site Abha = ○ (visits). Description: "weekly online coordination · monthly site visits" (NOT "daily online coordination" or "monthly site presence"). Include "on-site BIM support: Eng. Ali A. Mostafa" in remarks — Ali provides site BIM coverage when Dr. Waleed isn't physically at site.
- **Follow Appendix B only for specialist packages** — Appendix B (`Subcontractors/_MANAGER_DASHBOARD/APPendix B.pdf`) is the authoritative specialist package list. Do not add roles to the plan that aren't in Appendix B, even if they appear in the KPR. If a KPR role is not in Appendix B, remove it from both the plan AND the KPR. User directive: "we follow only the Appendix B — don't add extra work that isn't required."

## Common pitfalls
- **HTML entities for &**: "T&C Manager" becomes "T&amp;C Manager" in the HTML — searches for plain `T&C` will miss it
- **Grid card uniqueness**: `<div style="background:white;border:1px solid var(--accent);">` appears once per card — when inserting, reference the **prior card's closing `</div>`** as the insertion anchor
- **QA/QC name in sign-off table**: The sign-off section (§1.4) may use a different QA/QC name than the org chart — these are distinct people (Samaya internal QA vs project QA/QC per SMP). Only fix if the user confirms both should match.
- **Number of grid cards**: A 4-column grid with 10 cards becomes 4+4+2 layout (3 rows). Verify no overflow or gap issues.
- **Cover page caption**: Must stay synced with the revision description (e.g. "Synced with Stakeholder Plan Rev 03")
