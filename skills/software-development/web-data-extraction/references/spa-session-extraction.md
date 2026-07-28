# SPA Extraction Worked Example — Sultan House (عمارة 210)

## Target
`https://land210.vercel.app/` — a password-protected React SPA for tracking construction finishing works. Built with React + i360code. All data behind login.

## Goal
Extract ALL data (dashboard, work items, payments, reports, legal files, stages, users) and produce structured MD documentation.

## Steps Taken

### 1. Login
```
browser_navigate(url) → see login form
browser_type(ref=e4, "email") → browser_type(ref=e5, "password") → browser_click(ref=e6)
```

### 2. Confirm dashboard loaded
```
browser_snapshot() — shows banner with project info, financial KPIs, charts, expense breakdown
```

### 3. Programmatic navigation via console
`browser_click` on nav buttons did NOT change the accessibility tree snapshot (React Router not registering in aXe tree). Workaround:

```javascript
// Run via browser_console(expression=...)
document.querySelectorAll('button').forEach(b => {
  if (b.textContent.trim() === 'بنود الأعمال') b.click();
});
// Then extract:
document.body.innerText  // 5000+ chars, all 40 work items
```

### 4. Extract each section
Repeat for each nav section: بنود الأعمال, المدفوعات, التقارير والرسوم, الملفات القانونية, المراحل, المستخدمين.

### 5. Save raw files
Write each section's `document.body.innerText` to a `.txt` file on the Micro volume.

### 6. Delegate analysis
```
delegate_task(
  goal="Study the data and create MD documentation",
  context="Files at /Volumes/MIcro/.pi-tmp/work/sultan-house/...",
  role="leaf"
)
```

## Key Lessons

- **Don't re-navigate:** `browser_navigate` to the same URL after login resets the SPA state. Stay on page and use JS `click()`.
- **Trust innerText over snapshot:** The aXe snapshot is reliable for initial structure but SPAs may not update it on route change. `document.body.innerText` always reflects what's rendered.
- **Extract → save → delegate:** Don't hold raw data in your context. Save to disk, then delegate processing to a sub-agent.
- **Chunk large datasets:** For 40+ records, use `substring(0, 15000)` in console to avoid truncation, or extract via multiple console calls targeting specific DOM subtrees.
