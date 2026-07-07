# Cross-Subcontractor Conflict Audit Workflow

## When to use

When a new RFP, SOW, or scope document is created for one subcontractor and needs to be checked against all other subcontractors for:
- Scope overlaps (same work described in two contracts)
- Interface gaps (work that falls between two scopes)
- Contradictions (conflicting requirements, incompatible materials)
- Missing coordination (services that penetrate each other's scope)

## Workflow

### Step 1: Identify affected subcontractors

From the new RFP/SOW, extract:
- Physical scope (ceilings, walls, floors, MEP, AV, etc.)
- Materials and products specified
- Performance targets (NRC, fire rating, STC)
- Installation methods (spray, trowel, suspend, mount)

Map to all subcontractors whose scope touches the same physical areas:

| Subcontractor | Why check |
|--------------|-----------|
| MEP Contractor | Ductwork, sprinklers, diffusers in same ceiling void |
| MEP Designer | Noise criteria, silencer specs |
| Lighting Designer | Fixtures in ceilings |
| AV/IT Contractor | Speakers, projectors in ceilings |
| FLS Specialist | PAVA speakers, fire detectors in ceilings |
| Structural Contractor | Suspension anchors, loading |
| Rigging Contractor | Ceiling suspension points |
| Showcases Contractor | Floor-to-ceiling case interfaces |
| CITC/BMS-ICT | WAPs, sensors in ceilings |
| Exhibition Fit-Out | Wall-ceiling junctions |

### Step 2: Read each subcontractor's scope documents

For each affected subcontractor, read:
1. `SCOPE_REQUEST.md` or `SOW` in `_MANAGER_DASHBOARD/`
2. `SPEC.md` in `_MANAGER_DASHBOARD/`
3. Any existing submittal register or status report
4. Returned submittals in `05_Returned_Submittals/`

### Step 3: Identify conflicts per category

| Category | What to look for |
|----------|-----------------|
| **Scope overlap** | Both subs claim the same work (e.g., both include baffle suspension) |
| **Interface gap** | Neither sub covers a required interface (e.g., duct silencers not in any scope) |
| **Physical conflict** | One sub's work prevents another's (e.g., speakers in fabric ceiling) |
| **Performance contradiction** | One sub's target conflicts with another's (e.g., NR 30 vs noisy HVAC) |
| **Timing risk** | One sub's deliverable depends on another's input (e.g., acoustic specialist not appointed before MEP 50% gate) |
| **Undefined term** | Scope language is ambiguous (e.g., "integrated lighting" without definition) |

### Step 4: Structure the conflict report

```markdown
# [RFP/SOW Name] — Cross-Subcontractor Conflict Audit

**Audit Date:** YYYY-MM-DD
**RFP Reference:** [RFP-XXX-XXX]
**Scope:** [brief description]

## Executive Summary

[N] conflicts identified across [N] subcontractor packages.
- **High severity:** [N]
- **Medium severity:** [N]
- **Low severity:** [N]

## Conflict Register

### C-01 | [Subcontractor Name] — [Issue Title]
| Field | Detail |
|-------|--------|
| **Subcontractor** | [NN_Subcontractor_Name] |
| **Issue** | [Description of the conflict, including what each sub's scope says] |
| **Severity** | [High/Medium/Low] — [why this matters] |
| **Recommended Resolution** | [Specific action to resolve, with party assignments] |

### C-02 | ...

## Summary Matrix

| ID | Subcontractor | Issue | Severity |
|----|--------------|-------|----------|
| C-01 | [Name] | [Short description] | [High/Medium/Low] |

## Recommended Immediate Actions

| # | Action | Party | Deadline |
|---|--------|-------|----------|
| 1 | [Action] | [Party] | [Date] |
```

### Step 5: Save and report

1. Save the conflict audit to the originating subcontractor's `_MANAGER_DASHBOARD/` as `[SCOPE]_CONFLICT_AUDIT.md`
2. Report findings to the user with a compact summary table
3. Flag the top 3-5 high-severity items that need immediate resolution before RFP award

## Example: Acoustic Ceiling RFP Conflict Audit

See `ACOUSTIC_CEILING_CONFLICT_AUDIT.md` in `18_Acoustic_Specialist/_MANAGER_DASHBOARD/` for a worked example with 12 conflicts across 7 subcontractors.

## Common high-severity patterns

| Pattern | Example | Resolution |
|---------|---------|------------|
| **Missing silencers** | NR 30 target but no duct silencers in MEP BoQ | Add silencer line items; coordinate with acoustic specialist |
| **Unmountable devices** | PAVA speakers in fabric/soft ceilings | Provide solid mounting plates or relocate |
| **Undefined scope split** | Baffle suspension anchors — who provides? | Clarify: acoustic = fixing schedule, structural = slab anchors |
| **No ceiling void** | Spray-on acoustic applied directly to soffit | Route MEP services below treatment or embed before spray |
| **Uncoordinated penetrations** | 51 speakers need cut-outs in acoustic ceiling | Add integration drawings to RFP D4 deliverable |
