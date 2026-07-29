# Egyptian Government Education Portal Patterns

Patterns learned from accessing Egyptian Ministry of Education (EMIS) portals, specifically for Thanaweya Amma (General Secondary Certificate) result checking.

## Domain Structure

| Domain | Status | Purpose |
|--------|--------|---------|
| `emis.gov.eg` | ✅ Resolves (50.85.18.241) | Main EMIS portal, static HTML |
| `g12.emis.gov.eg` | ❌ No DNS record | Grade 12 subdomain — configured in Azure App Gateway but no backend deployed (404 all paths) |
| `www.emis.gov.eg` | ❌ No DNS record | www subdomain — does not exist |
| `moe-register.emis.gov.eg` | ✅ Resolves | General Certificates Platform (registration, seat number lookup) |
| `natega.youm7.com/Registration` | ✅ | Result portal (authorised partner — Youm7 newspaper) |

## Azure Application Gateway Pattern

Some subdomains (like `g12.emis.gov.eg`) have no public DNS record but ARE configured in the Azure Application Gateway at 50.85.18.241. The gateway accepts connections to the hostname if forced via `--resolve` but returns **404 on every path** when no backend is deployed.

**Try HTTPS too:** The wildcard TLS certificate `*.emis.gov.eg` covers all subdomains including `g12`. Even if HTTP fails, the HTTPS endpoint may respond differently. Use `--resolve` with port 443:

```bash
curl -sk --max-time 10 "https://g12.emis.gov.eg/" \
  --resolve "g12.emis.gov.eg:443:50.85.18.241"
```

A successful TLS handshake + 404 confirms the hostname is configured in the gateway but inactive. Track hostname → IP mapping even when DNS returns NXDOMAIN, as the gateway config may be live but the backend service may be deployed later.

**When a user gives you a URL that won't resolve — try harder before giving up:**

If the user provides a specific URL repeatedly and it doesn't resolve with standard DNS:

1. `nslookup <domain>` — baseline check
2. `curl --resolve "<host>:<port>:<ip>"` against the known server IP (from the main domain, e.g., 50.85.18.241 for emis.gov.eg)
3. Try both HTTP and HTTPS — the wildcard cert may cover the subdomain
4. `curl -v` to inspect the HTTP response — Azure Gateway returns `Server: Microsoft-Azure-Application-Gateway/v2` with 404 when the backend isn't deployed vs. no response at all when the hostname isn't configured
5. **Delegate to sub-agent** via `delegate_task` — a fresh session has independent DNS resolution and network access. Use when the user says "try from sources" or "try from ai model server"

**Diagnosis:**
```bash
# Force DNS resolution to known IP
curl -sk --max-time 10 "http://g12.emis.gov.eg/" \
  --resolve "g12.emis.gov.eg:80:50.85.18.241"

# Server header confirms Azure Gateway
# Server: Microsoft-Azure-Application-Gateway/v2
```

This means the subdomain "exists" in gateway config but has no active service. Track the domain via DNS `nslookup` and gateway response headers to distinguish "not configured" from "configured but not active."

## Delegate for Alternative Network Paths

When DNS resolution fails from the local environment:
1. First verify with `nslookup g12.emis.gov.eg`
2. If NXDOMAIN, try forced resolution with `curl --resolve`
3. If that also fails, **delegate the task to a sub-agent** via `delegate_task` — a fresh session on the same machine may have different DNS resolution or network access. The sub-agent gets its own terminal session and can independently resolve and curl the target.

## Service Identification from Arabic Transliteration

Users may refer to services by transliterated Arabic names:
- "sanwaya amaa / sanwaya ama" = **سنوية عامة** / **ثانوية عامة** = General Secondary Certificate (Thanaweya Amma)
- "resulte" = **نتيجة** = result

When the user provides a URL mid-conversation, use it **directly** — do not first try to reverse-engineer what service they mean through web searches.

## User-Provided URLs Are Authoritative

When a user gives you a specific URL and keeps asking you to try it (even after multiple failures), **trust their input**. They likely know the correct URL from an external source (Ministry announcement, news article, SMS, etc.). Do not dismiss it after a few attempts — the URL may be correct but the service may not be deployed yet.

**Pattern:** User says "try thes http://g12.emis.gov.eg/" repeatedly. The URL:
1. Returns NXDOMAIN on all public DNS servers
2. Returns 404 when forced-resolved to the gateway IP
3. Is linked from the official Ministry website (moe.gov.eg) as the official result portal

The URL was correct all along — the service just wasn't deployed yet. The user knew what they were talking about.

**Lesson:** When a user insists on a specific URL, document it, keep trying it, and set up monitoring (cron job) rather than concluding it's dead. The user's persistence is a signal that the URL is authoritative.

## Form Interaction Techniques (Youm7 Portal)

The Youm7 registration form uses a **custom combobox** for governorate and **hidden radio buttons** for section/system that `browser_click` fails on.

### Governorate Combobox Workaround

The `<select id="governorate">` has options with numeric values (الجيزه = "2", القاهره = "1", etc.):

```javascript
// Set via JS console — browser_type on the combobox contaminates the email field
const sel = document.getElementById('governorate');
sel.selectedIndex = 8;  // الجيزه is index 8
sel.dispatchEvent(new Event('change', {bubbles: true}));
```

Full governorate index/value table:

| Index | Value | Name |
|-------|-------|------|
| 0 | "" | اختر المحافظة |
| 1 | 5 | أسوان |
| 2 | 6 | أسيوط |
| 3 | 4 | الإسماعيلية |
| 4 | 3 | الأقصر |
| 5 | 7 | الاسكندريه |
| 6 | 8 | البحر الأحمر |
| 7 | 9 | البحيرة |
| 8 | 2 | الجيزه |
| 9 | 13 | الدقهلية |
| 10 | 14 | السويس |
| 11 | 15 | الشرقية |
| 12 | 16 | الغربية |
| 13 | 10 | الفيوم |
| 14 | 1 | القاهره |
| 15 | 11 | القليوبية |
| 16 | 17 | المنوفيه |
| 17 | 18 | المنيا |
| 18 | 19 | الوادى الجديد |
| 19 | 20 | بني سويف |
| 20 | 21 | بورسعيد |
| 21 | 22 | جنوب سيناء |
| 22 | 23 | دمياط |
| 23 | 24 | سوهاج |
| 24 | 25 | شمال سيناء |
| 25 | 26 | قنا |
| 26 | 27 | كفر الشيخ |
| 27 | 28 | مطروح |

### Section Radio Buttons

```javascript
// Radio button names and values
// DepartmentID: 2=علمى علوم, 1=علمى رياضة, 3=أدبى
// System: 2=قديم, 1=حديث
// IsSMS: 0=عرض على الموقع, 1=SMS

// Set علمى رياضة + نظام حديث
const radios = document.querySelectorAll('input[type="radio"]');
radios[1].checked = true;   // DepartmentID=1 (علمى رياضة)
radios[4].checked = true;   // System=1 (حديث)
radios[1].dispatchEvent(new Event('change', {bubbles: true}));
radios[4].dispatchEvent(new Event('change', {bubbles: true}));
```

### Registration vs Result-Check

**This portal is a REGISTRATION service** — it saves the user's data to notify them when results are officially released by the Ministry of Education. It does NOT display the result immediately on submission. The page text confirms: "فور إعلانها رسميًا من وزارة التربية والتعليم" (immediately upon official announcement).

### Cron Job for Pending Results

When a portal is in pre-registration mode and the result hasn't been published yet, set up a **recurring cron job** to check periodically:

```bash
cronjob action=create schedule="every 5m" deliver="local" \
  prompt="Check if the result has been published on natega.youm7.com. \
If not, say 'Not yet' — if found, report all grades and total." \
  enabled_toolsets=["web","terminal","file"] \
  name="Result Check - Student Name"
```

Key design decisions:
- **schedule:** `every 5m` or `every 10m` — frequent enough to catch it early
- **deliver:** `local` — results accumulate in the cron log without interrupting the session. Viewable via `cronjob action='list'`
- **prompt:** Instruct the agent to say only `"Not yet"` when unpublished (no spam), but report **full grades, total score, and percentage** when found
- The user may ask you to "try now" between cron ticks — navigate and check manually when requested

The cron job should check multiple sources: natega.youm7.com first (authorised partner), then emis.gov.eg for any new result section.

### Form Submission and Validation

- The form validates phone format client-side (must start with 010/011/012/015 followed by 8 digits = 11 total)
- All fields are required except the SMS opt-in
- The form submits via AJAX (no page redirect on success)
- After successful registration, the form resets (fresh empty form on full page reload)
- No visible success/error message appears on the page — the form simply resets or stays in place
- The "تسجيل البيانات" (Register Data) button does a full form submission; `form.submit()` does a server-side POST which returns the same page fresh

The result portal (natega.youm7.com) requires:

| Field | Arabic Label | Format | Example |
|-------|-------------|--------|---------|
| Phone | رقم الهاتف | Egyptian mobile (010/011/012/015 + 8 digits) | 01012345678 |
| Full name | الاسم بالكامل | Arabic full name | محمد أحمد علي |
| Seat number | رقم الجلوس | 7 digits | 2013791 |
| Governorate | المحافظة | One of 27 Egyptian governorates | القاهره |
| Email | البريد الإلكتروني | Valid email | user@example.com |
| Section | الشعبة | علمي علوم / علمي رياضة / أدبي | — |
| System | النظام | قديم (old) / حديث (new) | — |

## National ID vs Phone Number

Egyptian **national ID** (الرقم القومي) is 14 digits.
Egyptian **mobile numbers** are 11 digits (01X + 8 digits).

When the user provides two numbers for a result check:
- If 7 digits → likely the **seat number** (رقم الجلوس)
- If 14 digits → likely the **national ID** (الرقم القومي)

## form.js — Client-Side Validation and Submission

The form submission is handled by `/assets/scripts/form.js`. Key behaviors:

- The form has **two IDs**: `registration-form` (the multi-field registration) and `inquiry-form` (a simpler seat-number-only lookup that appears when results are published).
- Fields are validated client-side before submission:
  - Phone: `^01[0125][0-9]{8}$` (starts with 010/011/012/015, 11 digits total)
  - Seat number: digits only
  - Email: browser-native `typeMismatch` validation
  - Governorate: must have a non-empty value
  - DepartmentID: at least one radio checked
- On submit, the form submits via **standard HTML form POST** (not AJAX/fetch).
- The **submit button** (`class="inquiry-form__submit"`) is disabled during submission (`isSubmitting` flag).
- On success, the server responds with `data-show-success="true"` on the `registration-form` element, plus `data-success-phone`, `data-success-fawry`, and `data-is-sms` attributes. The JS then opens a **hidden popup** (`#registration-success-popup`).
- The popup is a modal (`class="success-popup is-open"`) with:
  - For SMS mode: shows phone number and Fawry payment code
  - For website mode (`isSms=false`): shows a simple success message
- The popup closes on Escape key or clicking `[data-close-popup]` elements.
- The page sets `document.body.style.overflow = "hidden"` when the popup is open.

### Form HTML `name` attributes

| Name attribute | Type | Notes |
|---|---|---|
| `Phone` | tel | 11-digit Egyptian mobile |
| `Name` | text | Full name in Arabic |
| `SeatNumber` | text | Digits only |
| `GovernorateID` | select | Numeric values per governorate |
| `Email` | email | |
| `DepartmentID` | radio | 1=علمى رياضة, 2=علمى علوم, 3=أدبى |
| `System` | radio | 1=حديث, 2=قديم |
| `IsSMS` | radio | 0=عرض على الموقع, 1=SMS |

### Button-click vs form.submit() — Different Behaviors

| Method | Behavior |
|--------|----------|
| Click `تسجيل البيانات` button | Triggers JS validation → if valid, submits via standard POST → server responds with success popup data or validation errors → **form resets on success** |
| `form.submit()` via console | **HTTP 405** — raw POST to `/Registration` is rejected; the JS validation handler is bypassed and the server returns the empty form page |

Always click the submit button (`browser_click` on the submit ref) rather than calling `form.submit()` from console. The latter bypasses the JS handler and always fails.

## Common Pitfalls

- **Subdomain resolution:** Not all EMIS subdomains have DNS records. `g12.emis.gov.eg` does not resolve. Use `nslookup` to verify before assuming a URL works.
- **Azure Application Gateway — hostname accepted without DNS record:** Some EMIS subdomains (like `g12.emis.gov.eg`) have no public DNS record but ARE configured in the Azure Application Gateway. The gateway accepts connections to the hostname if forced via IP but returns **404 on every path** when no backend is deployed. This means the subdomain "exists" in configuration but has no active service. Diagnose with: `curl --resolve "g12.emis.gov.eg:80:<IP>" http://g12.emis.gov.eg/`
- **Next.js / React SPAs:** The main EMIS site and `moe-register.emis.gov.eg` are Next.js apps — their actual content requires JavaScript rendering and cannot be scraped via `curl` alone. Use browser tools for interaction.
- **Youm7 result portal:** The registration form requires many fields beyond just seat number + national ID. The user must supply name, governorate, section, phone, and email.
- **Button click vs form.submit():** Submit button click triggers AJAX-compatible POST that the JS handler processes. Calling `form.submit()` from console bypasses the handler and gets HTTP 405. Always click the submit button element instead.
- **No visible feedback on success:** The form resets and a hidden popup appears. `browser_snapshot` may not show the popup. Check for `data-show-success="true"` on the form element or the popup's `is-open` class via `browser_console`.
- **SEF (Statens Elev Fund) / Danish portal confusion:** Do not confuse emis.gov.eg (Egypt) with other EMIS systems in other countries.
