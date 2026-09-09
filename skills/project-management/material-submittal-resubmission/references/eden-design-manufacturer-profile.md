# Eden-Design GmbH — Patinated Brass Manufacturer (MA-0007)

Facts gathered 2026-09-08 for the MA-0007 (Patinated Brass) resubmission. CG comment #3 asked for "manufacturer details" — the material's maker, NOT the showcase fabricator.

## Who makes the material
- **Eden-Design GmbH** — Am Großen Teich 15, D-58640 Iserlohn, Germany
- Established **1969**
- Product: **EDEN BRONZE™** — architectural bronze / patinated brass. Solid brass (CuZn) base, chemically bronzed and patinated. Options: polished, brushed, burnished, etched, textured, embossed. Made in Germany.
- Contact: eden@eden-design.de · +49 (0) 2371-40668 · www.eden-design.de
- Legal entity on certs: "Eden-Design GmbH Hans-Hermann Skischuweit-Eden Designer BDB GmbH"

## Certificates (SGS, both valid 24-Jul-2023 → 23-Jul-2026)
- ISO 9001:2015 — No. DE23/00000403
- ISO 14001:2015 — No. DE23/00000404
- PDFs: `https://eden-design.de/wp-content/uploads/2024/01/Zertifikat-ISO-9001.pdf` and `.../Zertifikat-ISO-14001.pdf` (image-only PDFs — read via pixmap, not text extraction)

## Product lines (all, for a general company profile)
- EDEN BRONZE™ — architectural bronze / patinated brass
- EDEN INOX™ — creative stainless steel surfaces
- EDEN PVD™ (page slug `eden-colors`) — decorative PVD stainless steel, anti-fingerprint option
- EDEN AQUASTEEL™ — water-ripple structured stainless steel
- EDEN WIRE FABRIC™ — architectural wire fabric (SS or brass)
- EDEN ROLLING STRUCTURES™ — patterned rolled stainless steel

## Site image URLs (high-res originals under /wp-content/uploads/, NOT /cache/ thumbnails)
- Bronze: `.../2026/02/bronze-patina-oberflaeche-individuell-charakter.jpg` (500×500)
- Inox: `.../2022/12/EDEN-INOX-2.jpg` (664×496)
- PVD: `.../2026/02/pvd-edelstahl-perforiert-design-spiegelnd.jpg` (1920×2560)
- Aquasteel: `.../2023/10/Water-Ripple-C002-ceiling-J-Hotel-Shanghai-Tower-4-scaled.jpg` (2560×1920)
- The `/cache/` variants are 250×200 thumbnails — too small for print.

## Company-profile build recipe (weasyprint, single A4 page)

Two accepted variants — the user iterated from the image grid to a text-only site summary:

**Variant A — image grid (first pass):**
1. HTML with `@page { size: A4; margin: 0 }`, bronze/beige palette (#8a6d3b).
2. Sections: header (name + tagline + ISO badges) → company overview table → product grid (2×2 cards, each img + name + desc) → processes → applications → certifications → footer.
3. Product images: `object-fit: cover; height: ~34mm` in 48%-width cards.
4. Compress spacing/fonts (9pt body, tight margins) to fit ONE page — content + 4 images overflows to 2 pages otherwise.

**Variant B — text-only site summary (FINAL, what the user kept):**
The user rejected the image grid: *"مش لازم صور ممكن تعمل قايمه بالمنتاجات والمشاريع حسب النوقع الرسمي بتاعهم"* (no images needed — make a list of products and projects per their official site; treat the file as a summary of their whole site). So:
- Drop the product image cards entirely; list product lines as a table (name + one-line description).
- Add an **Applications & Project Types** section (from the site's "Applications" block: architecture, elevator construction, shopfitting, art & design, yacht & shipbuilding, mechanical/medical/automotive).
- Add a **Processes & Capabilities** section (polishing, etching, PVD, gold plating, laser cutting, embossing).
- Add an **Environment & Sustainability** section — the user supplied the 8-point block verbatim (ISO 9001/14001, 100% recyclable materials, "Made in Germany", energy efficiency, customer awareness, day-to-day integration, 100% product recycling).
- Add a **Gallery link** row in the company overview (`https://eden-design.de/en/gallery/`).
- **Remove the Certifications section** — the user said *"remove CERTIFICATIONS section i will add copy"* (they supply their own cert copy). Keep the ISO badges in the header only.
- **Footer label** = `Company details` (NOT "Company Profile · Confidential") — because the profile is self-made from their public info, not an official manufacturer document. The user: *"change Company Profile · Confidential to Company details since this made form us not form them."*

**Both variants:**
5. `weasyprint in.html out.pdf`; verify page count + visual via pixmap.
6. **Never** mention the project name (Aseer Museum) in a manufacturer profile — it's internal and the profile is a generic company doc.
7. Be transparent: self-made from public site info, not an official manufacturer brochure. If CG demands official, request from manufacturer.

## Site structure notes (Eden-Design)
- The site has **no dedicated references/projects page** — `/en/references-2/`, `/referenzen/`, `/historie/`, `/unternehmen/`, `/produkte/` all return 404. "Projects" data therefore comes from the homepage's **Applications** block, not a references page.
- Product page slugs: `architectural-bronze/`, `eden-inox/`, `eden-colors/` (PVD), `eden-aquasteel/`. `eden-pvd/` and `eden-brass/` 404.
- ISO cert PDFs are image-only (read via pixmap, not text extraction).

## CRS reply for comment #3 (humanized — FINAL)
> Noted. The patinated brass material is manufactured by **Eden-Design GmbH** (Iserlohn, Germany) — their EDEN BRONZE™ architectural bronze, a solid brass (CuZn) base that is chemically bronzed and patinated. **Company details attached.**
>
> To ensure colour and finish consistency across all applications, the patinated brass is supplied from this **single source** (Eden-Design), while each application is fabricated by its respective approved specialist:
> - **Showcases** — Glasbau Hahn GmbH (PQ-0063, Code B)
> - **Setworks** (display units, display frames, AV units) — approved setwork specialist
> - **Main gallery doors & door reveals** — approved door fabricator
> - **Reception desk** — approved specialist
> - **Reception feature wall** (FI_ST_03) — approved specialist
> - **Wayfinding signage** (FI_GR_11) — approved signage specialist
> - **Floorbox trim** (FI_ME_03) — approved specialist

**Reply evolution (why it changed):**
1. Started as "Company profile and ISO 9001/14001 certificates attached" → changed to **"Company details attached"** once the self-made doc was named `Eden-Design_Company_Details.pdf`.
2. User corrected: don't stop at showcases — **every application has its own approved fabricator** (setworks, doors, reception, wayfinding, floorbox trim). Enumerate all applications from the approved Finishes Schedule 6930 Rev A.
3. User added: state the material comes from a **single source** (Eden-Design) to guarantee colour/finish matching across all applications — this strengthens the reply.

## Logo in the profile header
The user supplied the official Eden-Design logo image (black "EDEN DESIGN · EXCLUSIVE METAL SURFACES" wordmark, ~1280×262) and asked to add it to the header. Replace the text brand block with `<img src="eden_logo.jpg" height:16mm>` + keep the "Established 1969 · Iserlohn, Germany" line below it. Keep the ISO badges on the right.
