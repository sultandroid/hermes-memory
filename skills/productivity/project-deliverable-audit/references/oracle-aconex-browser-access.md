# Oracle Aconex (Construction & Engineering) — Browser Access Pattern

Access the project Common Data Environment (CDE) via Oracle Cloud browser interface.

## Login URL

```
https://constructionandengineering.oraclecloud.com/idcsLogin
```

Redirects to Oracle Identity Cloud Service (IDCS) for authentication.

## Login Flow

1. Navigate to the URL → "Sign In" page loads with Username field
2. Type username → click "Next"
3. Password field appears → type password → click "Sign In"
4. Cookie consent dialog appears → click "Accept"
5. Dashboard loads showing Projects list

## Post-Login Navigation

After login, the Oracle Construction and Engineering lobby shows all accessible projects in a table:

| Column | Example |
|--------|---------|
| Name | Aseer Museum |
| Status | Active |
| Controlling Organization | Oracle |
| Application | Aconex |
| Region | Saudi Arabia (KSA1) |
| Username | sultan-1 |

Click the project row to enter. The project workspace has these tabs:

| Tab | Purpose |
|-----|---------|
| Home | Dashboard, recent activity |
| Models | BIM models |
| **Documents** | Document register — submittals, drawings, statuses |
| Mail | Project correspondence, transmittals |
| Field | Field inspections, observations |
| **Packages** | Submittal packages with workflow status |
| Workflows | Approval/review workflows |
| Directory | Project team directory |
| Insights | Reports, analytics |
| Setup | Project configuration |

## Key Modules for Submission Plan Work

### Documents Tab
- Document register showing all registered documents
- Search/filter by document number (e.g., MOC-MUS-ASE-1A0-MA-0006)
- Status column shows current approval status
- Can export to Excel for offline cross-referencing

### Packages Tab  
- Grouped submittals with review workflows
- Shows current review stage, assigned reviewers, days in review
- Status: In Review, Approved, Approved w/Comments, Revise & Resubmit, Rejected

## Known Limitations

- The page is a heavy JavaScript SPA (Single Page Application) — the headless browser snapshot may show "(empty page)" while the app loads
- Wait 2-3 seconds after navigation, then check `document.title` to verify the page loaded
- The cookie consent dialog appears on first login per session — always accept it
- The iframe-based tab content may not be accessible via snapshot — use browser_console to check page state
- Login session persists for the browser session; if the tab is idle too long, re-authentication may be needed

## Cross-Reference Workflow

When you need to update a submission plan from Aconex data:

1. Login and navigate to Documents or Packages tab
2. Export or manually extract the relevant document list
3. Cross-reference document numbers (e.g., MOC-MUS-ASE-MA-xxxx) against the submission plan
4. Update plan statuses based on Aconex approval status (A/B/C/D codes)
5. Log the comparison in the submission plan Remarks column
