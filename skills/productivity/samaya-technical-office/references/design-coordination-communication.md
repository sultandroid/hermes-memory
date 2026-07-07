# Design Coordination Communication

## When to use

A design subcontractor (NRS, ZNA, etc.) issues a design direction / RFI / coordination note about a specific area or system. You need to:

- Understand the instruction
- Identify all affected parties (subcontractors, consultants, internal teams)
- Trace their contact information from project documents
- Draft and distribute a clear action email
- Track the instruction through to submittal/inspection

## Source documents for contact tracing

| Document type | Where to find | What it gives you |
|---|---|---|
| **Email archive (EML files)** | `Email_Archive/_attachments/` | To/CC/From headers with full names and email addresses |
| **Stakeholder map** | `Scripts/notes/stakeholders.md` | Organization → person mapping, roles, domains |
| **Subcontractor scope docs** | `Subcontractors/<Package>/00_Scope_of_Work/` | Subcontractor company name, registered address, contact person |
| **Proposals / fee docs** | Same subcontractor scope folder or `Contracts/<Party>/02_Proposals_and_Quotes/` | Direct contact details of subcontractor principals |
| **Email intel notes** | `Scripts/notes/email_intel_30d.md` | Recent email threads showing who communicates about what |
| **Project memory** | `Scripts/PROJECT_MEMORY.md` | Organizational structure, key personnel, domain conventions |

## Email address discovery

When a party's direct email is not immediately visible:

1. **Check naming conventions** — most organizations follow patterns:
   - `samayainvest.com`: `firstname@samayainvest.com` or `firstname.lastname@samayainvest.com`
   - `nissenrichardsstudio.com`: `firstname.lastinitial@nissenrichardsstudio.com` (e.g., `jim.r@`, `francesco.b@`)
   - `ace-mb.com`: `firstname.lastname@ace-mb.com`
   - `cg.com.sa`: initial-based or full name

2. **Search email archive** for the person's name or company domain:
   ```bash
   grep -r "person@\|company\.com" Email_Archive/_attachments/*.eml
   ```

3. **Check scope documents and proposals** — subcontractor fee proposals and scopes of work often list the principal's direct contact info.

4. **When you can't find a direct email**, note it as "routed via <Samaya contact>" — the Samaya-side project manager or procurement lead is the authorized intermediary. Do not guess.

## Draft the communication

Structure of the coordination email:

### Subject line
```
[Project] — [Designer] Direction: [Area/Room] — [Subject]
```
Example: `Aseer Museum — NRS Direction: G11 Scripts & G13 CAC — Black Fixture Finish`

### Body

| Section | Content |
|---|---|
| **Reference** | "Please see attached direction from [Designer] received [date]" |
| **The instruction** | Plain-language statement of what needs to happen |
| **Affected parties table** | Who needs to do what — one row per party |
| **Action required** | "Please confirm receipt and update your deliverables by [date]" |

Affected parties table format:
```
| Party | Action |
|---|---|
| [Subcontractor A] | [Specific deliverable change] |
| [Subcontractor B] | [Specific deliverable change] |
| Internal team X | [Tracking/coordination action] |
```

### Recipient assignment

| Role | Placement |
|---|---|
| Subcontractor PM/lead | TO |
| Samaya internal team leads | TO |
| Designer (for visibility) | CC |
| Project Director | CC |
| PMC (if needed) | CC |

## After sending

1. **File the instruction** in `Correspondence/` with a descriptive filename
2. **Tag related submittals** — any submittal for the affected area gets a standing comment about the design direction
3. **Update the submittal register** if one exists — add a note under the relevant package

## Pitfalls

- **Do not send design directions directly to external parties** if the contract channels communication through Samaya. Studio ZNA, for example, is contacted via Mohammed Hakami (m.hakami@samayainvest.com).
- **The CC list should not exceed 8-10 people** — group emails lose accountability. If in doubt, put the decision-maker in TO and the observers in CC.
- **Some email domains follow non-obvious patterns** — NRS uses `firstname.lastinitial@` (e.g., `joshua.b@`, `robin.k@`). If a new NRS person appears in a CC list, apply the same pattern.
- **Gianluca Vartan** at NRS follows the pattern `gianluca.v@nissenrichardsstudio.com` (confirmed by CC list on 28 May 2026 email).
