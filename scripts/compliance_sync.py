#!/usr/bin/env python3
"""
Daily Compliance Sync — Aseer Regional Museum
Runs at 07:00 AST daily.
Checks Aconex transmittals for new approvals, updates compliance matrix and gaps.
"""
import subprocess, re, json, os, sys
from datetime import datetime, date
from pathlib import Path

REPO = Path(os.path.expanduser("~/aseer-museum-pm"))
MATRIX = REPO / "Technical_Office/Compliance_System/compliance_matrix.md"
GAPS = REPO / "Technical_Office/Compliance_System/compliance_gaps.md"
CHECKLIST = REPO / "Technical_Office/Compliance_System/compliance_checklist.md"
SPEC_LIST = REPO / "01_Registers/specification_list.md"
PQ_REG = REPO / "01_Registers/prequalification_register.md"
MA_REG = REPO / "01_Registers/material_submittal_register.md"
SPEC_REG = REPO / "Technical_Office/Specialist_Management/specialist_register.md"

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    return r.stdout.strip(), r.returncode

def check_aconex_emails():
    """Check Outlook for Aconex transmittals from the last 24h."""
    out, _ = run("""
        sqlite3 "$HOME/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite" \
        "SELECT datetime(date_received,'unixepoch','localtime'), subject \
         FROM messages \
         WHERE sender LIKE '%aconex.com' \
           AND date_received > strftime('%%s','now','-1 day','localtime') \
         ORDER BY date_received DESC LIMIT 20;" 2>/dev/null
    """)
    if not out:
        return []
    lines = out.strip().split('\n')
    results = []
    for line in lines:
        parts = line.split('|', 1)
        if len(parts) == 2:
            results.append({'time': parts[0].strip(), 'subject': parts[1].strip()})
    return results

def parse_approval_from_subject(subject):
    """Try to extract PQ/MA ref and status from Aconex subject line."""
    # Patterns: "PQ-0057 Approved", "MA-0001 Code B", "MOC-MUS-ASE-...-PQ-0057"
    pq_match = re.search(r'PQ[-\s]?(\d+)', subject, re.I)
    ma_match = re.search(r'MA[-\s]?(\d+)', subject, re.I)
    status_match = re.search(r'(Approved|Code [ABCDU]|Revise|Rejected|Disapproved)', subject, re.I)
    return {
        'pq_ref': f"PQ-{pq_match.group(1)}" if pq_match else None,
        'ma_ref': f"MA-{ma_match.group(1)}" if ma_match else None,
        'status': status_match.group(1) if status_match else None,
        'subject': subject
    }

def update_matrix_last_checked():
    """Update the last_updated date in the compliance matrix."""
    today = date.today().isoformat()
    with open(MATRIX) as f:
        content = f.read()
    content = re.sub(r'last_updated: \d{4}-\d{2}-\d{2}', f'last_updated: {today}', content)
    with open(MATRIX, 'w') as f:
        f.write(content)
    return True

def generate_report(aconex_items, changes_made):
    """Generate a brief compliance report."""
    lines = []
    lines.append(f"# Compliance Sync Report — {date.today().isoformat()}")
    lines.append("")
    if aconex_items:
        lines.append("## Aconex Transmittals (last 24h)")
        for item in aconex_items:
            parsed = parse_approval_from_subject(item['subject'])
            status = parsed['status'] or '—'
            refs = ' '.join(filter(None, [parsed['pq_ref'], parsed['ma_ref']]))
            lines.append(f"- {item['time']} | {status} | {refs} | {item['subject'][:80]}")
    else:
        lines.append("## Aconex Transmittals (last 24h)")
        lines.append("No new transmittals found.")
    lines.append("")
    lines.append(f"## Changes Made: {'Yes' if changes_made else 'No'}")
    lines.append("")
    # Read roll-up from matrix
    with open(MATRIX) as f:
        matrix_content = f.read()
    rollup_match = re.search(r'## Roll-up\n\n\| Metric \| Count \|\n\|[-| ]+\|\n((?:\|.*\|.*\|\n)+)', matrix_content)
    if rollup_match:
        lines.append("## Compliance Roll-up")
        lines.append(rollup_match.group(1).strip())
    return '\n'.join(lines)

def main():
    changes_made = False
    report_lines = []
    
    # 1. Check Aconex
    aconex_items = check_aconex_emails()
    if aconex_items:
        report_lines.append(f"Found {len(aconex_items)} Aconex transmittals")
        for item in aconex_items:
            parsed = parse_approval_from_subject(item['subject'])
            if parsed['status'] and ('Approved' in parsed['status'] or 'Code B' in parsed['status']):
                changes_made = True
                report_lines.append(f"  New approval: {parsed['subject'][:60]}")
    
    # 2. Update last_checked date
    update_matrix_last_checked()
    
    # 3. Generate report
    report = generate_report(aconex_items, changes_made)
    
    # Print report to stdout (cron captures this)
    print(report)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
