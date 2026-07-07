# Three Pipeline Pitfalls (discovered 2026-06-12)

## 1. download_mails.py crashes on dataless old archives

The script reads ALL existing archive files (.md) to de-duplicate by Outlook ID. When old archives (01.md–23.md) are OneDrive dataless placeholders, the script hits EDEADLK on each one and crashes.

**The crash does NOT mean the current week's data is lost.** The script writes each email to the archive file *immediately* after downloading — before it ever reads old archive files. If you see `[+] Completed Archiving Week 24` in stdout before the crash traceback, Week 24's archive (`24.md`) is intact.

**Verify:**
```bash
# Check file size change on current week archive
ls -la ~/Documents/04_Outlook_Connection/mails/24.md
# Compare against its known pre-run size
wc -l ~/Documents/04_Outlook_Connection/mails/24.md
```

**If Week N is intact:**
- Re-run the organizer manually: `python3 ~/Documents/04_Outlook_Connection/scripts/fast_organize.py`
- Continue with Steps 3–7 of the pipeline normally
- Report the crash as a note but process Week N's data

**If Week N is also truncated (rare):**
- Re-run `download_mails.py` after hydrating old archives: `brctl download ~/Documents/04_Outlook_Connection/mails/23.md` etc.
- Or exclude old weeks: temporarily rename old archives to `.bak`, re-run, then rename back

## 2. Arabic subjects mask critical technical emails

Arabic-subject emails from supervision consultants (EGEC, FEP, CG, PMC) can contain high-priority findings that English keyword filters miss entirely.

### Key Arabic patterns

| Arabic Keyword | Typical Context | Example Finding |
|---------------|----------------|-----------------|
| `انحناء مواسير` | Pipe bending/warping | Zamzam pipe thermal stress (2026-06-09) |
| `إجهادات حرارية` | Thermal stress in pipes/structures | Same as above |
| `إنذار` / `إنذار نهائي` | Warning / Final Notice | Kareem's 72hr ultimatum to Al Maghrabi (glass works) |
| `تصحيح` | Corrective action required | Usually paired with photos |
| `استقالة` | Resignation | HR event |
| `عهدة` | Inventory/custody | Workshop inventory request |
| `تصديق` | Attestation | Document legalization |
| `اجتماع` | Meeting | Check for MOM attachment |
| `طلب` | Request | Various operational requests |

### Integration into the scan step

```python
arabic_critical = {
    'انحناء': ('CRITICAL', 'structural issue'),
    'إجهادات حرارية': ('CRITICAL', 'thermal stress'),
    'إنذار': ('HIGH', 'warning/ultimatum'),
    'إنذار نهائي': ('HIGH', 'final notice'),
    'استقالة': ('MEDIUM', 'resignation'),
}

def scan_arabic_subjects(text):
    findings = []
    for line in text.split('\n'):
        if line.startswith('## '):  # email subject line
            for kw, (priority, desc) in arabic_critical.items():
                if kw in line:
                    findings.append((priority, desc, line.strip()[:150]))
    return findings
```

## 3. One email, multiple project targets

The auto-organizer (`fast_organize.py`) categorizes attachments based on the sender's Outlook folder/project assignment. This can misroute evidence when:

- A consultant email about Project A contains site photos showing a defect on Project B
- A general email includes attachments relevant to multiple projects
- A cross-project coordination email has docs for 2+ projects

### Detection and correction

**Step 1:** Read the email body (not just the subject) to identify which projects/contractors are mentioned.

**Step 2:** If the body references a different project than the auto-categorized target, COPY (don't move) the attachment to the correct project folder:

```bash
# Example: photos from EGEC email (Zamzam issue) auto-routed to Aseer/99_Images
# Correct: copy to Zamzam/Docs as well
cat "~/Documents/04_Outlook_Connection/mails/attachments/WhatsApp Image ...jpeg" > \
  "/path/to/Zamzam Museum/Docs/WhatsApp Image ...jpeg"
```

**Step 3:** Log the cross-project copy in the pipeline report.

### Heuristic: when to suspect cross-project attachments

| Signal | Suspect |
|--------|---------|
| Sender is a consultant/supervisor (`@egec.com.sa`, `@cg.com.sa`, `@ace-mb.com`) | Email may cover multiple projects under their supervision |
| Subject contains multiple project names | Attachments may belong to each named project |
| Attachment is a site photo (`WhatsApp`, `IMG_`, screenshot) | Context determines project, not folder |
| Subject is Arabic, attachments are photos | Likely a site issue — read body to identify correct project |
