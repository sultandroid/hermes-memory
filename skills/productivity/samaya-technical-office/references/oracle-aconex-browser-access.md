# Oracle Construction & Engineering (Aconex) Browser Access

Oracle acquired Aconex. The platform is now called **Oracle Construction and Engineering** but internally still referred to as "Aconex."

## Access

- **URL**: `https://constructionandengineering.oraclecloud.com/idcsLogin`
- **Login flow**: Username → Next → Password → Sign In
- **Known issue**: Session expires after inactivity; browser must re-login

## Project Navigation

1. After login, you land on **Projects** page showing all accessible projects
2. Find the target project (e.g., "Aseer Museum") and click to enter
3. The project dashboard loads with tabs:
   - **Home** — Task summary, project details, shortcuts
   - **Models** — BIM models
   - **Documents** — Document register (125 entries for Aseer Museum)
   - **Mail** — Project correspondence
   - **Field** — Field inspections
   - **Packages** — Submittal packages
   - **Workflows** — Approval/review workflows
   - **Directory** — Project team
   - **Insights** — Analytics
   - **Setup** — Project configuration

## Key Module: Document Register

- Found under **Documents → Document Register**
- Shows grid with columns: File, Document No, Revision, Version, Title, Type, Review Source, Status, Review Status, Discipline, Created By
- **Standard searches**: Approved, Issued for approval, Drawings modified today, Temporary files uploaded by me today
- **Search filters**: Text search, Floor filter, 9 additional pinned filters
- **Results**: Shows total count (e.g., "125 results")

## Known Browser Limitations

- **Oracle C&E is a heavy SPA** — loads slowly in headless browser
- **Content is inside cross-origin iframes** — JavaScript in the parent page cannot access iframe document content
- **`browser_snapshot` truncates large grids** — 125+ row grids are truncated at ~1800 lines
- **Session timeout** — session expires and redirects to login page after inactivity
- **Best approach for data extraction**: Use the Aconex Reports/Export feature to produce Excel/CSV, then process the exported file programmatically
- **Element refs change on every page re-render** — always get a fresh `browser_snapshot` before clicking

## Login Automation Pattern

```
browser_navigate(URL)
browser_snapshot()                    # Get refs
browser_type(ref=e2, text=username)  # Type username
browser_click(ref=e1)                 # Click Next
browser_snapshot()                    # Wait for password field
browser_type(ref=e6, text=password)  # Type password
browser_click(ref=e5)                 # Click Sign In
browser_snapshot()                    # Wait for project dashboard or cookie dialog
browser_click(ref=e2)                 # Accept cookies if dialog appears
```

## Password Visibility

- The password is stored in memory and should not be written to skill files or shared
- Login should be done per-session using the user-provided credentials in the current conversation
