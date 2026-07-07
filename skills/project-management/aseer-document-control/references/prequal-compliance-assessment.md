# Prequal Compliance Assessment & Gap-Filling

**Trigger:** User sends prequal documents for a supplier and asks "are they compliant?" or "can they pass?" — evaluating a supplier against a specific SOW's prequalification requirements (§5).

## Workflow

1. **Read the SOW prequal requirements** (§5 of the relevant SOW) — extract mandatory certifications, experience minimums, technical capabilities, and submittal package items.

2. **Map supplier's submitted docs** against each requirement in a compliance table:
   - ✅ Pass — requirement met
   - ❌ Missing — not provided
   - ⚠️ Partial — partially met or TBC

3. **Classify gaps into three tiers:**
   | Tier | Description | Verdict |
   |------|-------------|---------|
   | **Waivable** | ISO certs, BIM capability, fire/GREENGUARD knowledge — common for KSA establishments, CG may accept track record instead | Likely pass with conditions |
   | **Negotiable** | Museum project count (2 of 3 if cultural venues), team CVs if strong lead | Partial — needs framing |
   | **Blocker** | Missing methodology, programme, team CVs per SOW §5.4 | Must provide |

4. **Give a practical verdict** — not just pass/fail, but "can they pass with conditions" and what's needed.

5. **Offer to generate supporting docs** (methodology + programme) if the supplier's submission is incomplete. Generate these as standalone DOCX using the subcontractor's own branding:

   - **Methodology doc**: Map each SOW scope section to a technical approach. Use the supplier's actual equipment, tools, and team from their profile. Structure: assessment methodology → design methodology → commissioning → quality management → team & capabilities. Include SVG flowcharts (assessment workflow, design layers, commissioning workflow) embedded as PNG via cairosvg.

   - **Programme doc**: Extract deliverables from SOW §3 (Deliverables by Stage), map to phases with dates from the project's Design Phase Master Programme. Include: programme summary table (phase, ref, description, day range, dates, duration), deliverable schedule (ref, deliverable, phase, submission date), coordination dependencies table, assumptions. Include a Gantt-style SVG timeline.

   - **Format**: Generate as DOCX (user preference — editable). Use cairosvg for SVG→PNG embedding: `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 script.py`.

   - **Logo handling**: Extract the subcontractor's logo from their company profile PDF using PyMuPDF (`fitz`). Save to `_assets/` subfolder inside the supplier's prequal folder. Embed as PNG in DOCX via `run.add_picture(path, width=Cm(N))`.

   - **Branding rules for subcontractor-facing docs**:
     - Use the subcontractor's own logo and color scheme — NOT SamayaDoc template
     - Use raw python-docx with helper functions (add_h1, add_h2, add_styled_table, add_svg_logo, add_svg_flowchart, add_cover_block)
     - Cover says "Submitted to: Samaya Investment" and "Prepared by: [Subcontractor Name]"
     - Headings in the subcontractor's brand color (e.g., Pan Acoustics blue #0D57A5)
     - Table headers in brand color with light-tint alternating rows
     - Flowcharts recolored to match brand palette
     - No Samaya mentions in body text — use "the project's BIM Manager", "the project team" etc.

   - **Domain-specific scoping (learned from user corrections)**:
     - Oddy test only applies to materials in showcase/display areas near exhibits — NOT to general construction materials (ceiling panels, baffles, wall treatments, floor underlay). Scope the Oddy mention accordingly.
     - For acoustic specialists: GREENGUARD Gold and fire classification (EN 13501-1 Class A2/B) apply to all exposed materials in enclosed gallery spaces.

6. **File both docs** in the supplier's prequal folder and update the register's "Docs Filed" column.

## Pitfalls

- **Don't overstate compliance** — If the supplier has 0 museum projects, say so. Don't soften the gap.
- **Methodology must use the supplier's actual tools** — Don't invent equipment they don't have. Extract from their profile.
- **Programme dates must align with project baseline** — Use the Design Phase Master Programme (MOC-ASEER-0PS-SH-006), not invented T+X durations.
- **DOCX is preferred over PDF** for editable documents the supplier may need to modify. Generate both if time allows.
- **Subcontractor-facing docs must NOT use Samaya branding** — The user will correct you immediately if you put SamayaDoc template or Samaya logo on a document that a subcontractor is submitting TO Samaya. Use standalone raw python-docx with the sub's own logo and colors.
- **Oddy test is not for general construction** — Acoustic ceiling panels, baffles, wall treatments, and floor underlay do not contact exhibits. Only scope Oddy for materials inside showcases or directly adjacent to objects.
