# Info Card Field Group Definitions

Complete `SCHEDULE_FIELD_GROUPS` for schedule types. Each group defines what fields show in the hotspot tooltip info card.

## Important: No "Exhibit Name" in Setwork/Showcase

`Exhibit Name` was removed from `setwork_schedule` and `showcase_schedule` because the NRS source data uses **gallery theme names** (e.g., "Landscape", "Architecture & Landscape") rather than actual exhibit names, which confused users seeing "Exhibit: Landscape" on a setwork info card. Keep `Exhibition ID` if reference is needed — it's less ambiguous.

## finishes_schedule
```typescript
'finishes_schedule': [
  { label: 'Material', fields: [
    { key: 'code', label: 'ID', mono: true },
    { key: 'Exhibition Element Component', label: 'Component' },
    { key: 'finish', label: 'Finish' },
    { key: 'colour', label: 'Colour' },
  ]},
  { label: 'Specifications', fields: [
    { key: 'Material Description', label: 'Description', full: true },
    { key: 'supplier', label: 'Supplier' },
  ]},
],
```

## setwork_schedule
```typescript
'setwork_schedule': [
  { label: 'Setwork', fields: [
    { key: 'Setwork ID', label: 'ID', mono: true },
    { key: 'Type', label: 'Type' },
    { key: 'Exhibition ID', label: 'Exhibition ID' },
  ]},
  { label: 'Details', fields: [
    { key: 'description', label: 'Description', full: true },
    { key: 'Finishes', label: 'Finishes', full: true },
    { key: 'Drawing Code Reference', label: 'Drawing Ref' },
  ]},
],
```

## showcase_schedule
```typescript
'showcase_schedule': [
  { label: 'Showcase', fields: [
    { key: 'Showcase Type', label: 'Type' },
    { key: 'Showcase ID', label: 'ID', mono: true },
  ]},
  { label: 'Display', fields: [
    { key: 'No. of glass sides', label: 'Glass Sides' },
    { key: 'Anti-Reflective (AR) Glass Coating Req', label: 'AR Coating' },
    { key: 'Integral Lighting', label: 'Lighting' },
    { key: 'Climate Control', label: 'Climate' },
  ]},
],
```

## graphic_schedule
```typescript
'graphic_schedule': [
  { label: 'Graphic', fields: [
    { key: 'Graphic ID', label: 'ID', mono: true },
    { key: 'Graphic Type', label: 'Type' },
    { key: 'Gallery Name', label: 'Gallery' },
    { key: 'Exhibit ID', label: 'Exhibit ID' },
  ]},
  { label: 'Specifications', fields: [
    { key: 'Height (mm)', label: 'Height (mm)' },
    { key: 'Width (mm)', label: 'Width (mm)' },
    { key: 'substrate', label: 'Substrate' },
    { key: 'Substrate Details', label: 'Substrate Detail' },
    { key: 'Print Method', label: 'Print Method' },
  ]},
  { label: 'Details', fields: [
    { key: 'description', label: 'Description', full: true },
    { key: 'Qty', label: 'Qty' },
  ]},
],
```

## wayfinding_schedule
```typescript
'wayfinding_schedule': [
  { label: 'Wayfinding', fields: [
    { key: 'Wayfinding ID', label: 'ID', mono: true },
    { key: 'Wayfinding Type', label: 'Type' },
    { key: 'Floor Location', label: 'Floor' },
    { key: 'Gallery Name', label: 'Gallery' },
  ]},
  { label: 'Specifications', fields: [
    { key: 'description', label: 'Description', full: true },
    { key: 'Height (mm)', label: 'Height (mm)' },
    { key: 'Width (mm)', label: 'Width (mm)' },
  ]},
  { label: 'Materials', fields: [
    { key: 'substrate', label: 'Substrate' },
    { key: 'Print Method', label: 'Print Method' },
    { key: 'Qty', label: 'Qty' },
  ]},
],
```

## ff_e_schedule
```typescript
'ff_e_schedule': [
  { label: 'FF&E Item', fields: [
    { key: 'FF&E ID', label: 'ID', mono: true },
    { key: 'Space Name', label: 'Space' },
    { key: 'Finish', label: 'Finish' },
    { key: 'QTY', label: 'Qty' },
    { key: 'Bespoke - Qty', label: 'Bespoke Qty' },
  ]},
  { label: 'Details', fields: [
    { key: 'supplier', label: 'Supplier' },
    { key: 'Bespoke Dimensions', label: 'Bespoke Dims', full: true },
    { key: 'FF&E Dimensions', label: 'FF&E Dims', full: true },
    { key: 'Notes', label: 'Notes', full: true },
  ]},
],
```

## av_equipment_schedule
```typescript
'av_equipment_schedule': [
  { label: 'Equipment Info', fields: [
    { key: 'code', label: 'ID', mono: true },
    { key: 'ref', label: 'Ref', mono: true },
    { key: 'description', label: 'Description', full: true },
    { key: 'product', label: 'Product' },
    { key: 'category', label: 'Category' },
    { key: 'qty', label: 'Qty' },
  ]},
  { label: 'Specifications', fields: [
    { key: 'dimensions', label: 'Dimensions' },
    { key: 'power_watts', label: 'Power (W)' },
    { key: 'voltage', label: 'Voltage' },
    { key: 'zone', label: 'Zone', mono: true },
  ]},
],
```

## lighting_schedule
```typescript
'lighting_schedule': [
  { label: 'Fixture Info', fields: [
    { key: 'code', label: 'ID', mono: true },
    { key: 'description', label: 'Description', full: true },
    { key: 'manufacturer', label: 'Manufacturer' },
    { key: 'drawing_ref', label: 'Drawing Ref' },
    { key: 'dimensions', label: 'Size' },
  ]},
  { label: 'Lamp Specs', fields: [
    { key: 'fixture_type', label: 'Type' },
    { key: 'lamp_type', label: 'Lamp' },
    { key: 'wattage', label: 'Wattage (W)' },
    { key: 'lumens', label: 'Lumens' },
    { key: 'cct', label: 'CCT' },
    { key: 'cri', label: 'CRI' },
    { key: 'beam_angle', label: 'Beam Angle' },
    { key: 'total_power', label: 'Total Power' },
  ]},
  { label: 'Installation', fields: [
    { key: 'room', label: 'Room', full: true },
    { key: 'floor', label: 'Floor' },
    { key: 'mounting', label: 'Mounting' },
    { key: 'quantity', label: 'Qty' },
    { key: 'unit', label: 'Unit' },
    { key: 'control_zone', label: 'Control Zone', mono: true },
    { key: 'ip_rating', label: 'IP Rating' },
    { key: 'dimming', label: 'Dimming' },
    { key: 'finish', label: 'Finish' },
    { key: 'notes', label: 'Notes', full: true },
  ]},
],
```
