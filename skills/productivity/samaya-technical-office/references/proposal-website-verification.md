# Proposal Experience Verification Against Company Website

## When to Use
When a tender proposal (Section 8 or similar) lists "relevant experience / projects" — cross-reference each claimed project against the company's official website.

## Why
The user explicitly requires credibility checks. Fabricated or exaggerated project claims damage the company's reputation if an evaluator checks the public website and finds no trace. This step catches:
- Projects that don't exist on the public portfolio
- Client names that contradict what the website states
- Year/date mismatches
- Projects done through subsidiaries that should be credited differently

## How

### Step 1: Extract the website's public portfolio
```python
# Browse the company website
url = "https://samayainvest.com"
# Extract project list from homepage / portfolio page
```

### Step 2: Build a cross-reference table
For each project in the proposal:

| Status | Meaning |
|--------|---------|
| ✅ Match | Project appears on website with matching description |
| ⚠️ Not found | Project not on website — may be current/unpublished or fabricated |
| 🔴 Missing | Real project on website that SHOULD be in proposal but isn't |

### Step 3: Flag risks
- **"Private" client projects** (no public client name) are inherently unverifiable — flag these in the discrepancy report
- **Current projects** (e.g., "2025–") may not be on the website yet — note this but don't flag as critical
- **Subsidiary projects** — work done through subsidiaries (Rawasin, Graphit, Eventech, CCM) may not appear on the parent company website. Verify the subsidiary's own portfolio instead.

### Step 4: Report findings to the user
Present as a clean table with:
- ✅ Projects that match
- ⚠️ Projects NOT found on website
- 🔴 Projects on website MISSING from proposal
- Clear recommendation: add missing verifiable projects, remove or provide evidence for unverifiable ones

## Samaya Investment-Specific Portfolio
From samayainvest.com (verified June 2026):

### Projects on website:
1. **متحف القرآن الكريم** (Holy Quran Museum) — 2023
2. **متحف الجوف** (Al-Jouf Museum) — 2022
3. **متحف وبستان الصافية** (Al-Safiyah Museum & Orchard) — 2021
4. **معرض أصحابي** (Companions Exhibition) — 2023
5. **معرض الخلق العظيم** (Prophet's Character Exhibition)
6. **معرض "حكايا علم" التفاعلي** (SFDA Interactive Exhibition) — 2025
7. **متحف خير الخلق ﷺ** (Madinah Museum) — 2025
8. **فعاليات مكة تعايدنا** (Hira Cultural District Events)
9. **جناح شركة فمتك** (FM Facility Management Booth) — 2025

### Subsidiaries (separate portfolios):
- Technosign (est. 1999) — printing and digital tech
- Rawasin (est. 2000) — AV production
- Graphit (est. 2003) — visual identity and design
- Eventech (est. 2005) — events and conferences
- CCM (est. 2013) — museum planning and content
- Tawator (est. 2016) — digital marketing

### Partners listed on website:
وزارة الثقافة • وزارة السياحة • الهيئة العامة للغذاء والدواء • شركة علم • برنامج خدمة ضيوف الرحمن • الهيئة الملكية لمدينة مكة المكرمة والمشاعر المقدسة • أمانة منطقة المدينة المنورة • أمانة منطقة الرياض • هيئة التراث
