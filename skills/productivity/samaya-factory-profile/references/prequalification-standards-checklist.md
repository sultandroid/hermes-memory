# Prequalification Standards Checklist — Samaya Factory Profile

Use this 7-point checklist when auditing the profile for prequalification submissions or updating section content.

## The Standards

| # | Standard | What to look for | Violation Examples |
|---|----------|------------------|-------------------|
| 1 | **Factory Language** | Never "ورشة/workshop/atelier" in visible text | "ورشة", "Workshop" in project meta, "Specialised ATELIERS", "Sculpture Atelier" |
| 2 | **Capability Evidence** | Show machines, process flow, equipment specs | Pages with only decorative text/no process (GRC/GRP, wayfinding gallery) |
| 3 | **No Brand Names** | Use generic technical terminology for scanner/consumable brands. **Exception**: machine brand names for production equipment (HOMAG CNC, Blum/Hettich hardware) ARE acceptable — they signal real installed capability in a prequal profile. | "Durst" instead of "UV Flatbed", "Roland" instead of "Roll-to-Roll Solvent" |
| 4 | **Museum Relevance** | Conservation-grade, Oddy/PAT, climate control | Sections that don't connect their capability to museum/exhibition use cases |
| 5 | **Bilingual Punch** | Arabic primary, English secondary. Short, active, no fluff | "we pride ourselves", paragraphs over 3 lines, Arabic as afterthought |
| 6 | **Photo Authenticity** | Real project/process photos only | SVG placeholders, GenAI images, phantom paths (Claude-invented filenames) |
| 7 | **No Aseer Museum** | Profile must NOT mention Aseer Regional Museum | Any mention of "متحف عسير", "Aseer Museum", "عسير الإقليمي" |

## Aseer Museum Relevance Criteria

Even though Aseer Museum isn't named, the profile should demonstrate capability for:
- Museum-grade replica production (3D scanning → CNC → hand-finish)
- Conservation-grade display systems (Oddy-tested materials, climate-controlled vitrines)
- Interactive AV/IT integration (Rawasin scope: T2-09)
- Scenography and museum fit-out
- High-precision documentation (structured light scanning, VDI/VDE 2634)

## Ed-Eyebrow Numbering Cross-Check

The `ed-spread` archetype has TWO numbering locations that must match:

1. **Page header**: `<div class="section-tag">17 · HSE RECORD</div>`
2. **Ed-eyebrow**: `<span class="ed-eyebrow">17 · ... · HSE</span>`

| Section | ID | Tag # | Eyebrow # |
|---------|----|-------|-----------|
| HSE | p4-hse | 17 | **17** |
| Approvals | p20 | 18 | **18** |
| After-Sales | p22 | 19 | **19** |
| Certifications | p25 | 20 | **20** |
| Financial | p4-financial | 21 | **21** |

## Terminology Replacement Table

| Wrong | Right (EN) | Right (AR) |
|-------|-----------|------------|
| workshop | factory, production unit | مصنع, خط إنتاج |
| atelier | team, department, production line | قسم, خط إنتاج |
| ورشة | مصنع | — |
| ستّ ورش | ستة خطوط إنتاج | — |
| ورش إنتاج | خطوط إنتاج | — |
| sculpture atelier | sculpture department | قسم النحت |
| specialised ateliers | production lines | خطوط إنتاج متخصّصة |

## Bilingual Eyebrow Check (BONUS QA)

After any redesign, verify ALL eyebrow labels use Arabic-primary ordering. Common pattern:

```html
<!-- WRONG — English first -->
<span class="v4-cmyk-eyebrow">SCOPE 05 · PRINT MACHINES <span>الطباعة</span></span>

<!-- RIGHT — Arabic first -->
<span class="v4-cmyk-eyebrow">الطباعة الرقمية وخط الإنتاج <span>SCOPE 05 · PRINT MACHINES</span></span>
```

**Check**: grep for eyebrow patterns where English appears as the outer text and Arabic is in the inner `<span>`. Fix by flipping.

## RTL Photo Placement Check (BONUS QA)

In `dir="rtl"`, the first DOM child renders on the RIGHT side. For 2-column pages with a photo column, the photo div must be FIRST in DOM order. Check all flagship and ed-spread pages.

## Multi-Agent Audit Workflow

1. Split 39 sections into 3 blocks (p1-p13, p13b-p25e, p4-hse-p27)
2. Each agent audits against 7 standards
3. Return section ID, specific quote+line, priority (HIGH/MED/LOW), suggested fix
4. Apply Round 1 fixes (text/terminology) directly via patch
5. Delegate Round 2 fixes (content expansion) to content subagent
6. QA verify: terminology, eyeballs, brand names, GenAI, Aseer, slogan, CSS height constraints
