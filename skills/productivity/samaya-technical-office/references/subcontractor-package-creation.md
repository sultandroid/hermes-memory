# Subcontractor Package Creation

## When to use

A new specialist trade/subcontractor needs to be added to the Aseer Museum project. This covers creating the folder structure, authoring scope of work, and updating the project register.

## Step-by-step

### 1. Determine the next package number

Check the existing folders in `Subcontractors/`:

```bash
ls -d /path/to/Aseer-Museum/Subcontractors/[0-9][0-9]_*/
```

The highest number is the current max. Add 1. If there's a gap (e.g., 14 used twice and one moved to `_ARCHIVE/`), use the next clean number.

### 2. Create folder structure

```bash
mkdir -p Subcontractors/NN_<Trade>_Contractor/{01_Schedule_and_BOQ,02_Reference_Drawings,03_Specifications_and_Standards,04_Reference_Imagery,05_Returned_Submittals,06_RFIs,07_Approvals,Email_Data_Extraction,_MANAGER_DASHBOARD}
```

### 3. Author SCOPE_REQUEST.md

Follow the existing template pattern from an established contractor (e.g., `03_AV_IT_Contractor/SCOPE_REQUEST.md` or `16_Acoustic_Specialist/SCOPE_REQUEST.md`).

**Required sections:**
- Header block: Project, Contractor, Issuer, Issue date, Reply by, Discipline, Contract ref
- Privity note (Samaya → Sub only, no privity with MoC/PMC/CG/NRS)
- 1. Purpose — plain-language what this sub will do
- 2. Background — relevant RFIs, scope gap documents, NRS confirmations
- 3. Scope — headline table + critical spaces + key design parameters
- 4. Programme — milestone table (Day-N)
- 5. Required deliverables — staged deliverable table
- 6. Critical interfaces — interface table with counterpart parties
- 7. Sub-Contractor submission — what the bidder must return (pre-qual, tech proposal, priced BoQ, programme)
- 8. Reference files — table of source documents
- 9. Authority basis — contractual references (ER, SoW, DMP, RFI refs)

**Scope summary table format (use for §3):**
```
| # | Sub-system | Description |
|---|------------|-------------|
| 1 | [System] | [What it covers] |
```

**Programme table format:**
```
| Milestone | Day-N | Note |
|-----------|-------|------|
```

**Interface table format:**
```
| Interface | Counterpart | Resolution |
|-----------|-------------|------------|
```

### 4. Copy key reference documents into `02_Reference_Drawings/`

- The triggering RFI or NRS correspondence
- Relevant drawings from the design package
- Any spec sheets the sub must comply with

### 5. Create `_MANAGER_DASHBOARD/SITUATION_REPORT.md`

Status template:

```markdown
# [Trade] Contractor — Situation Report

**Last updated:** [date]
**Status:** 🔴 Not appointed / 🟡 Pending / 🟢 Appointed

## Current state
| Dimension | Status |
|---|---|

## Open actions
| # | Action | Owner | Target |
|---|--------|-------|--------|

## Key documents
| Document | Ref | Status |
|---|---|---|

## Risk items
```

### 6. Update `Subcontractors/README.md`

- Add the new row to the subcontractor register table (insert after the last row, maintaining sequential numbering)
- Update the "Last updated" date line at the top
- Include: `#`, trade name with description, folder link, status, lead time

### 7. Update project memory

Add a memory entry noting:
- New package number
- Trade name
- Date created
- Triggering document (RFI, scope gap, etc.)
- T2 allocation reference (if known)

## Pitfalls

- **Number conflicts** — if a previous folder used the same number for a different trade and was archived, pick the next clean number. Do NOT reuse archived numbers without explicit direction.
- **T2 allocation matters** — before creating the SCOPE_REQUEST, check the T2 allocation table for the trade. The package may sit under another subcontractor's umbrella (e.g., Interactive T2-09 sits under Rawasin's umbrella, not standalone).
- **Distribution list clues** — when a document triggers the package creation, the CC list tells you who's already involved. Route reference documents to those same parties.
- **No BOQ yet** — if there's no budget line for this trade yet, flag it in the risk items section of the situation report. Do not fabricate BOQ entries.
- **Reference the triggering document** — always copy the RFI/email/correspondence that prompted the package into `02_Reference_Drawings/` so the narrative is traceable.
