# Schedule Activity ID Mapping

When the user provides a programme schedule (P6/Aconex export), map its activity IDs to the submission plan's "Linked Activity ID" column.

## Typical Schedule Structure (Aseer Museum)

The schedule uses prefix codes:
- `EN` = Engineering/Design activities
- `AS` = Assessment/Survey
- `PE` = Preliminary/Establishment

## Architectural Design Activities

| Activity ID | Description | Typical Finish |
|-------------|-------------|----------------|
| EN1000 | Preparation & Submission of 3D Shot | 12-Jul-26 |
| EN10 | Approval of 3D Shot | 14-Jul-26 |
| EN108 | Preparation & Submission of Architectural Technical Design 50% | 19-Jul-26 |
| EN109 | Preparation Architectural BIM Model 50% | 19-Jul-26 |
| EN110 | Preparation Architectural Product/Material Submittal Schedule 50% | 19-Jul-26 |
| EN111 | Approval of Architectural Technical Design 50% | 19-Jul-26 |
| EN112 | Approval of Architectural BIM Model 50% | 13-Aug-26 |
| EN113 | Approval of Architectural Product/Material Submittal Schedule 50% | 05-Aug-26 |
| EN134 | Preparation Exhibition Lighting Design 50% | 27-Jul-26 |
| EN135 | Preparation Showcase Design 50% | 27-Jul-26 |
| EN136 | Preparation Graphic Design 50% (Exhibitions + Wayfinding) | 27-Jul-26 |
| EN137 | Preparation AV Hardware Systems Design 50% | 27-Jul-26 |
| EN138-141 | Approvals for Specialized Designs 50% | 30-Jul-26 |
| EN144 | Preparation & Submission of Architectural Technical Design 90% | 19-Aug-26 |
| EN154-157 | Specialized Designs 90% (Lighting, Graphic, AV, Showcase) | ~Sep-26 |
| EN163 | Preparation & Submission of BIM Model 90% | ~03-Sep-26 |
| EN164 | Submission of Clash Detection Report 90% | ~03-Sep-26 |

## Structural Design Activities

| Activity ID | Description | Typical Finish |
|-------------|-------------|----------------|
| EN102 | Preparation & Submission of Structural Design 50% | 19-Aug-26 |
| EN103 | Preparation Structural BIM Model 50% | 19-Aug-26 |
| EN104 | Preparation Structural Product/Material Submittal Schedule 50% | 16-Aug-26 |
| EN106 | Approval of Structural Product/Material Submittal Schedule 50% | 19-Aug-26 |
| EN144 | Preparation & Submission of Structural Design 90% | 19-Aug-26 |
| EN163 | Preparation & Submission of BIM Model 90% | 03-Sep-26 |

## Key Programme Dates

- 50% Design (Arch, Structural, MEP, Electrical, ICT): 19-Jul-26 to 13-Aug-26
- Specialized Designs (Showcase, Graphic, Lighting, AV): 27-Jul-26 to 30-Jul-26
- 90% Design: 19-Aug-26
- BIM Model 90% + Clash Detection: 03-Sep-26
- IFC: After 90% approval (~Sep-26)

## Mapping Convention

The schedule treats 50% DD as one package per discipline (not per floor). The submission plan breaks it by floor. When mapping:

1. **All floor-level DD items** under the same discipline map to the same activity ID (e.g. all Basement, LGF, GF, 1F architectural items -> EN108)
2. **All structural items** (BOD, loading, analysis, gallery) map to EN102
3. **Specialized designs** (showcase, graphic, lighting, AV) map to their own activity IDs
4. **Material submittals** map to the product/material schedule activity (EN104/EN110)
5. **BIM models** map to BIM activities (EN103/EN109/EN163)
6. **IFC packages** map to the 90% design activity (EN144)

## Pitfalls

- The schedule's "Finish" date is the baseline completion. Actual progress may differ — check the "Actual Finish" column.
- Some submission plan items (e.g. FF&E layout, Life Safety) may not have a corresponding schedule activity. Leave the Linked Activity ID blank or mark "TBC".
- The schedule uses Oracle P6 format. PDF exports may have garbled column alignment — extract with pdftotext and grep for activity IDs.
- When a scope is split into a separate register (e.g. Rigging), the separate register should also get its own activity IDs from the schedule.
