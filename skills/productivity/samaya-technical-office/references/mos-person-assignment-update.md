# MOS/Plan HTML Person Assignment Update — Worked Example

## Scenario
User specified a person to fill a QC Manager role for a Method of Statement:
> "Eng. Mohamed Samir Acting Review by QC Manager"

**Document:** MOC-ASEER-SIC-1K0-MOS-001_Rev00_MOS_LiDAR_Survey.html
**Person:** Eng. Mohamed Samir
**Role:** Acting QC Manager (title changes: "Samaya QA/QC Manager" → "Samaya Acting QA/QC Manager")

## 3 Distinct Blocks to Update

### Block 1 — Cover Page QC Block
Uses `.role` / `.nm` / `.tt` class structure:
```html
<div class="cell">
  <div class="role">Review by Acting QC Manager</div>     <!-- title change -->
  <div class="nm">Eng. Mohamed Samir</div>                <!-- name fill -->
  <div class="tt">Samaya Acting QA/QC Manager</div>       <!-- title change -->
  <div class="sig"><span>Signature</span><span>Date</span></div>
</div>
```

### Block 2 — Section 13 (Approval page, metadata grid)
Uses `.k` / `.v` + inline `div` structure:
```html
<div class="cell">
  <div class="k">Reviewed by (QC)</div>
  <div class="v">Eng. Mohamed Samir</div>                          <!-- name fill -->
  <div style="font-size:7pt; color:#444;">Samaya Acting QA/QC Manager</div>  <!-- title change -->
</div>
```

### Block 3 — Section 13 (QC Sign-off block, same structure as cover)
```html
<div class="cell">
  <div class="role">Reviewed by</div>
  <div class="nm">Eng. Mohamed Samir</div>                    <!-- name fill -->
  <div class="tt">Samaya Acting QA/QC Manager</div>           <!-- title change -->
  <div class="sig"><span>Signature</span><span>Date</span></div>
</div>
```

## Search Strategy

1. Find all occurrences of the old name/title:
   ```
   search_files(pattern='Samaya QA/QC Manager', path='path/to/file.html')
   ```
   This returns all 21+ occurrences in the file.

2. Group by context to identify which are the three distinct blocks:
   - Look for `.role` / `.nm` / `.tt` parent context → Block 1 or Block 3
   - Look for `.k` / `.v` parent context → Block 2

3. Patch each block individually — do NOT use a global replace because:
   - The HTML class structures differ between blocks
   - Some occurrences are the same title in different roles (e.g., "Samaya Technical Office Manager" also has `.role` / `.nm` / `.tt` but shouldn't be changed)
   - Some `.role` text differs slightly ("Review by QC Manager" vs "Reviewed by")

## Naming Convention

Two distinct scenarios:

| Scenario | Name Format | Title Change? |
|----------|------------|---------------|
| **Appointed Acting** (new appointment) | `Eng. Mohamed Samir` (no suffix) | Yes — title becomes "Samaya Acting QA/QC Manager" |
| **Signing on behalf of vacant role** | `Eng. Mohamed Samir (acting)` with "acting" in muted/smaller text | No — title stays "Samaya QA/QC Manager" |
