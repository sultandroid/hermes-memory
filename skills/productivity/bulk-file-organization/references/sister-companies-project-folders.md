# Sister Companies — Project Folder Setup

## Context

The `Reports/Sister_Companies/` folder holds files for multiple subsidiary/café/gift-shop projects. Each project gets its own subfolder named in English.

## Source data pattern

The user provides a **numbered list** mapping project # → Arabic name:
```
متجر ١ الوحي              → Store 1 - Al Wahi
متجر ٢ القران الكريم      → Store 2 - Holy Quran
كافيه١ - قهوتنا           → Cafe 1 - Qahwatna
كافيه ٢ - حراء كافيه      → Cafe 2 - Hira Cafe
متجر ٣ جبل عمر            → Store 3 - Jabal Omar
متجر ٤ - الصافيه          → Store 4 - Al-Safiya
متجر ٥ - متحف خير الخلق   → Store 5 - Khair Al Khalq Museum
كافيه ٣ - الصافيه         → Cafe 3 - Al-Safiya
متجر ٦ - تذكارات          → Store 6 - Tzkarat
متجر ٧ - رطيب             → Store 7 - Rateeb
كافيه ٤ - القهوه النجدية  → Cafe 4 - Najdi Coffee + Ice Coffee Store
```

## Workflow

### 1. Rename Arabic files → English (if not already done)

Scan the root for Arabic-named `.xlsx`/`.docx`/`.xls` files and rename:
- `mv "تكاليف متجر تذكارات.xlsx" "Tzkarat_Store_Costs.xlsx"`
- Use `mv` directly (small batch, <20 files)
- Prefix: `Store_Costs`, `Coffee_Shop`, `Purchasing-Orders`, `tasks`

### 2. Create project folders from numbered list

For each item in the user's numbered list, `mkdir -p` an English folder name:
- `متجر ١ الوحي` → `Al_Wahi_Store`
- `متجر ٢ القران الكريم` → `Holy_Quran_Store`
- `كافيه١ - قهوتنا` → `Qahwatna` (check if already exists)
- `كافيه ٢ - حراء كافيه` → `Hira_Cafe`
- `متجر ٣ جبل عمر` → `Jabal_Omar_Stores`
- `متجر ٤ - الصافيه` → `As_Safiyyah_Giftshop`
- `متجر ٥ - متحف خير الخلق` → `Khair_Al_Khalq_Museum_Store`
- `كافيه ٣ - الصافيه` → `Qahwatna_Al_Safiya`
- `متجر ٦ - تذكارات` → `Tzkarat`
- `متجر ٧ - رطيب` → `Rateeb`
- `كافيه ٤ - القهوه النجدية + ice coffe store` → `Cafe_4_Najdi_Coffee_and_Ice_Coffee`

**Naming conventions:**
- Underscores, not spaces
- PascalCase for multi-word names (`As_Safiyyah_Giftshop`)
- Cafe 4 with two sub-brands → merge into one combined folder
- Keep existing folders that aren't in the numbered list but existed before (flag them to the user)

### 3. Search for related files in other locations

After creating folders, search **Downloads** and the parent **Reports/** directory for files matching any project keyword:
```bash
find "$DOWNLOADS" -maxdepth 1 -type f ( -iname "*quran*" -o ... )
find "$REPORTS" -maxdepth 2 -type f ( -iname "*حراء*" -o ... )
```

Keywords to try for each project:
| Project | Search keywords |
|---------|----------------|
| Al Wahi | `وحي`, `wahy`, `wah` |
| Holy Quran | `قران`, `quran`, `kareem` |
| Hira Cafe | `حراء`, `hira` |
| Khair Al Khalq Museum | `خير`, `خلق`, `khair`, `khalq`, `museum` |
| Najdi Coffee | `نجد`, `najdi` |

Also check for `-STORE-` and `-SHOP-` in filenames (JN reference number pattern).

### 4. Move files into project folders

```
mv "$DOWNLOAD/JN-Quaran-Kareem-Shop-Status-Report.docx" "$BD/Holy_Quran_Store/"
```

### 5. Report the final mapping

Present as a table mapping the user's numbered list → folder name → files present. Flag empty folders and extra folders not in the numbered list.

## Edge cases

- **Combined cafe/store projects**: When the numbered list groups two brands under one item (e.g. "القهوه النجدية + ice coffe store"), create ONE combined folder and move existing subfolders into it (e.g. `Ice_Coffee_Store/` → `Cafe_4_Najdi_Coffee_and_Ice_Coffee/`)
- **Pre-existing extra folders**: `Saudi_Coffee`, `Tayyiba_Gifts_Jabal_Noor`, `Cybrani`, `_Management` — these exist but weren't in the numbered list. Flag them to the user and ask for disposition.
- **OneDrive folder disappearance**: Sometimes newly created folders seem to vanish (OneDrive race). Re-check with `ls` after creation.
- **Temp/lock files**: `~$` prefix files are Office temp files — ignore them during search.
