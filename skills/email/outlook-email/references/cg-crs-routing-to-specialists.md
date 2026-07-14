# CG CRS Routing to Specialists — Forwarding Pattern

When CG returns a Comments Resolution Sheet (CRS) with comments spanning multiple disciplines, Samaya needs to route the relevant portions to each specialist (NRS, Glasbau Hahn, ZNA, AD Engineering, etc.) for their action.

## Workflow

### 1. Trace the full email thread first

Use `Conversation_ConversationID` to get the complete thread — not just the latest email. The CRS may be the culmination of a multi-week exchange.

```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeSent, 'unixepoch', 'localtime') as sent,
       f.Folder_Name, m.Message_SenderList, m.Message_SenderAddressList,
       m.Message_NormalizedSubject, m.Message_HasAttachment as att
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Conversation_ConversationID = (
    SELECT Conversation_ConversationID FROM Mail WHERE Record_RecordID = <LATEST_EMAIL_ID>
)
ORDER BY m.Message_TimeSent;
```

### 2. Read the latest email body

Use AppleScript to get `plain text content` — the SQLite preview is truncated. This reveals the CG's justification for the overall status and any context not in the CRS.

### 3. Read the CRS Excel

The CRS is typically attached to the CG's reply email. Extract it via AppleScript, then read with openpyxl. Key columns:
- **No.** — Comment number
- **Initial** — Reviewer name (identifies which CG reviewer)
- **Sheet** — Drawing number or category (e.g. "Gen" for general, "Gen (showcases)", specific drawing numbers)
- **Reviewer Comment** — The actual comment text
- **Code** — Status: B = Approved w/Comments, C = Revise & Resubmit
- **Originator Reply** — Samaya's response (may be blank on first pass)

### 4. Identify comments relevant to each specialist

| Specialist | Signal keywords in CRS |
|---|---|
| **NRS (Jim Richards)** | Showcase design intent, Type 1/2/3 dimensions, opening mechanisms, material finishes (patinated brass, powder coated), perspective views, gallery layout, solid surface caps, plinth heights, frame widths |
| **Glasbau Hahn** | Showcase structural support, floor fixing, opening/closing mechanisms, security screws, hinge details |
| **ZNA / Studio ZNA** | Lighting coordination with showcases |
| **AD Engineering** | MEP coordination, structural comments |
| **Rawasin** | AV/IT/interactives coordination with showcases |

### 5. Draft the forwarding email

Structure:
- **Subject**: `FW: {original subject} — CRS for {Specialist} Action`
- **Body**: Brief context (what was submitted, overall CG status), then a bullet list of the specific CRS items requiring their action, grouped by category
- **Attachment**: The CRS Excel file itself

### 6. Key pitfalls

- **Don't forward the entire CRS raw** — specialists only need their subset. Extracting only relevant items shows you've done the triage.
- **Don't omit the overall status** — specialists need to know the package got C (Revise & Resubmit) so they understand urgency.
- **Don't paraphrase CG comments** — quote them verbatim. The specialist needs the exact wording to respond correctly.
- **Don't forget cross-references** — if a comment says "see General Comments" (items 1-13), include those general items in context even if they weren't addressed to that specialist directly.
- **Check if the specialist already replied in the thread** — Jim Richards may have already responded (e.g., "can't unzip RAR files"). Note that in the forwarding email so they know the file format issue is being addressed.

## Example: NRS-relevant items from an Arch DD CRS

Typical NRS-relevant items in an architectural CRS:

**Showcase comments (by CG's Islam Mostafa):**
- Showcases to be submitted as separate package with dedicated drawings
- All showcase drawings to be reviewed by Glasbau Hahn prior to final installation
- Standardize numbering system for all showcases
- Coordination schematic for services (power, fire alarm, data, AV) to showcases
- Showcase opening mechanism — under discussion between Samaya and Glasbau Hahn
- Structural support and floor fixing details — under discussion
- Lighting coordination with Studio ZNA — unresolved
- Perspective view per gallery required
- Type 1 showcase dimensions (length/depth variations)
- Solid surface 'caps' to fill recessed fixings
- Type 2 dimensions, proportions, materials, plinth height corrections
- Opening/closing mechanism impact on external appearance
- Pivot hinge finish (patinated brass or powder coated)
- Frame widths (15mm around door openings, 20mm elsewhere)
- Push-and-slide system vs hinged doors
- Flush solid surface cladding interface with setworks

**General comments (by CG's Maged Zamzam) that affect design intent:**
- Dimensions tentative — subject to cloud survey verification
- Coordinate with previously submitted Audit Report
- QA notes and sheet layout standards compliance
- On-site mock-ups for physical inspection
- Material samples for specification compliance
