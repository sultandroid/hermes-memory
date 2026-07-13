# Local-Agent vs Distributor — TRN + Trade-License Verification Recipe

A common compliance-system pitfall: a submittal names a "local agent" whose
TRN, trade license, and COO are all from a different country than KSA. The
project is in KSA, so the natural assumption is "KSA agent", but the documents
tell a different story.

## Quick verification recipe

1. Open the **Group TRN sheet** (e.g. `ProLab Trading LLC -TRN ... - Group.pdf`).
   - TRNs starting with `100` are **UAE Federal Tax Authority**.
   - A TRN starting with `3` is **KSA ZATCA** (10 digits, all-numeric).
   - A 15-digit number starting with `300` is also KSA VAT.
2. Open the **trade license** (e.g. `Pro Lab Trade License_2026_.pdf`).
   - Look at the "Authority" or "Issued by" field. If it says
     **Department of Economy and Tourism (DET)** or **Dubai DED**, it is UAE.
   - If it says **Ministry of Commerce (MOC)** KSA, it is KSA.
3. Open the **COO + Warranty** document.
   - The "Manufacturer" field tells you where the factory is, not the local
     agent. Use it for the manufacturer, not the local entity.

## Aseer-specific reference: ProLab Trading LLC

- **Entity:** ProLab Trading LLC (also written "Pro Lab Trading LLC")
- **TRN:** 100552354100003 (UAE FTA — not KSA)
- **Trade licenses:** 2025 + 2026 on file, both Dubai DET
- **Role for Aseer Museum:** **UAE distributor for Audinate**
- **Implication for compliance system:**
  - PQ to be submitted: "Prequalification of Distributor (ProLab Trading LLC)"
    — not "Local Agent" or "KSA Agent".
  - When listing ProLab in `compliance_matrix.md` supplier column, write
    `ProLab Trading LLC (UAE distributor)` — do not say "KSA agent".
  - The fact that ProLab sells into KSA does not change its registered
    jurisdiction; the trade license is the source of truth.

## How to record a non-KSA distributor in a compliance row

| Field | Recommended value |
|-------|-------------------|
| Supplier/Material | `Audinate (via ProLab Trading LLC, UAE distributor)` |
| PQ Ref (proposed) | `MOC-MUS-ASE-1E0-PQ-#### (Distributor — ProLab Trading LLC)` |
| Notes | "UAE distributor; Dubai DET trade license 2025+2026, TRN 100552354100003; not a KSA local agent" |

## Related CG Submission Sequence Rule (27-Apr-26)

A submittal without **both** an approved manufacturer PQ **and** an approved
local-entity PQ (whether the local entity is a KSA agent or a UAE distributor
selling into KSA) will receive Code C from CG. The compliance gap should
name *both* missing PQs so the procurement action is unambiguous.
