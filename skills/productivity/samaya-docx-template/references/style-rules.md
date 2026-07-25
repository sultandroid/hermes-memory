# Samaya Style Rules — Quick Reference

## Prohibited symbols
- **No `§`** — use "Section" (e.g. "DMP Section 3")
- **No icons or emoji in any format** — DOCX, Excel CR sheets, HTML, or email. Forbidden: ✅ ❌ ⚠️ ➡️ → 🟢 🔴 🟡 🔵 📌. Use plain text: `[done]`, `[missing]`, `[caution]`, `to`, ` - `, `per`
- **No arrows or typographic dashes** — em dash (—), en dash (–), right arrow (→), bullet (•). Write plain: "to", "-", "per"

## Known pitfall — icons in CR sheets and registers

The user WILL reject any file containing status icons (✅ ❌ 🟢 🔴 🟡). This includes Excel CR sheets, comment columns, review notes, and internal trackers — not just formal DOCX or HTML documents. Always use plain text `[done]`, `[in progress]`, `[missing]` instead. This is the #1 recurrent error across all deliverables.

## Prohibited AI fingerprints
- **Clichés**: seamlessly, robust, cutting-edge, bespoke, leveraging, delve, navigate, holistic, streamline, game-changer, state-of-the-art, world-class, innovative, synergistic
- **Phrasing**: "It is worth noting that", "It is important to mention", "Please be advised", "In the realm of", "When it comes to", "delighted to", "committed to excellence"

## Language rules
- **Active voice** — "Samaya will install..." not "Installation will be carried out by..."
- **British English** — natural, direct, Level 6 (B2-C1) readability
- **Samaya** (not "the Contractor") when referring to ourselves
- **No icons, emoji, or status symbols in any deliverable** — DOCX, Excel CR sheets, registers, slides, or internal trackers. This includes ✅ ❌ ⚠️ ➡️ → 🔴 🟡 🟢. Use plain text: `[done]`, `[missing]`, `to`, ` - `, `per`. The user will reject any file with these symbols.
- **Short sentences** (15-22 words), every sentence carries weight

## Visual rules
- **Font**: Calibri 11pt body, headings 14-18pt bold
- **Colours**: Navy #1E293B headers, Gold #C9A84C accents
- **Page**: A4 portrait, margins 2.5cm top/left, 2.0cm bottom/right
- **Tables**: Navy header row, alternating white/light gray (#F1F5F9) rows

## Remark/Note style
- **Remarks, evidence, caveats**: 9pt italic MEDIUM_GRAY (#64748B), compact spacing (Pt 11 line height)
- Use `doc.add_remark()` for compliance evidence, assessment notes, and secondary text
- Compliance matrix evidence column: 9pt italic gray, not body font

## Section page breaks
- Every H2 heading (14pt bold navy) auto-gets `pageBreakBefore` via `SamayaDoc.save()`
- No section starts near the bottom of a page — always at the top of a new page
