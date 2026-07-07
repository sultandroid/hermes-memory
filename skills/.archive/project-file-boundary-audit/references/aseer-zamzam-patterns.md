# Aseer ↔ Zamzam Cross-Contamination Patterns

## NRS Showcase Drawings (Aseer → Zamzam)

### File Identification
Pattern: `Freestanding Case-Type {N}- ID.Nr. {NN}.NN_SC_01_NRS_comments_*.pdf`

Known mismatches:
- **Type 2, ID.Nr. 08.03** — Freestanding Case Type 2 / Cabinet 8
  - `2026-04-21_Freestanding Case-Type 2- ID.Nr. 08.03_SC_01_NRS_comments_260421_stamped.pdf`
  - This is **Aseer Museum Submittal 07**, NOT Zamzam

### Why It's Aseer
1. **NRS** (Nissen Richards Studio) is Aseer's exhibition designer only
2. **SC_01** = NRS Showcase drawing sheet numbering (Aseer discipline 1800)
3. **Type 2 / ID Nr. 08** = NRS showcase type taxonomy, specific to Aseer
4. Drawing prefix **A2742-18xx** matches Aseer's 1800_Showcases folder structure
5. Zamzam has no NRS involvement — its showcase vendors are GHM, Goppion, Hasenkamp

### File in Zamzam Folder
`Zamzam Museum/Design Files/8-2025 مستود الدعاية مشترك مع الخزائن.pdf`
- Name references "8-2025" (possible Cabinet 8) and "الخزائن" (cabinets)
- May contain the same NRS showcase drawings

### How to Scan
```bash
# Search Zamzam folders for Aseer patterns
find "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Zamzam Museum" \
  -type f \( -iname "*NRS*" -o -iname "*SC_01*" -o -iname "*Type 2*" -o -iname "*A2742*" \) 2>/dev/null

# Check file sizes (0 = OneDrive stub, needs sync)
ls -laS "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Zamzam Museum/Design Files/" | grep -E "(NRS|SC_|Type|A2742|خزائن)"
```

## Other Known Cross-Contaminations
- *(Add patterns here as discovered)*
