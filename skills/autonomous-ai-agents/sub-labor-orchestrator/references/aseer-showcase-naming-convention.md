# Aseer Museum — NRS Showcase / Cabinet Naming Convention

## Background
NRS (Nissen Richards Studio) designed the exhibition showcases for Aseer Museum (Project 3092). Their drawing codes and file naming patterns are **exclusive to Aseer** — if found in any other project folder (Zamzam, Tahakom, etc.), the files are misplaced.

## Detection Patterns

| Pattern | Example | Meaning |
|---------|---------|---------|
| `A2742-1800` through `A2742-1815` | `A2742-1800 type 01.pdf` | Showcase drawing series (1800_Showcases), 17 drawing sets |
| `SC_01` | `...SC_01_NRS_comments...` | Showcase drawing sheet — if seen in a non-Aseer folder, misplaced |
| `Freestanding Case-Type 2` | `Freestanding Case-Type 2- ID.Nr. 08.03_...` | Cabinet Type 2 = الخزائن نوع ٢ |
| `ID.Nr. 08` | `...ID.Nr. 08.03_SC_01...` | Cabinet ID 08 = الخزائن رقم ٨ |
| `NRS` in filename | `Block Diagram_NRS_260425_stamped.pdf` | NRS is the exhibition designer for Aseer only |
| `Submittal 07` / `Submittal 11` content | Showcase shop drawings in submittal 07 | Aseer submittal packages with showcase content |

## File Location (Canonical Copies)

```
Aseer-Museum/Docs/03_Submittals/
├── 2026-04-21_Freestanding Case-Type 2- ID.Nr. 08.03_SC_01_NRS_comments_260421_stamped.pdf
├── 2026-04-21_Submittal 07 04-21-2026.7z
├── 2026-04-22_Submittal 08 04-22-2026.7z
└── ... (other submittal packages)

Aseer-Museum/Completed Tender Package From NRS/06_Drawing_Source_Folders/1800_Showcases/
├── A2742-1800/  (Type 01)
├── A2742-1801/  (Type 01)
├── A2742-1802/ through A2742-1815/  (various showcase types)
└── A2742-1820/  (additional)
```

## Files Known to Be Misplaced

Found in `Zamzam Museum/Design Files/` but belong to Aseer:

- `8-2025 مستود الدعاية مشترك مع الخزائن.pdf` — references cabinet 8 (ID.Nr. 08)
- `الخزائن-8-2025.pdf` — references cabinet 8 (ID.Nr. 08)
- `Zamzam_Museum _SHOWCASES.pdf` (0-byte stub — verify on OneDrive)

## Action Protocol

When files matching any of the above patterns are found in a **non-Aseer** project folder:
1. Confirm the file is indeed Aseer property (check NRS reference, SC_ code, Type/ID naming)
2. Move to a quarantine location outside both projects (user preference: خارج المشاريع)
3. Notify the user with file names and detection evidence
4. Let user inspect before permanent placement
