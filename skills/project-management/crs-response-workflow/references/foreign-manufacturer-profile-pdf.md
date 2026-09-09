# One-Page Company Profile PDF for a Foreign Material Manufacturer

Pattern for building a quick, submittal-ready company profile when the manufacturer has **no downloadable brochure/company-profile PDF** on their site (only web pages + ISO certs). Used for the Eden-Design GmbH (patinated brass) case, 2026-09-08.

## When to use
- CG/consultant asks for "manufacturer details" on a material submittal.
- The material manufacturer is a foreign company with no official profile PDF.
- User wants speed over waiting for the manufacturer to email a brochure ("اعمل بروفيل من الموقع بتاعهم لسرعة المعاملة").

## Decision: build vs request
- **Build ourselves** (fast, sufficient for CG) — CG wants to verify the material comes from a real manufacturer, not a glossy brochure. Website facts + ISO certs are enough.
- **Request official brochure** only if CG explicitly demands a manufacturer-issued document. Be transparent in the reply: say "company profile attached" without claiming it's manufacturer-issued.

## Profile scope — GENERAL company profile, NOT our material (user preference)
The user's standing preference (corrected 3× in one session): the profile must be a **general company profile covering ALL the manufacturer's products and applications**, NOT a document focused on the one material relevant to our project. Concretely:
- **List every product line** the manufacturer makes (e.g. all 6 EDEN lines: BRONZE, INOX, COLOR/PVD, AQUASTEEL, WIRE FABRIC, ROLLING STRUCTURES), not just the patinated brass we're submitting.
- **Do NOT feature our specific material** as a highlighted section. The user said: "مش لازم تذكر بيانات المنتج بتاعنا" (no need to mention our product's data). A general profile reads as a neutral manufacturer capability statement; a product-focused one looks like we're steering CG.
- **Treat the file as a summary of the manufacturer's whole website** — "اعتبر الملف اللي هتعمله ملخص للموقع بتاعهم كله". Include: company overview, ALL products, processes/capabilities, applications/project types, certifications.
- **Images are optional / user often drops them.** The user first asked for product images from the site, then said "مش لازم صور" (no images needed) — a clean text list of products + applications is preferred. Default to a text-list layout unless the user explicitly asks for images.

## Applications vs named projects
- The manufacturer's site may have **no named-projects page** (Eden's `/references/` and `/historie/` URLs returned 404). When that happens, use the site's **"Applications" section** (architecture, elevators, shopfitting, art, yacht, automotive) as the project-type list. Do NOT invent named client projects that aren't on the site.
- If the site is German-only, translate the About/Applications pages rather than inventing content.

## Workflow
1. **Gather facts from the manufacturer's site** (browser or Brave Search):
   - Legal name + full legal entity (from ISO cert / imprint)
   - Address, contact, founded year
   - Product line relevant to the material + the material base/finish description
   - ISO certs (download the PDFs — they carry cert number, issuing body, validity, scope)
2. **Download ISO cert PDFs** and read them (they're often image-only — render to PNG and vision-analyze to extract cert no., body, validity, scope).
3. **Build a one-page A4 HTML** with weasyprint:
   - Bronze/brand-matching color scheme (for a metal-surfaces company: bronze `#8a6d3b` + beige `#f5f0e6`)
   - Header: brand name + tagline + founded/location + ISO badges
   - Tables for Company Overview, Product Lines, Certifications
   - A short "material" section describing the specific finish
4. **Compress to ONE page** — weasyprint spills to 2 pages easily. Reduce: body font ~9pt, line-height ~1.35, margins ~12-16mm, merge bullet lists into single lines, drop verbose product descriptions.
5. **Verify visually** — render page 1 to PNG, vision-analyze for overflow/cut-off before delivering.

## Pitfalls
- **NEVER put the project name in a manufacturer's profile.** Strip "Aseer Regional Museum" (or any internal project) from the profile text — it's internal info, not for a supplier-facing document. Say "for architectural and interior projects" instead.
- **Footer label: "Company details", not "Company Profile · Confidential".** The user corrected this: since WE built the document (not the manufacturer), the footer must say **"Company details"** — "Company Profile · Confidential" falsely implies it's a manufacturer-issued confidential document. This is a standing preference.
- **Use the manufacturer's real logo in the header.** The user supplied the official logo image (e.g. EDEN DESIGN · EXCLUSIVE METAL SURFACES). Replace the text brand block with the logo `<img>` (height ~16mm, width auto) + the founded/location line beneath it. Ask the user for the logo if not already in hand.
- **Verify the domain before trusting search results.** A "Eden catalog PDF" found via Brave Search was a *different* company (Eden retail shelving, Czech/UK). Confirm the URL is the manufacturer's own domain before using content.
- **ISO certs are often image-only PDFs** — `fitz.get_text()` returns empty. Render to PNG (`get_pixmap`) and vision-analyze to extract the cert details.
- **Don't fabricate** — only include facts actually on the site/certs. If the site is German-only, translate the About page rather than inventing.
- **Environment & Sustainability section** — the user may supply the manufacturer's sustainability bullet points verbatim (ISO certs, 100% recyclable materials, "Made in Germany", energy efficiency, recycling options). Add them as a dedicated section; keep the wording close to the source.

## Tooling
- `weasyprint profile.html out.pdf` (installed at `/opt/homebrew/bin/weasyprint`)
- Brave Search API for finding the manufacturer's pages: `curl -s "https://api.search.brave.com/res/v1/web/search?q=<query>" -H "X-Subscription-Token: <key>" -H "Accept: application/json"`
