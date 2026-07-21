# Risk Merge Protocol

## When to merge
Two risks should merge when one is the **cause** or **sub-problem** of the other, not a separate risk. Signals:
- Same root cause (e.g. compressed baseline IS why completion won't happen)
- Same event/consequence (e.g. renovation permit + Stramp = same permit risk)
- One is a sub-problem of the other (e.g. fire pump option is part of Life Safety)
- Different scores/owners but same underlying risk event

## Merge procedure
1. **Absorb content** into the survivor risk:
   - Merge `cause` fields (the absorbed risk's cause becomes additional context)
   - Merge `consequence` fields
   - Merge `evidence` arrays (add `"Consolidated PRR-{ABSORBED}"` tag)
   - Merge `response_action` (combine with semicolons)
   - Merge `actions` arrays (deduplicate by text)
   - Merge `history` arrays (chronological order)
   - Keep the survivor's higher score if both are same; keep the higher if different

2. **Remove from all data sources**:
   - `risks.json` — remove the absorbed risk object from the `risks` array
   - `dashboards/risks.json` — same
   - `risks.json.bak` — same
   - `index.html` — rebuild the embedded JSON (or regenerate via build script)
   - Excel — rebuild Risk Register sheet, Dashboard critical-risks list, RBS counts
   - `risk_register.md` — rebuild the markdown table

3. **Mark treatment file as merged**:
   - Set frontmatter: `status: merged`, add `merged_into: PRR-SURVIVOR`
   - Body: explain what was absorbed and why

4. **Update survivor treatment file**:
   - Add `created` date if missing (use NTP/origin date, not system-creation date)
   - Update `last_updated`
   - Add note in history about the merge

5. **Deploy and commit**:
   - SCP index.html + Excel to server
   - Git add all changed files, commit with merge summary
   - Push

## Date correction rule
When a risk's `created` date is the system-creation date (e.g. `2026-07-12`) but the risk originates from NTP (`2025-12-01`), change it to the NTP date. The risk existed from project start — the system just didn't capture it until later.
