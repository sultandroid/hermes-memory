# AV Content vs MoC Object List — Distinction for PRR-AV-01

## The Problem

PRR-AV-01 (AV/media content partly 'by others') was repeatedly discussed with the user. The user corrected the assumption that the MoC object list contained AV content. It does not.

## Key Distinction

| Term | What It Is | Examples | Source |
|------|-----------|----------|--------|
| **MoC Object List** | Physical artifacts approved by Ministry for display | Photographs, paintings, textiles, archaeological pieces, stone objects | CG email 2-Jul-2026 forwarding ministry-approved folder |
| **AV Content** | Digital media files for screens/projectors | Videos, motion graphics, interactive apps, slideshows | Rawasin scope / 'by others' boundary |

## The MoC Object List (Received 2-Jul-2026)

- **File:** `6930_Aseer_Object Schedule_20260610 (1).xlsx` (188 MB)
- **Path:** `OneDrive/.../02_Submittals/01_Shop Drawings/1.01 Showcase Shop Drawings/2026-07-01_CG_Object_Schedule/`
- **Total objects:** 295
- **In showcases:** 53
- **Hung/mounted on wall:** 197
- **TBC:** 32

### AV-Relevant Objects (only 11 out of 295)

| Object ID | Gallery | Display Method |
|-----------|---------|---------------|
| OB001–OB005 | Welcome Gallery | Image on screen (×5) |
| OBJECT CUT 1–6 | Flowersmen AV Slideshow | Projected as slideshow (×6) |

The remaining 284 objects are physical — no video files, no motion graphics, no interactive content.

## What This Means for PRR-AV-01

The risk says "AV/media content partly 'by others' and not finalised." The 'by others' content refers to **digital media files** (videos, motion graphics, interactives) that MoC may produce or provide. The object list does NOT contain this content — it only lists physical artifacts.

**The RFI to MoC (Action A1) should ask about:**
1. Content format, resolution, codec, delivery stage for each gallery's digital media
2. Which items MoC produces vs Rawasin produces
3. Storage estimates per gallery

**The object list review (separate from the RFI) should ask:**
1. Does the object list change AV hardware requirements (projectors, screens, interactives)?
2. Are there new objects that need different display methods than originally scoped?

## Email Thread Reference

- **2-Jul-2026:** CG (Mohammad Elbaz) forwarded ministry-approved object folder link (Zoho download)
- **3-Jul-2026:** Sultan sent to team: "The Ministry has approved the object collection reference for the Aseer Museum"
- **3-Jul-2026:** Jim Richards (NRS) raised concerns about stone dimensions and new showcase 12.65_SC_02
- **5-Jul-2026:** Waris sent acknowledgment to CG with contractual caveats
- **8-Jul-2026:** Yara Altahawy (Glasbau Hahn) provided showcase review comments

## NRS Tender Package JSON

The object schedule is also mirrored in the NRS tender package at:
`14_Completed_Tender_Package_From_NRS/07_Visualizations/.../object_schedule.json`

This JSON has 295 objects with fields: Object ID, Exhibit Name, Display Method, Showcase needed, Height/Width/Depth/Weight, Medium, Materials, Conservation requirements.

Use this JSON for quick analysis (no OneDrive lock issues) when the Excel file is inaccessible.
