# Cumulative CG Comment Disposition Table

Pattern for tracking CG review comments across multiple submission rounds in project management documents (Aseer Museum CRP, DMP, etc.).

## Structure

Two tables, same data at different detail levels:

### 1. Page 02 Summary Table (cover/resubmission page)

5 columns: `# | Round | CG Comment | Resolution in this Rev | CRP §`

### 2. §1.5 Detailed Table (body page)

Styling: `font-size:0.42rem` to fit more rows.
5 columns: `# | Round | CG Comment | Resolution | CRP §`

## Cumulative Round Format

Use `cat-row` section dividers between rounds:

```html
<tr class="cat-row"><td colspan="5">Round 1 · Rev.00 (25-Feb-2026)</td></tr>
<tr>
  <td class="mono">R1</td>
  <td><span class="badge badge-high">Rev.00</span></td>
  <td><b>Comment Title</b></td>
  <td>Resolution text</td>
  <td class="mono"><a href="#sX" style="text-decoration:none;color:inherit">§X</a></td>
</tr>
<tr class="cat-row"><td colspan="5">Round 2 · Rev.01 (CG Code C · 25-May-2026)</td></tr>
<tr>... (comments 1-8) ...</tr>
```

## Badge Semantics

- `badge badge-high` (amber) — Rev.00 / informational round
- `badge badge-critical` (red) — Code C / action required
- `badge badge-pass` (green) — Code A/B / approved
- `badge badge-info` (blue) — Under Review / submitted
- `badge badge-low` (gray) — Submitted / no response yet

## CRP § Column

All section references must be clickable anchor links with invisible style:

```html
<a href="#sX" style="text-decoration:none;color:inherit">§X</a>
```

## Resolution Text Style

- Start with the action taken ("§X updated to...", "§X provides...")
- Use present perfect for completed actions, present tense for current state
- Keep under 2 lines per row at 0.42rem
- Move section references to the CRP § column — don't embed them in resolution text
- Reference the CG reviewer by name (Mohamed Afifi for Roadmap, Mohamed Elbaz for Code C)

## When Adding a New Round

1. Append a `cat-row` divider + rows after the last round
2. Update the banner subtitle span to list all rounds covered
3. Verify CRP § links point to correct anchors