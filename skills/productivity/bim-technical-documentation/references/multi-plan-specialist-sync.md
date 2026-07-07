# Multi-Plan Sync — Specialist Deployment Updates

When a clarification request, CG comment, or deployment review triggers specialist assignment changes, the changes must propagate consistently across multiple management plan documents. The three documents that form the "deployment triad" are:

| Document | Location (OneDrive) | Web Deploy |
|---|---|---|
| Stakeholder Management Plan (SMP) | `02.13_Stakeholder_Plan/01_Source_Files/01_HTML/` | `/build/technical-office/stakeholder-management-plan.html` |
| Project Resource Management Plan | `02.14_Project_Resource_Management_Plan/01_Source_Files/01_HTML/` | `/build/technical-office/resource-management-plan.html` |
| Key Personnel Register (KPR) | `02.14_Project_Resource_Management_Plan/04_Registers/` | N/A (Excel, not web-deployed) |

## When to Sync

Trigger events that require multi-plan updates:
- CG/PMC clarification request about specialist staffing (Engr. Elbaz / Waris emails)
- Specialist status change (CV submitted, pre-qual approved, vendor assigned)
- Client object research received that unblocks a pending specialist
- SMP revision bump that changes specialist assignment data

## Sync Workflow

### 1. Extract Changes from the Trigger

When reading a clarification request (like Waris's email about SOW §5.5), extract:
- Which positions are asked about
- Current status per project docs
- Any corrections the user provides

### 2. Update SMP First — It's the Source of Truth

The SMP has the most detailed specialist register with Tier IDs (T2-XX, T3-XX). Apply changes here first:

- Bump revision (Rev XX → Rev XX+1) in title, cover, footers, revision history
- Update the specialist row(s): firm name, status, description, Tier ID
- Add revision history entry describing what changed — data only, no internal rationale
- **Status conventions**:
  - Named firm = firm name + optional status (e.g., "Samaya-Graphic · Pre-qual pending")
  - TBD/not appointed = just "TBD" — no status suffix
  - Design split → "Design: NRS · Contractor: Samaya Factory (pending)"

### 3. Propagate to Resource Plan

The Resource Plan has parallel sections that mirror SMP specialist data:
- **Section 3 Specialist Firms table** — firm name + description per specialist
- **Section 5 Role Allocation table** — per-role commitment levels per phase
- **Section 7 Sub-Contractor Schedule** — firm names + phase timing

Apply the same changes here, using the same revision bump pattern.

### 4. Deploy Both to Web

```bash
# SMP
cp /tmp/smp.html stakeholder-management-plan.html
tar -czf deploy.tar.gz stakeholder-management-plan.html
cat deploy.tar.gz | ssh u517606786@samaya-factory.com -p 65002 \
  'cd domains/samaya-factory.com/public_html/build/technical-office/ && tar -xzf -'

# Resource Plan
cp /tmp/resource_plan.html resource-management-plan.html
tar -czf deploy.tar.gz resource-management-plan.html
cat deploy.tar.gz | ssh u517606786@samaya-factory.com -p 65002 \
  'cd domains/samaya-factory.com/public_html/build/technical-office/ && tar -xzf -'

# Fix permissions
ssh -p 65002 u517606786@samaya-factory.com \
  'chmod 644 domains/samaya-factory.com/public_html/build/technical-office/*.html'

# Verify
curl -s -o /dev/null -w "%{http_code}" \
  "https://samaya-factory.com/build/technical-office/stakeholder-management-plan.html"
curl -s -o /dev/null -w "%{http_code}" \
  "https://samaya-factory.com/build/technical-office/resource-management-plan.html"
```

### 5. Update the Draft Reply

After the plans are updated, ensure the email reply to the requester references the correct revision numbers and statuses from the updated documents.

## Common Change Patterns

| Change | SMP Update | Resource Plan Update |
|---|---|---|
| Graphics firm renamed | T2-11 firm name + status | Section 3 SP table firm name; Section 5 row label |
| Setworks fab assigned | T2-08 description (design/fab split) | Section 3 Interior Design row; Section 5 Joinery row |
| Model Maker status | T2-17 status text | Section 3 Model Maker row; Section 5 row |
| Cafe Shade split | T2-12 design/contractor split | Section 3 Cafe Terrace row; Section 5 row |
| ICT Integrator status | T2-15 status | Section 7 ICT row phase+status |
| Structural CV | T2-01 description | Section 3 Structural row |
| Accessibility | T3-08 firm assignment | Section 3 Accessibility row |

## Pitfalls

- **Desynchronized revisions** — SMP and Resource Plan can end up on different revision numbers if not bumped together. Always bump both with the same date.
- **Partial updates** — It's easy to update Section 3 of the Resource Plan but miss Section 5 (Role Allocation) or Section 7 (Sub-Contractor Schedule). Cross-reference the SMP's full specialist list against ALL Resource Plan tables.
- **Status suffix rules differ** — SMP can show "Pre-qual pending" or "CV submitted" because it's the detailed register. Resource Plan should use the simpler CG-submission conventions from §8.6.
- **OneDrive file lock** — Use `patch` for targeted edits, never `write_file` on OneDrive paths. Stage to /tmp first if full file replacement is needed, then `cp` back (which sometimes works for small files) or `ditto` if locked.
- **Deploy overwrites previous file** — The web deploy replaces the file in-place. Ensure the updated file is fully correct before deploying — there's no version rollback on the server.
