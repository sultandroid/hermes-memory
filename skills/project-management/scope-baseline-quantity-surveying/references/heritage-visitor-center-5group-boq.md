# Heritage Visitor Center BOQ Categorization (5 Groups)

When the user requests explicit grouping for a small heritage/visitor-center project (Al Faw, Moqtana sites, etc.):

## Standard 5-Group Structure
- **Foundation** — RC masonry base, footings, hybrid wall bases
- **Steel work** — Full steel frame, roof beams/purlins, ALUCOBOND cladding, bracing, stairs (use 3D steel structure renders)
- **Civil work** — Masonry walls/floors/finishes, exhibition halls, reception/gift/admin fit-out, MEP, AV (apply 2-level café uplift only)
- **Site work** — Earthworks, paving, external works, prelims, provisional sums
- **Landscape** — Dunes, naturalistic engineering, tensile shading structures

## Rules
- Note in every file header: "Café ONLY has 2 levels; all other zones single level"
- Primary area source = floor plan table (القاعة 1/2/3 41.8 m² each, مقهى 115 m², etc.)
- Steel scope always cross-checked against the latest steel structure render

## OneDrive Delivery (always)
Stage to /tmp → Finder AppleScript duplicate → verify `PK\x03\x04` with `xxd -l 8`.