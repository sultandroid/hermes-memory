# Sidebar Material Grouping by Schedule Type

Group materials in the gallery sidebar legend by schedule type instead of a flat list.

## Implementation Pattern

Replace the flat `.map()` over `displayHotspots` with a grouping pass:

1. **Label map**: `schedule_key` → display name
2. **Group**: iterate hotspots, look up `mat.schedule_key`, push into group buckets
3. **Sort groups**: known types first in a specific order, then alphabetical
4. **Render**: group header badge + items with sequential numbering

```typescript
const GROUP_LABELS: Record<string,string> = {
  'finishes_schedule':'Finishes',
  'setwork_schedule':'Setwork',
  'showcase_schedule':'Showcase',
  'graphic_schedule':'Graphic',
  'wayfinding_schedule':'Wayfinding',
  'ff_e_schedule':'FF&E',
  'object_schedule':'Object',
  'exhibit_schedule':'Exhibit',
  'art_commission_schedule':'Art Commission',
  'media_schedule':'Media',
  'av_equipment_schedule':'AV Equipment',
  'lighting_schedule':'Lighting',
  'asset_schedule':'Asset',
  'tactile_schedule':'Tactile',
  'model_schedule':'Model',
  'mockups_prototypes_schedule':'Mockup',
  'mockups_prototypes_graphic_schedule':'Mockup (Graphic)',
  'space_gallery_schedule':'Space',
};
```

## Rendering

Each group header:
```tsx
<div style={{
  fontFamily:"'Inter',sans-serif", fontSize:'.5rem', fontWeight:600,
  textTransform:'uppercase', letterSpacing:'0.06em',
  color:'#C8A45C', background:'rgba(200,164,92,.08)',
  padding:'3px 8px', borderRadius:'3px', margin:'4px 0 2px',
}}>{label}</div>
```

Items follow the same pattern as ungrouped list (code + cleaned name + hover/pin).

## Known Order

```
['Finishes','Setwork','Showcase','Graphic','Wayfinding','FF&E','Object',
 'Exhibit','Art Commission','Media','AV Equipment','Lighting']
```

Items with unknown schedule_key fall to "Other" label and sort last, alphabetically.
