# A4 Print Page — Claude Delegation Pattern

When the user asks for a page to be "ready to print in A4", delegate to Claude Code with a VERY specific prompt. Vague prompts result in minimal changes (Claude just adds print CSS) which the user will reject.

## When to Delegate

- User says "make this A4 ready" or "redesign for one A4 page"
- User says "consult claude to design the page"
- NOT: user asking to just add a feature to existing page (edit directly)

## Prompt Template

```text
DESIGN TASK: Redesign the HTML page at {PATH} from scratch for A4 PRINT.
Do NOT keep the original layout — build a new A4-optimized one.

This is a MATERIAL SUBMITTAL page for {PROJECT NAME}. 
Sample: {MATERIAL NAME} ({SAMPLE CODE}).

NEW LAYOUT (A4 portrait 210×297mm):
- TOP BAR: Thin navy stripe (11mm). Left: Samaya logo (14px height). 
  Right: 'Material Submittal · {PROJECT NAME}' in small caps bronze.
- TITLE ROW: Title '{MATERIAL}' large (24px), code '{CODE}' beside it, 
  category tags right-aligned.
- META LINE: Project ref, Museum, Client, CG/NRS/PMC in small 8px gray.
- MAIN BODY: Two columns with thin border separator.
  - LEFT COLUMN (45%): The sample photo, cropped/capped to fit 
    (max-height 140mm, object-fit:cover, object-position:center).
  - RIGHT COLUMN (55%): Three compact info blocks stacked — 
    Material (1-2 lines), Specifications (4 lines: Substrate/Finish/Coating/Gauges),
    Applications (7 items in 2 columns).
- BOTTOM STRIP: Side by side with thin borders:
  - QR CODE (width 26mm)
  - DATASHEET LINKS (flex:1)
  - APPROVAL TABLE (width 78mm)
    Each review entity has its OWN row with signature+date — do NOT merge.
- FOOTER: Thin top border. Exact text: '{FOOTER TEXT}'

COLORS: Navy #13151A, Bronze #C8904A, Warm #F6F4F0, Text #262626, 
        Muted #6B6B6B, Border #E0E0E0

FONTS: Title Georgia serif 24px, body Inter 9.5px, small/meta 7-8px

CRITICAL: The Samaya logo is base64-encoded PNG in the HTML — 
PRESERVE IT EXACTLY as-is. Do not touch the base64 data.

Write the complete HTML to {OUTPUT_PATH}.
```

## Claude CLI Invocation

```bash
claude -p "PROMPT_ABOVE" --allowedTools "Read,Write" --max-turns 15 --max-budget-usd 1.5
```

## Post-Delegation Checklist

1. Check approval block has SEPARATE rows for NRS, CG, PMC — never merged into one
2. Verify footer text matches exactly what was specified
3. Confirm base64 logo data was not truncated (check file size)
4. Check `@page { size:A4 portrait; margin:0; }` is present in CSS
5. Open in browser and visually confirm all elements render
6. Do Cmd+P print preview — should fit one A4 page
7. If Claude merged review entities into one row, patch it back to separate rows

## Common Claude Failures

| Issue | Fix |
|-------|-----|
| Merges NRS/CG/PMC into one approval row | Patch back to 3 separate rows |
| Changed footer text | Patch the exact text |
| Photo too tall (no height cap) | Add `max-height:140mm; object-fit:cover` |
| Approval table collapsed (too narrow) | Increase `width` on `.cell-ap` |
| Logo base64 truncated | Restore from original file |
