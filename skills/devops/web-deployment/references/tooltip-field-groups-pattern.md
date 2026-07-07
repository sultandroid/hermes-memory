# Tooltip Field Groups — Dynamic Info Card Pattern

## Problem

A single tooltip card must display different fields for different material/schedule types (Showcase, Object, Graphic, Setwork, etc.). Each type has 5–35 unique fields. Hardcoding all fields per type bloats the component and is hard to maintain.

## Solution

Define a config object `SCHEDULE_FIELD_GROUPS` mapping each schedule key to an array of sections, each containing labeled fields. The card renders only non-empty fields.

## Config Shape

```typescript
interface FieldDef {
  key: string;         // field name in the material object
  label: string;       // display label in the card
  mono?: boolean;      // render value in monospace font
  full?: boolean;      // span full width (not 2-column)
}

// Keyed by schedule_key from materials.json
const SCHEDULE_FIELD_GROUPS: Record<string, { label: string; fields: FieldDef[] }[]> = {
  'showcase_schedule': [
    { label: 'Showcase Info', fields: [
      { key: 'Showcase ID', label: 'ID', mono: true },
      { key: 'Showcase Type', label: 'Type' },
    ]},
    { label: 'Glass & Glazing', fields: [
      { key: 'Glass Thcikness', label: 'Thickness' },
      { key: 'Number of Doors', label: 'Doors' },
    ]},
  ],
  'object_schedule': [
    { label: 'Object Info', fields: [
      { key: 'Object/artwork name', label: 'Name', full: true },
      { key: 'Artist', label: 'Artist' },
    ]},
    { label: 'Materials & Mounting', fields: [
      { key: 'Medium', label: 'Medium' },
      { key: 'Mount type', label: 'Mount' },
    ]},
  ],
  // ... remaining types
};
```

## Rendering Logic

```typescript
function renderFieldGroups(mat: any, schedKey: string): React.ReactNode {
  const groups = SCHEDULE_FIELD_GROUPS[schedKey];
  if (!groups) return renderGenericFields(mat);  // fallback for unknown types

  const rendered: React.ReactNode[] = [];
  for (const group of groups) {
    const populated = group.fields.filter(f => hasValue(mat, f.key));
    if (populated.length === 0) continue;  // skip empty sections

    rendered.push(
      <div className="htc-group" key={group.label}>
        <div className="htc-group-title">{group.label}</div>
        <div className="htc-group-grid">
          {populated.map(f => (
            <div className={`htc-group-field ${f.full ? 'full' : ''}`} key={f.key}>
              <span className="flbl">{f.label}</span>
              <span className={`fval ${f.mono ? 'mono' : ''}`}>{String(mat[f.key])}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return <div className="htc-groups">{rendered}</div>;
}
```

## Generic Fallback

For schedule types not in the config, show all non-standard fields in a simple label:value table:

```typescript
const BASE_FIELDS = new Set(['code','description','category','element','finish','colour','supplier','source','_source','schedule_key','thumbnail']);
function renderGenericFields(mat: any): React.ReactNode {
  const extras: { key: string; val: string }[] = [];
  Object.entries(mat).forEach(([key, val]) => {
    if (BASE_FIELDS.has(key)) return;
    if (hasValue(mat, key)) extras.push({ key, val: String(val) });
  });
  if (extras.length === 0) return null;
  return (
    <div className="htc-groups">
      <div className="htc-group">
        <div className="htc-group-title">Details</div>
        <div className="htc-generic-grid">
          {extras.map(({key,val}) => (
            <React.Fragment key={key}>
              <span className="glbl">{key}</span>
              <span className="gval">{val}</span>
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
}
```

## Field Value Cleanup

Always filter out empty/missing/spurious values:

```typescript
function hasValue(mat: any, key: string): boolean {
  const v = mat[key];
  if (v === undefined || v === null) return false;
  const s = String(v).trim();
  return s !== '' && s !== 'None' && s !== 'n/a' && s !== 'N/A' && s !== '#VALUE!' && s !== '#VALUE';
}
```

## CSS Classes

```
.htc-groups          — container for all field groups
.htc-group           — one group section
.htc-group-title     — section header (gold border-bottom accent)
.htc-group-grid      — 2-column CSS grid (label | value)
.htc-group-field     — single field pair
.htc-group-field.full — full-width field
.flbl                — field label (tiny, uppercase, muted)
.fval                — field value
.fval.mono           — monospace variant for codes/IDs
.htc-generic-grid    — fallback grid for unknown types
.glbl / .gval        — generic grid label/value
.htc-source-badge    — footer badge with schedule source
```
