# Data Integrity Pitfalls

## The Principle

**Only use data that actually exists in the specified source files.** Never invent, extrapolate, or synthesize data from unrelated sources.

## Concrete Examples

| Scenario | ❌ Wrong | ✅ Right |
|----------|----------|----------|
| Material list has no image field | Extract swatch images from PPTX schedules and attach to materials | Show text-only tooltip — no images exists in source |
| JSON has `colour` field but no swatch hex | Generate a colored circle swatch from the colour name | Show the colour name as text, no visual swatch unless provided |
| Excel has product codes but no descriptions | Cross-reference from another spreadsheet without asking | Ask user if cross-reference is acceptable, or note "no description available" |
| PPTX has render images with callout positions | Extract callout positions from PPTX — these ARE real data because they're exact shape coordinates from the source file | ✅ Valid |
| PPTX has schedule tables with images next to material codes | Extract images from those tables and assign to materials as swatches | ❌ Invalid — the images are decorative/contextual, not a field in the materials data source. If the materials Excel/JSON has no `image` or `swatch` field, the images from PPTX schedule tables are NOT a valid substitute |

## Why This Matters

1. **Trust** — Every invented data point erodes trust. The user knows their data.
2. **Accuracy** — Synthetic swatches from colour names will be wrong (Terracotta ≠ #C4754A).
3. **Scope creep** — Once you start "enhancing" data, where do you stop? Each enhancement needs validation.
4. **User knowledge** — The user often has additional data sources they plan to connect later. Pre-empting this with invented data creates conflicts.

## Checklist Before Adding Any Field or Visual Element

- [ ] Does the specified source file contain this field? (Check JSON keys, Excel columns, CSV headers)
- [ ] If derived (e.g. truncated description), is the derivation obvious and lossless?
- [ ] If cross-referenced from another file, did the user explicitly ask for the merge?
- [ ] Am I generating placeholder data "for now" that user will need to replace later?

If any answer is "no" or "unsure" — don't add it. Ask first.
