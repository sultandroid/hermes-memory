# Batch Downloads Sort — Keyword Classifiers for Samaya BIM Projects

> Reference for mass-file-organization of `~/Downloads/` content into BIM Unit project folders.
> Updated May 2026 — added folder-level sorting, Aseer doc code routing, Private & Shared handling.

## Strategy

For **individual file batches** (50+ files), write a Python script that:
1. Scans source directory for all files
2. SHA256-hashes each to detect exact duplicates at source
3. Classifies by keyword (project name, doc code, supplier name) against known project folders
4. Moves to correct BIM project subfolder
5. Removes duplicates, temp files, archives non-essentials

For **folder batches** (folders from Downloads or OneDrive Shared), use a separate pass:
1. Classify each folder by name into a project
2. Check if destination folder already exists — if so, **merge** contents (skip identical files, move new/changed ones)
3. For unknown folders (Private & Shared N), inspect contained filenames to determine project routing
4. Clean up empty source folders after merge

For individual files (1-5), use direct classification logic.

## Duplicate Detection

```python
# Exact duplicate detection at source BEFORE moving
by_size = {}
for f in files:
    sz = os.path.getsize(f)
    by_size.setdefault(sz, []).append(f)

for sz, flist in by_size.items():
    if len(flist) > 1:
        for f in flist:
            h = hashlib.sha256(open(f,'rb').read()).hexdigest()
            for other in flist:
                if other <= f: continue
                h2 = hashlib.sha256(open(other,'rb').read()).hexdigest()
                if h == h2: # duplicate pair found
```

Common patterns: `filename (1).ext` == `filename.ext`, `filename (1) (1).ext` == `filename (1).ext`, `filename 2.docx` == `filename.docx`

## Project Classification Keyword Tables

### Aseer-Museum
Keywords: `aseer`, `asher`, `aser`, `nrs`, `moc-aseer`, `moc-mus-ase`, `10003521`, `a2742`, `nrs-sam`, `nrs_portfolio`, `freestanding`, `stair with 2 flight`, `audio visual system`, `fire alarm package`, `basement expansion`, `core samples`, `si-cg-aseer`, `si 02-310326`, `td-roof-01/02/03`, `purchase order - p00737`, `power supply - exterior`, `power- elm`, `data- elm`, `sultan@samayainvest`, `showcase drawing`, `type 4/6a/1/5a`, Arabic `متحف عسير`

**Folder patterns** (folders from Downloads, not individual files):
- `07_Public Address` → `Design Files (Stage 04)`
- `18-3-2026 1st floor drawing` / `18-3-2026 1st floor drawing 2` → `Design Files (Stage 04)` (AV layouts)
- `2_Galleries & Auxiliary Spaces_rev A` → `Design Files (Stage 04)`
- `BASSEM HANBALA 24-3-2026` → `Design Files` (Architect presentation)
- `Existing Expansion Joint` → `As-Built Docs`
- `Submittal NN MM-DD-YYYY` → `Submittals/`
- `nissenrichardsstudio_a2742-1160-dwg*` → `Design Files (Stage 04)` (NRS drawing delivery — 55 subdirs)
- `nissenrichardsstudio_a2742-1800-dwg*` → `Design Files (Stage 04)`
- `nissenrichardsstudio_nrs_samaya_sabic_50_concept_proposal*` → `Design Files`
- `download (N)` → `HR/CVs` (recruitment platform CV batches, 25 each)

### Zamzam Museum / Kaaba Kiswa
Keywords: `زمزم`, `zamzam`, `كسوة الكعبة`, `كعبة`, `خزانة ثوب`, `خزائن`, `goppion textile`, `hasenkamp`, `ghm-sam-zz`, `جدول أعمال رقم`, `دليل إدارة التركيبات`, `مقترح دليل اداره التركيبات`, `وثيقة الاعتماد العام`, `العروض_الفنية_*, العروض_الفنية_المصححة`, `تقييم_فائدة_العروض_الفنية`, `تقرير_الترابط_بين_مشروعي_كسوة`, `تحليل_مشاكل_العروض`

**Also routes to Zamzam** (Urwa Bin Zubair is part of Zamzam project area):
- `عروة بن الزبير`, `عروة`, `urwa`, `قصر عروة`, `مركز عروة` → `Design Files`
- `4-6 Final مخططات عروة*` → `Design Files` (Urwa palace plans)
- `الخزائن*` (cabinet inventories) → `Design Files`
- `عرض قصر عروة التاريخي*` → `Design Files`
- `عينات للتصنيع` (manufacturing samples folder) → `Design Files`

### Ryadh Museum (Rakah Center)
Keywords: `الراكة`, `راكة`, `rakah`, `مركز زوار الراكة`, `مركز زوار قرية ذي عين`, `مركز.*الأثري`, `الأثري`

### El-Ghamama Museum
Keywords: `الغمامة`, `ghamam`, `qahwtna`, `سيد الشهداء`, `sada uhud`, `أحد`, `الخطة_التشغيلية_لمتحف_حكاية_أحد`

### Hera' Ghar (Mosque Models)
Keywords: `حراء`, `hera`, `ghar`, `جبل النور`, `jabal al-noor`, `mvii`, `mosque model`, `masjid al-haram`, `rfp_high-precision_mosque_models`

### Other Projects
- Khair El-Khalq: `خير الخلق`, `khair el-khalq`, `تكلفة تشطيب`
- Masjid Alnoor: `مسجد النور`, `masjid alnoor`, `عقد_مسجد_النور`
- Hadaya_Teiba: `هدايا طيبه`, `hadaya`, `teiba`
- Prime Business Resort: `prime business`, `منتجع`, `resort`

## Aseer Subfolder Routing
- SI, site instruction → `Docs/05_SIs`
- RFI, TQ, technical query → `Docs/04_RFIs`
  - `MOC-ASEER-SIC-1A0-TQ-*` → `Docs/04_RFIs` (TQ = Technical Query)
- Quotation, purchase order, contract → `Contracts`
- Submittal, type, showcase, stair, AV, fire alarm → `Submittals`
- Invoice → `Invoices`
- DMP, plan, procedure, MOS → `Docs/02_Plans_and_Procedures`
  - `MOC-ASEER-SIC-1K0-PL-*` (PL = Plan, e.g. SMP, CRP, DMP, BEP) → `Docs/02_Plans_and_Procedures`
- BOQ → `B.O.Q`
- Report, meeting → `Reports & Meeting`
- Register, log → `Docs/09_Registers`
  - `MOC-ASEER-SIC-*K0-ZD-*` / `-*A0-ZD-*` (ZD = Document register) → `Docs/09_Registers`
- A2742 drawing, model, power supply, TD-ROOF, wayfinding → `Design Files (Stage 04)`
- As-built → `As-Built Docs`
- Email, inbox, gmail, eml → `Correspondence`
- Contract_Samaya_NRS* → `Contracts` (NOT SI)
- Phase_2_3_4_Design_Requirements → `Design Files (Stage 04)` (NOT SI)
- WAY FINDING SIGNAGE → `Design Files (Stage 04)` (NOT SI)
- RE: Aseer Museum - Discussion Updated SoW → `Correspondence` (NOT SI)
- Inbox* sultan@samayainvest → `Correspondence`

## Folder Merge Pattern

When a source folder already has content in the destination:

```python
def safe_move_dir(src, dst, new_name=None):
    name = new_name or os.path.basename(src)
    dst_path = os.path.join(dst, name)
    if os.path.exists(dst_path):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst_path, item)
            if os.path.exists(d):
                if os.path.isfile(s) and os.path.isfile(d):
                    # Same size + content check → skip
                    if os.path.getsize(s) == os.path.getsize(d):
                        continue
                    else:
                        stem, ext = os.path.splitext(item)
                        d = os.path.join(dst_path, f"{stem}_from_source{ext}")
                elif os.path.isdir(s) and os.path.isdir(d):
                    # Recurse merge subdirectories
                    safe_move_dir(s, d)
                    continue
            shutil.move(s, d)
        os.rmdir(src)  # clean up
    else:
        os.makedirs(dst, exist_ok=True)
        shutil.move(src, dst_path)
```

Used when: previous batches already deposited some files in the target directory, and a new batch adds more from the same source (e.g. NRS drawing deliveries).

## Samaya Corporate Routing
Use as fallback when no project matches: Company Profile, HR, Procurement, Licenses & Certificates, Factory Operations, QHSE, IT, Proposals, Procedures, Specifications, Estimations, Finance, Legal, Contractors, Meetings, Document Control, Templates, Technical, Scans, FF&E

**Folder patterns** (not individual files):
- `مقاول الأعمال المدنية والبنية التحتية` → `Contractors`
- `مواصفات_شبابيك_الحماية_الفورفورجيه` → `Specifications`
- `IT Feature Request Form*` → `IT`
- `Profiles Photos` → `Company Profile`
- `RFQ_Tents_Contractor` → `Contractors`
- `technical Proposal` → `Proposals`
- `OneDrive_4_17-03-2026` → `Finance` (bank/CR docs)
- `samaya-profile-v2` → `Company Profile`
- `Electrical` / `Electrical 2` → `HR` (CVs folder)
- `wetransfer_esnad*` → `_Archive/_from_Downloads_Folders/Esnad_Media_Tech/`

## Private & Shared Folder Content Inspection

OneDrive Shared folders (`Private & Shared`, `Private & Shared N`, `Private & Shared N_1`) contain mixed files. Inspect contained filenames to route:

| File pattern found inside | Route to |
|---|---|
| `كسوة`, `كعبة` | Zamzam Museum / Docs |
| `Samaya Factory Profile` | Samaya / Company Profile |
| `حوكمة` (governance) | Samaya / IT |
| `منافسة`, `كرنفانات` (competition) | Archive / Samaya_Misc |
| `العرض الفني` (technical offer) | Samaya / Proposals |
| `أثير`, `Atheer`, `مطل` | Archive / Samaya_Misc |
| `Tender`, `متابعة المهام` | Samaya / Procurement |
| `عرض أسعار`, `سعر` (pricing) | Samaya / Estimations |
| `UTILITIES` | Samaya / Factory Operations |
| `RFQ`, `طلب عرض سعر` | Samaya / Procurement |
| `الفريق الهندسي` (engineering team) | Samaya / HR |
| `دورة حياة مشروع المتحف` | Samaya / Procedures |
| No specific match | Archive / Samaya_Misc

## Edge Cases
1. **Leading spaces** in filenames — always `.strip()` the keyword search string
2. **Temp Office files** — `~$` prefix = delete immediately
3. **Personal/kid files** — school projects → archive to `_Archive/_from_Downloads_Documents/Personal/`
4. **Unrelated files** — historical/cultural/festival docs → archive to `_Archive/_from_Downloads_Documents/Samaya_Misc/`
5. **Arabic with control chars** — Some filenames contain `‎⁨` (LRM) and `⁩` (PDF) — strip or handle in regex
6. **Overly broad catch-all** — corporate keywords checked LAST, project-specific first
7. **Trailing spaces in folder names** — `عينات للتصنيع ` → use `.strip()` before matching
8. **OneDrive Shared folders** (`Private & Shared*`) — inspect contents for routing, don't rely on folder name alone
9. **CV download batches** (`download (N)`) from recruitment platforms — route to `HR/CVs/`, not design or procurement. Each batch is 25 PDFs with auto-generated filenames. `download (1)` and `(2)` have different content despite similar file naming
10. **NRS drawing deliveries** (`nissenrichardsstudio_a2742-1160-dwg_*`) — large folder structures with 50+ drawing subdirectories. Merge with existing rather than replace
11. **SBC1001 / protectedpdf.com WebViewer cache** — browser cache folders, not project content. Archive immediately
12. **Screen recordings** (`.mov` files on Desktop) — not project content, leave in place

## Pitfalls
- **OneDrive file locks**: `Resource deadlock avoided` means sync engine holds lease. Work on local copies.
- **New Excel files**: NEVER create new xlsx files. Only append to existing ones.
- **rm -rf**: NEVER use on any path. File-level `rm <filename>` only.
