# Material Sample Submittal Folders

When creating physical material sample folders (240×330mm) with QR codes linking to digital datasheets & test reports for client/consultant submittal:

1. **Load skill**: `sample-submittal-system` — covers naming convention, 24×33cm label design, QR generation, generate script
2. **Project submittal ref**: Every sample label carries its project document ref (e.g., `MOC-MUS-ASE-1A0-MA-0007` for Aseer Museum Material Approval #7)
3. **Critical pitfall**: Images must be embedded as **base64 data URIs** directly in `label.html` — file:// protocol + OneDrive cloud files make external image loading unreliable. Run the Python snippet from the skill's pitfall section or use the generate script which does this automatically.
4. **Register columns**: Code · Name · Type · Material · Submittal Ref · Project · Where to Use · Folder Size · Date · Status

## Aseer Museum Submittal Ref Format

`MOC-MUS-ASE-{ZONE}-{TYPE}-{NNNN}`

| Segment | Example | Meaning |
|---------|---------|---------|
| MOC | MOC | Muheel Oil Company (Client) |
| MUS | MUS | Museum project |
| ASE | ASE | Aseer |
| Zone | 1A0 | Zone 1A, Level 0 |
| Type | MA | MA = Material Approval, SD = Shop Drawing, RFI = Request for Information, FA = Finish Approval |
| Serial | 0007 | Sequential number |

## Related files

- `~/OneDrive.../Samaya/Samples/REGISTER.md` — master sample register
- `~/OneDrive.../Samaya/Samples/generate-new-sample.sh` — CLI scaffold
- `~/OneDrive.../Samaya/Samples/TEMPLATE-LABEL-24x33cm.html` — master label template (placeholders, not self-contained)
