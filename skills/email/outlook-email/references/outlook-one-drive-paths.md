# Outlook SQLite Database Paths for OneDrive Users

This document summarizes the possible locations for Outlook's SQLite database when using OneDrive for storage.

## Standard Locations (macOS)

If the user has not configured a custom profile path, the database is typically stored in:
- `~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite`

## OneDrive-Specific Locations

If the user is using OneDrive for Outlook storage, the database may be synced to:
- `~/OneDrive/Work/Samaya/Tenders/` or similar OneDrive paths for project-specific Outlook profiles.

## Troubleshooting Steps

1. **Check OneDrive sync status**: Ensure Outlook is synced to OneDrive.
2. **Search OneDrive manually**: Run:
   ```bash
   find ~/OneDrive/Work -name "Outlook.sqlite" -type f
   ```
3. **Verify Outlook profile**: Use AppleScript to list available Outlook profiles:
   ```bash
   osascript -e 'tell application "Microsoft Outlook" to get name of every profile'
   ```
4. **Check profile path**: If the user has a custom profile, inspect the profile's path in `~/Library/Preferences/com.microsoft.office.plist`.

## Notes

- If the database is not found in standard locations, the user may need to manually configure the correct Outlook profile path.
- For project-specific databases, check the project folder structure in OneDrive (e.g., `~/OneDrive/Work/Samaya/Tenders/2021/`).