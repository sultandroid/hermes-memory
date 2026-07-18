# RFI / TQ Register Design

## Status Semantics — Critical Rule

**RFI/TQ status = whether CG answered the query, not the folder it sits in.**

| Status | Meaning | When |
|--------|---------|------|
| **OPEN** | Submitted, no CG answer yet | No response date |
| **CLOSED** | CG answered (any outcome) | Has response date |
| **REJECTED** | CG rejected the query itself (not the content) | Rare — only when CG says "wrong channel" |

Do NOT use "PENDING APPROVAL" or "PENDING REVIEW" — those describe the folder state (e.g., "in Approval/ subfolder"), not the answer state. An RFI in an "Approval/" folder is still OPEN until CG responds.

## Source of Truth Hierarchy

1. **Aconex** — live status (open/closed, response dates)
2. **Project Query Tracker (OneDrive)** — secondary check
3. **Adel Darwish's folder bank** — file-level cross-check only (folder names like "Approval/", "Approved/", "Done/" are hints, not authoritative status)

## Cross-Check with Adel's Folder Bank

Adel's bank (`05- Request For Information-RFI/`) has one sub-folder per RFI. Each may contain status sub-folders:

| Sub-folder | Meaning | Status Impact |
|------------|---------|---------------|
| `Approval/` | CG approval PDFs inside | Still OPEN — CG answered but Samaya hasn't actioned |
| `Approved/` | Final approved PDF | CLOSED — CG answered |
| `Done/` | Closed item | CLOSED |
| `Rev.01/` etc. | Revision submitted | OPEN until CG answers the revision |
| No sub-folder | Still open / pending | OPEN |

**Never use folder names to determine status.** Always check for a response date. If no response date → OPEN regardless of folder name.

## Register Columns

| Column | Content |
|--------|---------|
| Ref | RFI/TQ code (e.g., `MOC-ASEER-SIC-1A0-TQ-0020`) |
| Discipline | Structural, Architectural, Mechanical, General |
| Date Raised | When submitted to CG |
| Subject | Brief description of the query |
| Response Date | When CG answered (blank = OPEN) |
| Status | OPEN / CLOSED / REJECTED |

## Revision Handling

Each revision is a separate row with `Rev.NN` suffix on the ref. A revision is OPEN until CG answers it, even if the original was CLOSED.

## Anomalies to Watch For

- **Wrong discipline code in filename** — e.g., `ST-007.xlsx` inside `GN-007/` folder
- **Same file copied across folders** — e.g., `06- ARM–RFI-ST-007.xlsx` appearing in both `07-` and `08-` folders
- **Wrong discipline prefix** — e.g., `0ID` instead of `1A0`
- **Draft files in `@ Draft/`** — may have wrong codes; don't add to register until formally issued
