# LiDAR / Reality-Capture MOS Conventions

Condensed conventions for Method of Statement (MOS) documents covering terrestrial laser scanning (TLS) with the Faro Focus Premium, based on Aseer Museum project work.

## Scan-Station Overlap

| Scenario | Recommended overlap | Notes |
|---|---|---|
| **Standard TLS interior / exterior** | **≥30%** between adjacent scan positions | Enough for target-based + cloud-to-cloud registration |
| **Complex/constrained/heritage zones** | **≥50%** | Tight columns, dense MEP, highly occluded areas |
| **Aerial / photogrammetry** | 60–80% | **Not** the right benchmark for terrestrial LiDAR |

**Do not write ≥70% overlap for Faro Focus Premium scan positions.** 70% overlap is a photogrammetry norm and would unnecessarily inflate field time, scan count, and data volume without improving registration.

Good wording for the workflow diagram:

> ≥30% overlap between scan positions (≥50% in complex / constrained zones)

## Registration Confidence

Faro SCENE reports a **registration confidence** percentage per cluster. A threshold of **≥70% per cluster** is a reasonable quality gate and is **not** the same as scan-station overlap. Keep this wording unchanged when it appears in QC tables.

| Metric | Typical acceptable value |
|---|---|
| Registration confidence per cluster | ≥70% |
| Target-based error | ≤3 mm |
| Cloud-to-cloud error | ≤6 mm |

## Targets

- **Spherical targets (145 mm)** — reflective registration spheres, typically qty 6, used to align multiple scan stations in Faro SCENE.
- **Checkerboard targets** — alternative/secondary target type.
- Minimum **3 common targets** between adjacent scans for target-based registration.

## Client-Facing Language

- Keep the document client/CG-facing. Avoid exposing data-source attribution in the deliverable body (e.g. do not write "using OpenStreetMap data").
- Replace source labels with neutral descriptions: "site context" instead of "OpenStreetMap data".
- Keep actual site coordinates and identified surrounding neighbors if they are relevant to exterior scan scope, but present them as context, not survey control points.

## Equipment Reference

- **Scanner:** Faro Focus Premium 200 m
- **Typical resolution:** 1/4 (6.1 mm @ 10 m) standard; 1/2 (3.0 mm @ 10 m) for detail areas
- **Typical scan time per position:** ~3–4 minutes standard; ~5–6 minutes high detail
- **HDR:** Enabled for all interior scans
- **Range:** 0.6 m – 200 m

## Deliverable Formats

| Format | Use |
|---|---|
| `.e57` | Open-standard colourised point cloud archive |
| `.las` / `.laz` | GIS, Civil 3D, CloudCompare |
| `.rcp` / `.rcs` | Autodesk ReCap indexed cloud for Revit/AutoCAD/Navisworks |
| `.dwg` / `.pdf` | 2D cross-section linework |

## MOS Page Layout Notes

- Section 6.1 "Registration Pipeline" is short (numbered list + format table) and often fits on the same page as the Section 5/6 workflow diagram.
- Appendix pages that are a single image + caption can often be combined, but watch image height constraints.
- **Sections 3.2 (Support Equipment, 8 rows) and 4 (Survey of Surrounding Area, incl. 14-row neighbors table) can be merged into one page** by compacting the neighbors table font-size to ~0.48rem and reducing margins. This eliminates one full page. The Support Equipment table stays at normal size. The neighbors intro paragraph reduces from 0.84rem to 0.5rem. Verified working on the Aseer Museum MOS Rev 00.

## Team Roles — No Survey Sub-Roles

**Do not split survey work into "Survey Manager", "Survey Team", "Laser Scanning Specialist", "Scan Processing Specialist".** In practice the project has one survey team that handles all field operations, scanner operation, data verification, processing, registration, and export. Consolidate into a single row:

| Role | Responsibility |
|---|---|
| **Survey Team** | Executes the full survey scope — field operations, scanner setup & operation, data verification, processing, registration, and export delivery. |

Keep BIM roles separate: BIM Modeling Team and BIM QC Specialist.

## Delivery Timeline — Use Parallel Tracks

**Do not present a flat sequential milestone list.** Group deliverables by parallel processing track:

- **Data Integrity** — raw data backup verification (1 WD)
- **Point Cloud** — registered cloud, per-level sets, ReCap index, coverage map (3 WD, all from SCENE)
- **Quality** — registration/quality report (5 WD)
- **Documentation** — 2D cross-section set (5 WD)

Add an explanatory note: "All processing runs in parallel from the day field data is ingested."

Do NOT list "Deviation analysis" for Round A (AS-IS pre-demolition) — there is no design model to compare against. Deviation analysis is scoped for Rounds B (post-demolition vs structural IFC) and D (final as-built).

The "All deliverables complete" row should span both milestone columns and clearly state the delivery time for the longest parallel tracks.

## No Redundant Approval Section

The cover page already has the full QC sign-off block (Prepared by / Reviewed by / Approved by with Signature/Date fields). **Do not duplicate this as a separate Section 13 at the end of the document.** If an earlier version had a Section 13, remove it and update:

1. TOC: remove the section 13 reference
2. TOC: remove the empty group heading (e.g. "5 — APPROVAL") if all its items are gone
3. Page numbers: shift subsequent pages back by 1 and update footers
4. Cover/title page totals
5. Appendix page references in TOC

## TOC Cleanup After Structural Deletion

When removing a section, always check whether its TOC group heading is now empty. For example, removing "5 — APPROVAL" (which only contained Section 13) leaves the heading with no rows underneath. Delete the `<tbody>` block containing the group heading `<tr>`.

## Page Renumbering — No Global Replace on /20

When reducing total page count (e.g. /20 → /19), do NOT use a global `str.replace("/20", "/19")` — the pattern `/20` can appear inside base64-encoded image data, corrupting embedded images. Use index-based footer replacement targeting only `<span class="pg-num">` elements, or update each footer individually.
