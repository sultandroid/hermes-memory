---
name: egyptian-gov-exam-results
description: Check Egyptian Ministry of Education exam results (Thanaweya Amma, Azhar, etc.) through official portals like natega.youm7.com and emis.gov.eg.
---

# Egyptian Government Exam Results Portal Interaction

Check Egyptian Thanaweya Amma (الثانوية العامة) and other MoE exam results.

## Official Portals

| Portal | URL | Purpose | Status |
|--------|-----|---------|--------|
| Youm7 Results | https://natega.youm7.com | Authorised result partner (pre-registration + lookup) | ✅ Active |
| EMIS main | https://emis.gov.eg | Ministry portal, directory of all services | ✅ Active |
| MoE main | https://www.moe.gov.eg | Ministry of Education official website | ✅ Active |
| G12 Official Result | https://g12.emis.gov.eg | **Official** Grade 12 result portal — linked from moe.gov.eg | ⏳ Backend not deployed (Azure Gateway 404) |
| Student portal | https://student.emis.gov.eg/login | Requires school Office 365 account | ✅ Active |
| Exam registration | https://moe-register.emis.gov.eg | Seat number lookup, form registration (login required) | ✅ Active |

### G12 Official Result Portal (g12.emis.gov.eg)

**This IS the official result portal** — it's linked directly from the Ministry of Education website (moe.gov.eg). The subdomain is configured in the Azure Application Gateway (wildcard cert `*.emis.gov.eg` covers it) but the backend service is **not deployed yet** (returns 404 on all paths).

**Do NOT mark this as "dead" or "deprecated"** — it's the correct URL, just inactive until the Ministry activates it for the current exam season.

Diagnosis:
- DNS: NXDOMAIN on all public DNS (Google, Cloudflare, OpenDNS, Quad9)
- Gateway: Accepts connections via `--resolve` to 50.85.18.241 (both ports 80 and 443)
- Response: `Server: Microsoft-Azure-Application-Gateway/v2` with 404 on every path
- TLS: Valid wildcard cert for `*.emis.gov.eg` (GoDaddy, expires Nov 2026)

When the Ministry publishes results, this URL will become active. Monitor via cron job.

## Third-Party Mirrors (Unofficial)

| Portal | URL | Backend | Notes |
|--------|-----|---------|-------|
| MoE Cloudflare Mirror | `https://moe-gov-eg.pages.dev/` | Supabase (`bbqivmyforcuezpmgjxo.supabase.co`) | Unofficial third-party mirror. Uses Cloudflare Pages free hosting, NOT a `.gov.eg` domain. Data may be accurate but not authoritative. |

### Supabase Direct Query (for moe-gov-eg.pages.dev)

The site exposes its Supabase anon key in the page source. Query directly:

```javascript
// Get the key from page source
const key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJicWl2bXlmb3JjdWV6cG1nanhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI0MTg5OTUsImV4cCI6MjA5Nzk5NDk5NX0.UEtUoChk9s5ot32Zhn0J5-uQ55HVSZ8s_kvRfujdHLs';

// REST API query
fetch('https://bbqivmyforcuezpmgjxo.supabase.co/rest/v1/student_results?seat_number=eq.2013791', {
  headers: { 'apikey': key, 'Authorization': 'Bearer ' + key }
}).then(r => r.json()).then(console.log);
```

The `student_results` table has columns: `seat_number`, `student_name`, `branch`, `status`, `subjects_added` (JSON), `subjects_not_added` (JSON).

Before wasting time navigating, verify subdomains exist with:
```bash
dig g12.emis.gov.eg A +short   # empty = dead
dig natega.emis.gov.eg A +short
```
Then probe paths directly against the known IP:
```bash
for path in / /g12 /result; do
  echo -n "$path -> "; curl -s -L -o /dev/null -w "%{http_code}" \
    "http://50.85.18.241$path" --max-time 5 2>/dev/null; echo ""
done
```

## Understanding the Portal

Youm7's result page is an **ASP.NET MVC** app with two forms:

1. **Registration form** (`id="registration-form"`) — active BEFORE results are published. Collects phone, name, seat number, governorate, email, section, system. Submits via POST and shows a success popup on response.

2. **Inquiry form** (`id="inquiry-form"`, field `name="seating_no"`) — activated AFTER results are published. Direct seat-number lookup.

The site text "فور اعتمادها رسميًا" / "فور إعلانها" means results are NOT yet released.

## Registration Workflow

### Setting form values (when browser_click fails on custom controls)

The form uses a `<select>` for governorate and radio buttons for section/system. Use browser console JavaScript to set values directly:

```javascript
// Governorate dropdown (id="governorate")
const g = document.getElementById('governorate');
g.selectedIndex = N; // find index first
g.dispatchEvent(new Event('change', {bubbles: true}));

// Find indices by iterating:
for(let i=0;i<g.options.length;i++) { console.log(i, g.options[i].text); }

// Radio buttons
document.querySelectorAll('input[type="radio"]') // check names:
// DepartmentID: 2=علمى علوم, 1=علمى رياضة, 3=أدبى
// System: 2=قديم, 1=حديث
// IsSMS: 0=موقع, 1=SMS

// Set radio:
document.querySelector('[name="DepartmentID"][value="1"]').checked = true;
document.querySelector('[name="System"][value="1"]').checked = true;
// Fire change events:
[/* radios */].forEach(r => r.dispatchEvent(new Event('change', {bubbles: true})));
```

### Form fields (ASP.NET MVC naming)

| HTML name | Field |
|-----------|-------|
| `Phone` | Phone number (Egyptian format: 01[0125] + 8 digits) |
| `Name` | Full name in Arabic |
| `SeatNumber` | 7-digit seat/جلوس number |
| `GovernorateID` | Select dropdown (value is number, not text) |
| `Email` | Email address |
| `DepartmentID` | Radio: 1=علمى رياضة, 2=علمى علوم, 3=أدبى |
| `System` | Radio: 1=حديث, 2=قديم |
| `IsSMS` | Radio: 0=display on site, 1=SMS notification |

### Form submission

Use the visible submit button if possible. If not, submit via form JS:
```javascript
document.querySelector('form').submit(); // or click the button
```

The server responds with either:
- Same page with validation errors (`class="field-validation-error"`)
- Same page with success popup (`data-show-success="true"` on form, triggers `registration-success-popup`)

## Verification

Check if results are published by visiting:
- `https://natega.youm7.com/` — redirects to Registration if pending
- `https://natega.youm7.com/Result` — shows "حدث خطأ" error if no result
- Look for `id="inquiry-form"` in the page (this is the direct lookup form, only active when results are out)

## Common Pitfalls

- **Combobox not accepting text input**: It's a custom `<select>` wrapper. Use JS to set `selectedIndex` + fire `change` event instead of trying to type/click.
- **Typed text going to wrong field**: Browser focus can shift between filled fields. Always reload fresh before filling.
- **Phone validation**: Pattern `/^01[0125][0-9]{8}$/` enforced by JS. Input is sanitised to digits only, max 11 chars.
- **National ID vs phone**: Egyptian national ID is 14 digits, phone is 11 digits. The form asks for phone, not national ID.
- **Form submits but page doesn't change**: The registration uses AJAX/standard POST with a success popup that auto-hides. Check `registration-success-popup` in DOM.
- **The result is NOT available yet**: The portal only accepts pre-registration until the Ministry officially releases results.

## Detect Result Publication

Check the Youm7 home page (`https://www.youm7.com/`) for a `thanaweya2026.html` landing page or look for news about result publication on EMIS (`https://emis.gov.eg/`).
