# Info Card Field Group Design for Material Hotspots

## Field Group Pattern

Each schedule type needs field group definitions showing the most relevant fields in compact 2-3 groups:

```typescript
const SCHEDULE_FIELD_GROUPS: Record<string, { label: string; fields: FieldDef[] }[]> = {
  'finishes_schedule': [
    { label: 'Material', fields: [
      { key: 'code', label: 'ID', mono: true },
      { key: 'finish', label: 'Finish' },
      { key: 'colour', label: 'Colour' },
    ]},
    { label: 'Specifications', fields: [
      { key: 'Material Description', label: 'Description', full: true },
      { key: 'supplier', label: 'Supplier' },
    ]},
  ],
};
```

## Rules
- `mono: true` for codes/IDs (IBM Plex Mono font)
- `full: true` for long text fields (span both grid columns)
- 2-3 groups max per type, 2-4 fields per group
- Show description/main text prominently

## ⚠ Key Casing Pitfall
The unified `materials.json` uses LOWERCASE keys (`description`, `finish`, `colour`, `supplier`, `substrate`) while individual schedule JSON files use Title Case (`Description`, `Finish`). The app reads from `materials.json`, so keys MUST match that file's casing. Sub-agents often read the schedule JSON files and get the casing wrong — always verify against `materials.json` directly.

## Clean Name Utility
Strip dimensions from material descriptions for info cards. Regex patterns:
1. Leading dimension: `^\d+ x \d+mm`, `^3500(w) x 4000(h) x 400(d)mm`
2. Leading "Nx ": `^8x `, `^3x `
3. Leading thickness: `^3mm thick `
4. Trailing/middle dims: ` - 450 x 2000mm`, ` - 172mm x 304mm`
5. Embedded dims: ` / 286 x 205mm`
6. Trailing mm specs: ` 1000mm$`

## Schedule Column Cleanup
Auto-hide columns with placeholder values:
```typescript
['#VALUE!','#VALUE','n/a','N/A','TBC','TBD','None'].includes(String(v).trim())
```
Filter image/thumbnail columns that only contain placeholders.

## Active Schedules Filtering
Only load schedule types relevant to current presentation stage:
```typescript
const ACTIVE_SCHEDULES = ['finishes_schedule','setwork_schedule','showcase_schedule',...];
const matMap = new Map(mats.filter(m => ACTIVE_SCHEDULES.includes(m.schedule_key)).map(m => [m.code, m]));
```
Also filter the Schedule table dropdown to match.