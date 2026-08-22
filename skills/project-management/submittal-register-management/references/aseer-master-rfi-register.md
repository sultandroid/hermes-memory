# Aseer Master RFI Register (`RFI.xlsx`)

Path: `.../Aseer-Museum/04_Docs/04_RFIs/RFI.xlsx` (~32 MB — often exceeds Telegram's 20 MB attach limit; work on it directly from the path, don't try to send it).

## Structure
- Single sheet `Sheet1`.
- **Row 2**: title banner. **Row 4 = header row**: `Subject | No. | Question | Photo if available | (SAMAYA Response) | (CG Response) | (PMC Response) | Answer`.
- Data rows start at row 5 (~524 live rows after stripping trailing empties).
- Organized as **blocks by Subject** (discipline). Each block restarts its own numbering in the `No.` column. Blocks repeat: "URGENT Object List", "A/V Design", "Show cases", "Showcase", "Art Commission", "Object List", "Tactile & Manual Interactives", "Graphic", "Structural Design Inquiries", "ICT/Security Design Inquiries", "Lightbox Coordination", "Lighting Decision", "Interior Design Decision".
- **Subjects repeat down the sheet** (a given Subject header appears many times, each starting a new block). A block can span 1 row up to ~40 rows (Showcase). Do NOT treat Subject as unique.

## Response-status reality (as of 2026-08)
- **PMC column is the only actively populated** one (~47 rows). Typical terse PMC values:
  - "Impact on showcase dimensions and specifications prior to fabrication." (bulk ~35×)
  - "Subject to advice and confirmation."
  - "Content to be provided by the End User." (Graphic block)
  - "Subject to project Specs." / "Valid"
- CG response ~1, SAMAYA ~0, Answer ~1. Fabrication-coordination register, heavily weighted to object/showcase fit-out (exhibit dims/weights per object across Lobby 3, Al Muftaha-G3, Al Qatt-G8, Scripts-G11, Archaeology-G12).

## The "Coordination" series (PRE-AUTHORED — do not duplicate)
Rows ~566-569 contain a pre-built family of **interface/coordination RFIs** with `Subject = Coordination - ...`. Search before adding any new coordination item:

| Row | Subject | Core ask |
|-----|---------|----------|
| 566 | **Coordination - Mounts & Art Handling** | Sec 2.2 / Interface Responsibility Matrix: (a) appointed MoC Mount Contractor + Art Handler, (b) sequence Display Cases→Mounts→Object Install, (c) cranage/rigging scope (Sec 13.31) |
| 567 | Coordination - Content & AV Media | content company + codecs/formats/resolutions |
| 568 | Coordination - Collections & Loans | loan object list + lender conditions + moving-object programme (Qasr Abu Melha rock) |
| 569 | Replica vs Original | final replica-vs-original list + BOQ quantities (Sec 010 TBC) |

If a user pastes one of these as a "new" RFI, **check it already exists** — don't add a duplicate row; instead confirm it's present and fill the blank `No.`/sender/date/response columns.

## NRS RFI discovery
NRS-driven RFIs arrive as Outlook emails from Jim Richards (jim.r@nissenrichardsstudio.com) with codes like `A2742-6.04-019` (Showcase Status). Extract the attached PDF via AppleScript; the body is short but the PDF holds the per-showcase numbered questions.

## User handling preference (Mohamed Sultan)
Asks to "read this file" and expects a **block-by-block breakdown by subject** with counts + response status, ending in a suggested next action — not a raw dump. When he pastes an RFI text asking "where do I put this", verify first whether it already exists in the register (search all cells for the Subject keyword) before proposing a new row.
