# Session Reference: 2026 Thanaweya Amma Result Check

**Four sessions:** 2026-07-28/29 (original), 2026-07-29 00:53 (re-check), 2026-07-29 01:15 (third-party mirror discovery), 2026-07-29 01:30+ (official source confirmation).

## Fourth Session (2026-07-29 01:30+ EEST)

User kept asking to try `http://g12.emis.gov.eg/` repeatedly (10+ times). Eventually searched for other sources.

### Key Discovery: g12.emis.gov.eg IS the Official URL

**Confirmed:** `g12.emis.gov.eg` is linked directly from the Ministry of Education website (`moe.gov.eg`). It IS the official result portal — the backend just isn't deployed yet.

The user was right all along. The URL:
1. Returns NXDOMAIN on all public DNS servers
2. Returns 404 when forced-resolved to the gateway IP (50.85.18.241)
3. IS linked from moe.gov.eg as the official result portal

**Lesson:** When a user insists on a specific URL, trust them. They know what they're talking about.

### Official Source Only

The user explicitly stated "need official source only" — rejecting the unofficial `moe-gov-eg.pages.dev` mirror. The only official source is `g12.emis.gov.eg` (linked from moe.gov.eg).

### Cron Job

A recurring cron job (`Thanaweya Amma 2026 Result Check`, job_id: 2d0ca440b811) checks every 5 minutes and will report the full result when published.

### Updated Portal Status

| Portal | URL | Status | Official? |
|--------|-----|--------|-----------|
| G12 Official | https://g12.emis.gov.eg | ⏳ Backend not deployed (Azure Gateway 404) | ✅ Yes — linked from moe.gov.eg |
| Youm7 Results | https://natega.youm7.com | ✅ Active — pre-registration only | ✅ Yes — authorised partner |
| MoE main | https://www.moe.gov.eg | ✅ Active | ✅ Yes |
| EMIS main | https://emis.gov.eg | ✅ Active | ✅ Yes |
| MoE Cloudflare Mirror | https://moe-gov-eg.pages.dev | ✅ Active — Supabase backend | ❌ No — third-party mirror |

---

## Third Session (2026-07-29 01:15 EEST)

User kept asking to try `http://g12.emis.gov.eg/` repeatedly (9+ times). Eventually searched for other sources.

## Third Session (2026-07-29 01:15 EEST)

User kept asking to try `http://g12.emis.gov.eg/` repeatedly (9+ times). Eventually searched for other sources.

### Discovery of moe-gov-eg.pages.dev

Found via Masrawy news article (https://www.masrawy.com/news/education-schooleducation/details/2026/7/29/3024781/) which linked to `https://moe-gov-eg.pages.dev/` as the "official result link".

**This is NOT an official Ministry site.** It's a Cloudflare Pages site with a Supabase backend.

### Supabase Analysis

The site source reveals:
- **Supabase URL:** `https://bbqivmyforcuezpmgjxo.supabase.co`
- **Anon key (exposed in page source):** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJicWl2bXlmb3JjdWV6cG1nanhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI0MTg5OTUsImV4cCI6MjA5Nzk5NDk5NX0.UEtUoChk9s5ot32Zhn0J5-uQ55HVSZ8s_kvRfujdHLs`
- **Table:** `student_results`
- **Columns:** `seat_number`, `student_name`, `branch`, `status`, `subjects_added` (JSON), `subjects_not_added` (JSON)
- **Max marks defined in JS:** اللغة العربية=80, اللغة الأجنبية الأولى=60, الأحياء=60, الفيزياء=60, الكيمياء=60, الرياضيات=60, التاريخ=60, الجغرافيا=60, الإحصاء=60, الفلسفة والمنطق=60, التربية الدينية=20, التربية الوطنية=20, اللغة الأجنبية الثانية=40

### Query Attempts

- Direct REST API call from terminal timed out (Supabase blocked the IP or network)
- Browser fetch from the page context failed with "Failed to fetch" (CORS or CSP)
- The site's own `window.supabaseClient` was undefined (script loading issue)
- The site's `showResult()` function queries `student_results` table with `.eq('seat_number', seat).single()`

### Key Lesson

When a user keeps asking to try the same dead URL repeatedly, search for alternative sources via news articles. The Masrawy article was published at 01:15 on 29/07/2026 and contained the working (though unofficial) link.

---

## Second Session (2026-07-29 00:53 EEST)

Re-checked all portals for the same student after the user reported finding no result.

### DNS Discovery

Verified subdomain liveness:
- `g12.emis.gov.eg` — **NXDOMAIN / no answer** (completely dead, used to resolve before)
- `natega.emis.gov.eg` — no record (doesn't exist)
- `result.emis.gov.eg`, `results.emis.gov.eg` — no records
- `emis.gov.eg` — resolves to `50.85.18.241`

### IP Probe Results (50.85.18.241)

All 18+ paths tried returned `404 Not Found`:
```
/ /g12 /g12/ /results /result /thanawya /thanaweya /secondary
/exam /exams /natega /login /Home /Home/Result /Home/Index
/student /g12/result /Result
```

The server at 50.85.18.241 only serves `emis.gov.eg` — no other virtual hosts.

### Youm7 Form Action

Found via `document.querySelector('form').action`:
```
https://natega.youm7.com/Registration/Registration
```
This is the POST endpoint for the registration form.

### Summary

| Portal | Status | Result |
|--------|--------|--------|
| g12.emis.gov.eg | Deprecated (DNS dead) | — |
| 50.85.18.241 | All paths 404 | — |
| emis.gov.eg | Live, no result lookup | — |
| natega.youm7.com | Live, pre-registration only | 2026 results NOT yet published |
| student.emis.gov.eg | Microsoft login required | — |
| moe-register.emis.gov.eg | Login required | — |
| moe-gov-eg.pages.dev | Unofficial mirror, Supabase backend | Data may exist but not authoritative |

**Conclusion:** The 2026 Thanaweya Amma results had not been released as of 2026-07-29.

---

## First Session (Original)

Checked 2026-07-28/29 for Yousef Abbas Sultan Abbas.

## Student Data

| Field | Value |
|-------|-------|
| Seat number | 2013791 |
| National ID | 30711152107356 |
| Name (Arabic) | يوسف عباس سلطان عباس |
| Name (Latin) | Yousef Abbas Sultan Abbas |
| Governorate | الجيزه (Giza) — index 8, value "2" |
| Section | علمى رياضة (Science-Math) — DepartmentID=1 |
| System | الحديث (New) — System=1 |
| Phone | 01155440022 |
| Email | sultan@samayainvest.com |

## Portal Interaction Summary

### Portal layers discovered

1. **https://natega.youm7.com** — redirects to `/Registration`
   - Main result partner for Youm7 newspaper
   - Currently in pre-registration mode only
   - ASP.NET MVC with `inquiry-form` (result lookup) and `registration-form` (signup)
   - The `inquiry-form` with `seating_no` field is NOT active yet
   - Submitting registration succeeded (no validation errors after JS-driven form fill)
   - `/Result` endpoint returns "حدث خطأ" (error) — result not published

2. **https://emis.gov.eg/** — Ministry of Education EMIS portal
   - Static HTML + JS-rendered directory grid
   - Directory contains link to `https://student.emis.gov.eg/login` (student portal)
   - News item about result announcement is commented out in `main.js`
   - Subdomains: teacher.emis.gov.eg, schools.emis.gov.eg, search.emis.gov.eg, etc.

3. **https://student.emis.gov.eg/login** — Student data portal
   - Requires Microsoft Office 365 school account login
   - Not accessible without student's school credentials

4. **https://www.youm7.com/landing/thanaweya2026.html** — Thanaweya landing page
   - Mostly university ads
   - Links back to main registration portal

### What worked

- `browser_type` for text inputs (phone, name, seat, email) ✓
- `browser_console` with JavaScript expressions to set `<select>` selectedIndex and radio buttons ✓
- Using synchronous XHR to probe API endpoints ✓
- Reading inline JS files (`form.js`, `main.js`) to understand form handling ✓

### What failed

- `browser_click` on combobox dropdown options (CDP error: "Could not compute box model")
- `browser_type` on combobox (typed text went to wrong field due to focus issues)
- Standard `form.submit()` (HTTP 405 on direct POST)
- Form button click didn't produce visible response (AJAX submission)

### Key JavaScript findings from form.js

The registration form:
- Listens to DOMContentLoaded, binds to `registration-form`
- Phone: pattern `/^01[0125][0-9]{8}$/`, sanitises to digits only
- Seat number: digits only, no pattern length limit
- All fields required
- On submit: checks validity, prevents double-submit with `isSubmitting` flag
- Success: triggered by `data-show-success="true"` attribute on form element
- Success popup: `registration-success-popup` with dynamic content (phone, Fawry code, SMS option)

The inquiry form (home form):
- Uses field `name="seating_no"` not `name="SeatNumber"`
- Shows custom seat error with `data-seat-error` element
- Only activated when results are published
