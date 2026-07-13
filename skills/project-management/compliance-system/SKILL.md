---
name: compliance-system
description: Manage the Aseer Museum compliance system — update compliance_matrix.md, compliance_gaps.md, and compliance_checklist.md when new specs/SOWs/materials/suppliers are approved.
---

# Compliance System — Aseer Regional Museum

## When to use

- A new supplier prequalification (PQ) is approved by CG
- A new material submittal (MA) is approved/rejected
- A new SOW or spec is approved
- A compliance gap is discovered or resolved
- Daily compliance sync (cron)

## Files

| File | Path | Purpose |
|------|------|---------|
| Compliance Matrix | `Technical_Office/Compliance_System/compliance_matrix.md` | Master spec→requirement→supplier mapping |
| Compliance Gaps | `Technical_Office/Compliance_System/compliance_gaps.md` | Open gaps tracker |
| Compliance Checklist | `Technical_Office/Compliance_System/compliance_checklist.md` | Checklist for new submissions |
| Spec List | `01_Registers/specification_list.md` | 387 specs, CSI MasterFormat |
| PQ Register | `01_Registers/prequalification_register.md` | 110 supplier prequalifications |
| MA Register | `01_Registers/material_submittal_register.md` | Material submittals |
| Specialist Register | `Technical_Office/Specialist_Management/specialist_register.md` | 27 specialists |
| Procurement Register | `01_Registers/procurement_package_register.md` | 19 procurement packages |

## How to update

### Adding a new supplier/material to the compliance matrix

1. Read `compliance_matrix.md` to find the correct Division and Req ID
2. Read `specification_list.md` to find the matching Spec No.
3. Read `prequalification_register.md` or `material_submittal_register.md` for PQ/MA ref
4. Add a new row to the compliance matrix with:
   - Req ID (from ER/SoW/DMP)
   - Requirement description
   - Spec No. (from spec_list.md)
   - Discipline code
   - Supplier/Material name
   - PQ Ref and/or MA Ref
   - Compliance status (🟢/🟡/🔴/⚪)
   - Gap ID (if non-compliant, link to compliance_gaps.md)
   - Last Checked date
   - Notes (action items, CG comments)
5. If a new gap is created, add it to `compliance_gaps.md`
6. **Recompute the roll-up block from the table data** — see "Roll-up
   recalculation" section below. Never edit roll-up by arithmetic against the
   prior declared value.
7. **Cross-agent audit** — before declaring done, have a second agent
   (Codex, Kimi, or any other labor) review the deltas against the source
   data and the project rules. The audit prompt must include the source
   file path and an explicit ask to enumerate issues. The leader agent
   integrates the audit, fixes any issues, then reports completion.

### Closing a compliance gap

1. Read `compliance_gaps.md`
2. Move the gap from Open Gaps to Resolved Gaps
3. Add Closed Date and Closed By
4. Update the compliance matrix row to 🟢

### Daily sync (cron)

1. Check Aconex transmittals (Outlook noreply@aconex.com) for new approvals
2. Update compliance_matrix.md with any new approvals
3. Update compliance_gaps.md (resolve closed gaps, add new ones)
4. Recalculate roll-up counts
5. Generate report if changes found

## Roll-up recalculation — DO NOT TRUST THE PREVIOUS NUMBERS

The pre-existing roll-up lines in both `compliance_matrix.md` and `compliance_gaps.md` are
historically drifted from the actual table contents. **Never edit by arithmetic against the
old roll-up.** Always recompute from the data:

- **Matrix row count** = sum of rows across all `Division NN` + `Exhibition-Specific` +
  `Specialist Sub-Contractor Compliance` sections, excluding the header row and the
  `---` separator. Don't include the roll-up block itself.
- **Matrix status counts** = walk every data row, count by the emoji (🟢/🟡/🔴/⚪) that
  appears in the Compliance column.
- **Matrix "Open gaps"** = count of **unique Gap IDs** referenced across the matrix
  (not the gap register's row count).
- **Gap register "Total gaps"** = open rows + resolved rows.
- **Gap register "🔴 Open (critical/high)"** = count of open rows where the Severity
  column contains `Critical` or `High`. **Not** the count of rows with a 🔴 emoji in
  the Status column.
- **Gap register "🟡 In Progress"** = count of open rows where the Status column
  contains 🟡 In Progress.
- **Gap register "🟢 Resolved"** = count of rows in the Resolved section, not in Open.

**Pitfall — emoji-vs-text dual signal:** the Open Gaps table mixes Status emoji (🔴/🟡/🟢)
with a separate Severity column. Several "🟢 Resolved" rows still appear in the Open section
because they were never moved. Treat the roll-up recompute as a chance to surface
duplication bugs (e.g. `GAP-AV-003` historically in both Open and Resolved) — flag
them, don't silently fix them in scope-limited updates.

**Pitfall — don't use "MOC-Asser-SIC-..." as the current PQ prefix.** The historical
register uses that prefix for early PQs (PQ-0001 through ~PQ-0110). The current
contract prefix is **`MOC-MUS-ASE-1E0-PQ-####`** (note: MUS, not Asser). When citing
the next available sequence, always read the highest-numbered row in
`01_Registers/prequalification_register.md` and add 1 — and **also check the
related "X- MOC-...PQ-XXXX" OneDrive folder index**, because Aconex-synced PQs
that were skipped on the register are still filed under their old number on
OneDrive. The two sources occasionally drift; if you only consult the markdown
register you'll propose a sequence number that is already in use on the CDE.
Always cite the *actual* next free number in compliance_matrix / gap Notes, not
"next free + buffer" or "PQ-0XXX+".

**Cross-agent audit is mandatory before declaring a compliance update complete.**
A leader agent making non-trivial updates (adding rows, opening gaps, recalculating
roll-ups) MUST have a second agent (Codex, Kimi, or another labor) audit the
deltas against the source-of-truth file before reporting done. Empirically the
audit catches: mislabelled jurisdictions (KSA vs UAE), stale PQ sequences, wrong
qty counts, roll-up arithmetic errors, missing pre-existing roll-up duplications
worth flagging. The audit prompt must include: the source file path, the
proposed delta, the rule(s) being applied, and an explicit request to enumerate
issues (not just PASS/FAIL). Don't rely on self-verification alone.

**Update the User profile after every successful compliance cycle.** When you
discover a non-obvious fact (a vendor's true jurisdiction, a new spec ID
convention, a contract prefix correction), it belongs in `memory` target=`user`
or `memory` target=`memory` so the next session starts already knowing. Don't
re-discover the same fact in a later session.

## Workflow pitfall — canonical OneDrive location for new PQs

When a submittal arrives in `~/Downloads` or `/Volumes/MIcro/Download/`, file
it under the **Samaya BIM Unit's Aseer project tree**, NOT under
`Adel Darwish's files`. The two trees look superficially similar but the
project of record is the BIM unit tree:

| Destination | Use it for |
|---|---|
| `OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/02_Submittals/09_Prequalifications/` | **Canonical PQ filing.** Flat folder of `MOC-MUS-ASE-1####-PQ-####.pdf` files mirroring the markdown register. |
| `OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/24_Subcontractors/<NN>_<ContractorName>/01_Schedule_and_BOQ/` | Equipment BOQs / scope-of-work XLSXs for each specialist sub-contractor. Pattern: drop a `<Vendor>_<Scope>_<Date>.xlsx` next to a `<_Vendor>_<Scope>_DepositRecord.md` sidecar (per AGENTS.md `PDF + _Analysis.md sidecar` rule). |
| `OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/02_Submittals/03_Submittals/03.3_Material_Submittals/<NN> -MA-####/` | Approved material submittals. |
| ~~`Adel  Darwish's files - 01- Execution Documents/07- Pre-Qualification Submittal/`~~ | **Do NOT use for new filings.** Adel's personal working folder, not the project canonical. Also unwritable from terminal sessions (uid 114). New PQs already filed there from earlier sessions should be left in place; new PQs go to the BIM tree. |

**Default rule:** when in doubt between `Adel Darwish's files/` and
`Samaya/Technical Office/Bim Unit/Aseer-Museum/`, choose the BIM unit
folder. The project of record lives there. `Adel Darwish's files/` is for
Adel's personal execution work, not the project archive. **The user has
explicitly corrected this twice** (13-Jul-2026: "no dont use addel darwish
files, use our BIM folder").

**Writable check (do this first):** before any `mkdir` or `cp` into a new
OneDrive subfolder, run a `touch .test_write` then `rm .test_write` on the
target. The BIM unit tree is uid 501 (writable). The Adel subfolder tree is
uid 114 (blocked). Always confirm before filing.

**Filing pattern (mirrors the existing PQ register):**

```bash
PQ_BASE="/Users/mohamedessa/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/02_Submittals/09_Prequalifications"
cp "Audinate_Datasheet.pdf" "$PQ_BASE/MOC-MUS-ASE-1E0-PQ-0113_Audinate_Datasheet.pdf"
```

Naming convention:
`MOC-MUS-ASE-1<disc>-PQ-<####>_<Vendor>_<DocType>_<YearExt>.pdf`
where `<disc>` matches the markdown register's discipline code (1E0 for AV/EL,
1A0 for AR, 1C0 for CIVIL, 1M0 for ME, 1K0 for management, 1V0 for surveys).

**For equipment scope docs** (BOQ XLSX, vendor quote PDFs that aren't formal
PQ cover letters), file them in the sub-contractor's BOQ folder, not the PQ
folder. Always write a sidecar `.md` per AGENTS.md convention.

**When `mkdir` fails for an unrelated reason** (cache lag, OneDrive sync
conflict), don't fall back to Adel Darwish's files — fall back to writing a
`_FILE_PLAN.md` next to the source files in `/Volumes/MIcro/Download/` so
the user can run the `cp` commands manually. Never silently misfile.

## Workflow pitfall — user non-response to `clarify`

When the user does not respond to a multi-choice `clarify` within the timeout,
default to the **lowest-risk reversible action**, not the most-complete one. For
a file-filing question this means: create placeholders / write a `_FILE_PLAN.md`,
keep source files in their original location, and let the user re-prompt if they
want a different structure. Don't make destructive assumptions ("they probably
want me to do X") that they cannot undo.

## Pitfalls learned in practice

- **Distributor ≠ KSA agent.** A TRN starting with `100` and Dubai/DET trade licenses
  means the entity is **UAE-registered**, even if it sells into KSA. Verify by reading
  the trade-license PDF (authority field) and the COO/Group-TRN sheet before
  labelling. For Aseer, ProLab Trading LLC is a **UAE distributor** (TRN 100552354100003),
  not a KSA local agent — `compliance_matrix.md` and `compliance_gaps.md` rows must
  say "UAE distributor" and the PQ submitted for them is a distributor PQ, not a
  local-agent PQ.
- **Qty cross-check against the design concept.** An equipment BOQ submittal can
  drift from the AV/electrical concept design (e.g. Audinate BT adapters: concept
  says 6 units, supplier XLSX says 5). Note the delta in both the matrix row and
  the gap, and add "resolve qty gap" to the mitigation list. Don't pick a winner
  in the compliance system — flag for the design coordinator.
- **CG Submission Sequence Rule (27-Apr-26) implications.** A material/equipment
  submittal whose manufacturer AND whose local distributor/agent both lack an
  approved PQ cannot receive Code A or B from CG. When a new submittal lands
  without PQs, default the new matrix row to 🔴 and create one gap that names
  *both* missing PQs (not one), so the procurement action is clear.
- **Related-PQ context.** When a submittal depends on multiple approved-but-
  pending PQs (e.g. Audinate adapters depend on Q-Sys DSP and Dante AV network
  approvals), list each related PQ with its current code in the gap Notes.
  Stakeholders reading the gap need to see the full dependency chain at a glance.
- **Source paths must be absolute and reproducible.** When a submittal originates
  from a download volume (e.g. `/Volumes/MIcro/Download/Audinate/...`), include
  the absolute path in the matrix row's Notes. Future agents will need it to
  re-open the source files.

See also `references/local-agent-vs-distributor.md` for the TRN + trade-license
verification recipe used to distinguish a UAE distributor from a KSA local agent,
and `references/aseer-onedrive-structure.md` for the verified OneDrive
folder map (where to file PQs vs equipment BOQs vs MAs in the canonical
Samaya BIM unit tree — vs the unwritable Adel Darwish's files tree).

See also `templates/pq_submission_email.md` for the **short default
email** the user wants when a compliance update turns into a submittal
(compliance statement + submit sentence + OneDrive file links + one
owner action). The long variant with the full compliance checklist
exists in the repo at
`Technical_Office/Specialist_Management/pq_submission_email_template.md`
but is **not** the default — default is the short version. The user
has explicitly corrected this once: "we didnt talk to much we just
tell its complince with project requirments, and give him the
submittle sentance and give him the prequl files link if any"
(13-Jul-2026).

## Communication after a compliance update → Aconex submittal

Whenever a compliance update leads to a PQ being filed in the BIM unit
PQ folder and is ready for Aconex upload, draft **one** short email to
the project team. Use the template at
`templates/pq_submission_email.md` — never the long variant. The
shape is always:

1. **One-line state of compliance** (e.g. "dossiers comply with the
   project PQ requirements per DMP Rev C04 §5.1.2 and the CG
   Submission Sequence Rule (27-Apr-26)").
2. **Submit sentence** — the explicit "Submitting for Aconex upload
   as follows:" header, then one line per PQ/MA with: `PQ-####` ref,
   full doc number, vendor, scope.
3. **PQ files block** — flat list of OneDrive paths to the filed
   docs. No PDF sizes, no per-document commentary.
4. **One owner action** — usually "Hesham — please upload to Aconex
   (separate transmittals) and circulate the CGP-WTRAN numbers."

**Do NOT include** in this short email:
- The full 11-item compliance checklist (lives in the matrix/gap).
- The full open-items list (lives in the gap Notes).
- The CG Submission Sequence Rule deep-dive (one sentence citation
  is enough).
- CC list beyond the canonical team: Hesham (Doc Ctrl), Shihab
  (Procurement), Adel/Waris (approval), sub-contractor coordinator
  (Rawasin for AV, etc.), Sultan (user).
- A pre-amble or post-script explaining the email.

File the draft at
`05_Comms/drafts/<YYYY-MM-DD>_<PQ-ref>_<Vendor>_Aconex_submission.md`
per project convention (plain-text in repo, user copies & sends
manually — never an Outlook draft).

**Compliance action items** triggered by the submittal (Sultan review,
Hesham Aconex upload, Adel/Waris endorsement) MUST also be appended
to `00_Status/action_items.md` with the date and the email-draft
filename as the source. The `prequalification_log.md` gets a new
row in DRAFT state for the proposed PQ number (not yet in the
markdown-register row count).

## Verification

Before committing any update to `compliance_matrix.md` or `compliance_gaps.md`,
run:

```bash
python3 ~/.hermes/skills/project-management/compliance-system/scripts/verify_rollups.py
```

The script recomputes the roll-up numbers from the actual table data and exits
non-zero if the declared roll-up has drifted. Wire it into the daily sync cron
before the report-generation step.

When the update introduces a new gap that names a proposed PQ number
(e.g. "submit Audinate as PQ-0113"), also run:

```bash
python3 ~/.hermes/skills/project-management/compliance-system/scripts/check_pq_sequence.py
```

This script reads **both** the markdown PQ register and the OneDrive folder
index, then reports the highest PQ seen in each source and the actual next
free number. Use it before claiming a PQ sequence in any compliance row or
gap — the markdown register and OneDrive drift occasionally (Aconex-synced
PQs may not be in the local md yet), and proposing a number that's already
in use on the CDE is a procurement blocker.

Before any `mkdir` or `cp` into OneDrive, run:

```bash
python3 ~/.hermes/skills/project-management/compliance-system/scripts/check_onedrive_writable.py
```

This script does a `touch`+`rm` write-test on the canonical BIM-unit
folders AND the known-blocked Adel Darwish's files folder, so the agent
gets a clear signal about where filing will succeed and where it
won't. Exit 0 = proceed; exit 1 = fall back to `_FILE_PLAN.md`.

## Compliance status codes

| Code | Meaning |
|------|---------|
| 🟢 Compliant | All requirements met |
| 🟡 Partial | Some requirements met; gaps remain |
| 🔴 Non-compliant | Critical requirements not met |
| ⚪ Not assessed | Not yet evaluated |

## CG status codes

| Code | Meaning |
|------|---------|
| A | Approved |
| B | Approved w/ comments |
| C | Revise & Resubmit |
| D | Disapproved |
| U | Under Review |

## Key rules

- Every compliance row must trace to an ER/SoW/DMP reference
- Every spec must have a CSI MasterFormat number
- Every supplier must have a PQ reference (or be flagged as not yet PQ'd)
- Every material near artefacts must have Oddy test status
- CG comments must be preserved verbatim in Notes
- Gaps must have a target date and owner
- Roll-up counts must be recalculated after every update
