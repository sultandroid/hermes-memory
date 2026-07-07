# Schedule Data Keys Reference

Actual keys found in `materials.json` per schedule type. Always verify against `materials.json`, not the raw schedule JSON files — casing differs.

## finishes_schedule
- `Exhibition Element Component` — where it's used
- `finish` (lowercase) — NOT `Treatment/Finish`
- `colour` (lowercase) — NOT `Colour`
- `supplier` (lowercase) — NOT `Supplier`
- `Material Description` — main text
- `Material ID` — NOT present as key; use `code` field instead
- `Qty`, `Unit` — rarely populated
- `Oddy Testing` — museum certification

## setwork_schedule
- `Setwork ID` — code
- `Type` — category (Graphic Housing, Wall, Bench, etc.)
- `Exhibit Name` — which exhibit
- `Exhibition ID`
- `description` (lowercase!) — main text
- `Finishes` — comma-separated finish codes
- `Drawing Code Reference`

## showcase_schedule
- `Showcase Type`, `Showcase ID`
- `Exhibit Name`, `Exhibit Number`
- `Glass Thcikness` (note typo "Thcikness")
- `Ext. Width (mm)`, `Ext. Height (mm)`, `Ext. Depth (mm)`
- `Door Type`, `Integrated Plinth`, `Integral Lighting`, `Climate Control`
- `Anti-Reflective (AR) Glass Coating Req`, `No. of glass sides`
- `Lighting Level`, `Lock Type`, `Case Rating`, `Air Exchange Rate (AER)`

## graphic_schedule
- `Graphic ID`, `Graphic Type`
- `Gallery Name`
- `Height (mm)`, `Width (mm)`
- `substrate` (lowercase!) — NOT `Susbtrate`
- `Print Method`, `Qty`
- `description` (lowercase!) — main text
- `Substrate Details`, `Exhibit ID`

## wayfinding_schedule
- `Wayfinding ID`, `Wayfinding Type`
- `Floor Location`, `Gallery Name`
- `Height (mm)`, `Width (mm)`
- `substrate` (lowercase!) — NOT `Susbtrate`
- `Print Method`, `Qty`
- `description` (lowercase!) — main text

## ff_e_schedule
- `FF&E ID`, `Space Name`
- `Finish`, `QTY` (uppercase!)
- `supplier` (lowercase)
- `Bespoke Dimensions`, `FF&E Dimensions`
- `Notes`, `Existing Design`, `FF&E Replacement`

## av_equipment_schedule
- `ref` (code), `description`, `product`, `category`, `qty`
- `dimensions`, `power_watts`, `voltage`, `zone`

## lighting_schedule
- `fixture_type`, `description`, `manufacturer`
- `lamp_type`, `wattage`, `cct`, `cri`
- `room`, `mounting`, `quantity`, `control_zone`
- `beam_angle`, `dimming`, `drawing_ref`, `floor`, `ip_rating`, `lumens`, `notes`, `total_power`, `unit`, `voltage`, `finish`

## object_schedule
- `Object/artwork name`, `Artist`, `Date`, `Sub-theme`
- `Height`, `Width`, `Depth`, `Diameter`, `Weight`
- `Display Method`, `Mount type`, `Medium`, `Materials`
- `Exhibit Name`, `Exhibit ID`, `Showcase ID`
- `Conservation requirements`, `Curatorial Notes`
- `Frame Type`, `Frame indicated in drawing`, `Hung`

## media_schedule
- `Media ID`, `Media Title`, `Media type`
- `Duration`, `Dwell time`, `Sound Y/N`
- `Media Purpose Description`, `Indicative Hardware`
- `Content Research Requirements`, `Assets required`
- `Exhibit name`, `Exhibit ID`

## exhibit_schedule
- `Exhibit ID`, `Exhibit Name`, `Gallery ID`
- `Exhibit Description`, `Exhibit Key Message`, `Outcomes`
- Reference IDs: `Art Commission ID`, `Graphic ID`, `Media ID`, `Object ID`, `Setworks ID`, `Showcase ID`, `Tactile/Manual ID`, `Model/Replica ID`

## art_commission_schedule
- `Art Commission ID`, `Art Commission Title`, `Artist Name`
- `Date`, `Dimensions`, `Materials`
- `Commission Description` — main text
- `Gallery ID`, `Exhibit ID`, `Exhibit Name`
- `Media Schedule`, `Status`

## tactile_schedule
- `Tactile / Manual Interactive ID`, `Tactile / Manual Title`
- `Tactile/Manual Type`, `Exhibit Name`, `Gallery ID`
- `Purpose / Description`, `Messages`, `Outcomes`
- `Content Research Requirements`

## asset_schedule
- `Asset ID`, `Asset Type`, `Application`
- `description` (lowercase!) — main text
- `Collection Origin`, `Copyright status`, `Qty`
- `Role in story`, `Exhibit Name`, `Gallery ID`
- `Available format and quality`, `Internal or External asset`

## model_schedule
- `Model/Replica ID`, `Type`, `Purpose / Description`
- `Exhibit Name`, `Exhibit ID`, `Gallery ID`
- `Content Research Requirements`

## mockups_prototypes_schedule / mockups_prototypes_graphic_schedule
- `Mockup code`, `Description`, `Gallery`, `Size`, `Notes`
- `#` (line number), `Image`, `Re-Use`

## space_gallery_schedule
- `Space ID`, `Exhibit list`
- `Gallery Key Messages`, `Visitor Experience Description`
- `Collection Interpretation Statement`
