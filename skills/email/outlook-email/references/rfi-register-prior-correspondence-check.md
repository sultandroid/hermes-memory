# Aseer RFI Register — "Does this RFI already exist / have prior correspondence?"

Workflow for the user's recurring question when adding a new RFI to the
Aseer RFI register (`04_Docs/04_RFIs/RFI.xlsx`): *"Is this already in the
register? Does it have any prior reference?"* Do NOT conclude "new/no prior
ref" until you have run every step below — the entry is often already in the
register under a block the user forgot.

## Search order (short-circuit — each step can end the check)

1. **Search the register itself FIRST (most common miss).** The user frequently
   types an RFI they already added. `RFI.xlsx` (32 MB, single sheet `Sheet1`):
   ```python
   import openpyxl
   wb = openpyxl.load_workbook('RFI.xlsx', read_only=True, data_only=True)
   ws = wb['Sheet1']
   for i,row in enumerate(ws.iter_rows(values_only=True)):
       for j,v in enumerate(row):
           if v and isinstance(v,str) and any(k in v.lower()
               for k in ['mount','art handl','rigging','content production','codec','media asset']):
               print(i+1, j+1, str(v)[:70])
   ```
   Note: an entry may exist with **empty No./sender/response columns** — its
   content (col 3) and title (col 1) are present but unnumbered/unanswered.
   Report it as "already exists (row N), needs numbering/dates/status".

2. **Outlook by SUBJECT keyword** (mounts/handling/rigging/content/media/AV):
   `Message_NormalizedSubject LIKE '%...%'`. Beware false positives from other
   projects — e.g. "mount" hits are Zamzam projector-mounting brackets, NOT Aseer.

3. **Outlook by PREVIEW/BODY text** (`Message_Preview LIKE`). Search exact
   phrases like `'appointed Mount Contractor'`, `'Art Handler'`, `'Interface
   Responsibility Matrix'`, `'content production company'`, `'codec'`.

4. **Related active package threads** — even if no prior RFI, flag the closest
   live correspondence as *contextual* (not a ref): e.g. the Rigging series
   (`48379` 15-Jul supplier ID, `50947` 16-Aug RFP, PQ-0130/131/132) for the
   cranage item; the AV Package Part II Rev001 submissions for the content/AV
   media item. These are NOT references to the RFI itself — say so explicitly.

5. **RFI Tracker (`00_Registers/A2742-10.05-004 RFI Traker.docx`)** — often
   OneDrive EDEADLK locked (unreadable). Note it as "unreadable" rather than
   "not present"; retry later rather than treating the lock as absence.

## RFI.xlsx structure (context for placement)

- Single sheet, organised in **subject blocks** — each block has its own Title
  column value + its own 1..N numbering. Blocks observed: `URGENT Object List`
  (object-dimension data requests), `A/V Design`, `Show cases`, `Art Commission`,
  `Object List`, `Tactile & Manual Interactives`, `Graphic`, `Structural Design
  Inquiries`, `ICT/Security Design Inquiries`, `Lightbox Coordination`, `Lighting
  Decision`, `Interior Design Decision`, and a **`Coordination - ...` series**
  (Mounts & Art Handling / Content & AV Media / Collections & Loans / Replica vs
  Original).
- Columns: Subject · No. · Question · Photo · SAMAYA Response · CG Response ·
  PMC Response · Answer. PMC is the only actively-filled response column on most
  rows.
- **Placement rule:** a pure interface/coordination query (Mounts+Art Handling,
  Content+AV Media) belongs in a `Coordination - ...` block, NOT shoehorned into
  the `Showcase` block (whose rows were mostly empty in this file). Create a
  new `Coordination - <topic>` block when none matches.
- Sibling queries often get built as a batch — check rows 560-575 for other
  `Coordination -` / `Replica vs` entries the user may already have drafted.
