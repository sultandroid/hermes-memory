#!/usr/bin/env python3
"""
Submission Plan Validation System (SPVS)
Validates a submission plan against SOW/scope, programme schedule, submittal register,
and cross-discipline dependencies. Runs 10 checks and produces a markdown report.

Usage:
    python3 validate_submission_plan.py \
        --plan "02_Schedule/landscaping_submission_plan.md" \
        --programme "02_Schedule/master_programme.md" \
        --register "01_Registers/submittal_register.md" \
        --scope "03_Scope/scope_summary.md" \
        --master-plan "02_Schedule/submission_plan_risk_assessment.md" \
        --output "02_Schedule/validation_report.md"
"""

import argparse
import re
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ─── Constants ───────────────────────────────────────────────────────────────

KSA_WEEKEND = {4, 5}  # Fri=4, Sat=5 (Mon=0)

GATE_DEADLINES = {
    "50%": datetime(2026, 7, 31),   # D35 ~end Jul
    "90%": datetime(2026, 8, 28),   # D65 ~late Aug
    "100%": datetime(2026, 9, 15),  # D82 ~mid Sep
    "IFC": datetime(2026, 9, 15),   # D82 ~mid Sep
    "AFC": datetime(2026, 9, 22),   # D88 ~late Sep
}

REVIEW_BUFFER = {
    "simple": 9,    # 2 internal + 7 CG
    "medium": 17,   # 3 internal + 14 CG
    "complex": 19,  # 5 internal + 14 CG
}

# ─── Data Classes ───────────────────────────────────────────────────────────

class PlanItem:
    def __init__(self):
        self.ref = ""
        self.description = ""
        self.gate = ""
        self.discipline = ""
        self.responsibility = ""
        self.date = None  # datetime
        self.date_str = ""
        self.depends_on = ""
        self.activity_id = ""
        self.status = ""
        self.source_file = ""
        self.line = 0

class Issue:
    def __init__(self, severity, check, description, recommendation, item_ref=""):
        self.severity = severity  # CRITICAL / HIGH / MEDIUM / LOW
        self.check = check        # 1-10
        self.description = description
        self.recommendation = recommendation
        self.item_ref = item_ref

# ─── Helpers ───────────────────────────────────────────────────────────────

def is_working_day(d):
    """Returns True if d is a KSA working day (Sun-Thu)."""
    return d.weekday() not in KSA_WEEKEND

def add_working_days(start, n):
    """Add n working days to start date."""
    current = start
    added = 0
    while added < n:
        current += timedelta(days=1)
        if is_working_day(current):
            added += 1
    return current

def parse_date(s):
    """Parse various date formats to datetime. Returns None if unparseable."""
    if not s or s.strip() in ("TBC", "TBD", "—", "-", ""):
        return None
    s = s.strip()
    # Try dd/mm/yyyy or dd/mm/yy
    for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d", "%d-%b-%Y", "%d-%b-%y"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    # Try "29/06/2026" with various separators
    m = re.match(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', s)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if y < 100:
            y += 2000
        try:
            return datetime(y, mo, d)
        except ValueError:
            return None
    return None

def normalize(s):
    """Normalize a string for comparison: lowercase, strip, collapse whitespace."""
    if not s:
        return ""
    return re.sub(r'\s+', ' ', s.lower().strip())

# ─── Extractors ─────────────────────────────────────────────────────────────

def extract_plan_items_markdown(filepath):
    """Extract items from a discipline submission plan markdown file."""
    items = []
    with open(filepath) as f:
        content = f.read()
    
    # Parse deliverable register tables
    # Pattern: | Ref | Deliverable | Due Stage | Acceptance Criteria | Status |
    lines = content.split('\n')
    in_table = False
    headers = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            
            # Detect header row
            if any(h in cells[0].lower() for h in ['ref', '#', 'item']) and \
               any(h in cells[1].lower() for h in ['deliverable', 'description', 'subject']):
                headers = cells
                in_table = True
                continue
            
            if in_table and len(cells) >= 3:
                item = PlanItem()
                item.source_file = str(filepath)
                item.line = i + 1
                
                # Map columns by header position
                for j, cell in enumerate(cells):
                    if j < len(headers):
                        h = headers[j].lower()
                        if 'ref' in h or '#' in h:
                            item.ref = cell
                        elif 'deliverable' in h or 'description' in h or 'subject' in h:
                            item.description = cell
                        elif 'stage' in h or 'gate' in h or 'due' in h:
                            item.gate = cell
                            item.date = parse_date(cell)
                            item.date_str = cell
                        elif 'status' in h:
                            item.status = cell
                        elif 'responsib' in h or 'owner' in h:
                            item.responsibility = cell
                        elif 'depend' in h or 'predecessor' in h:
                            item.depends_on = cell
                        elif 'activity' in h or 'id' in h:
                            item.activity_id = cell
                
                # Also check for date in "Target" column of schedule tables
                if not item.date:
                    # Try to find a date anywhere in the row
                    for cell in cells:
                        d = parse_date(cell)
                        if d:
                            item.date = d
                            item.date_str = cell
                            break
                
                items.append(item)
        else:
            if in_table and stripped and not stripped.startswith('|'):
                in_table = False
    
    return items


def extract_plan_items_master(filepath):
    """Extract items from the master submission plan (risk assessment doc)."""
    items = []
    with open(filepath) as f:
        content = f.read()
    
    # Parse the master schedule table
    # Pattern: | # | Package / Item | 50% / 1st Sub | 90% | 100% | IFC/AFC | Depends On | Group | Review Buffer | Notes |
    lines = content.split('\n')
    in_table = False
    headers = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            
            if any('package' in c.lower() for c in cells) and \
               any('50%' in c for c in cells):
                headers = cells
                in_table = True
                continue
            
            if in_table and len(cells) >= 5:
                item = PlanItem()
                item.source_file = str(filepath)
                item.line = i + 1
                
                for j, cell in enumerate(cells):
                    if j < len(headers):
                        h = headers[j].lower()
                        if '#' in h or 'item' in h:
                            item.ref = cell
                        elif 'package' in h or 'item' in h:
                            item.description = cell
                        elif '50%' in h or '1st' in h:
                            item.date = parse_date(cell)
                            item.date_str = cell
                            item.gate = "50%"
                        elif '90%' in h:
                            if not item.date:
                                item.date = parse_date(cell)
                                item.date_str = cell
                                item.gate = "90%"
                        elif 'depends' in h or 'predecessor' in h:
                            item.depends_on = cell
                        elif 'notes' in h:
                            item.status = cell
                
                items.append(item)
        else:
            if in_table and stripped and not stripped.startswith('|'):
                in_table = False
    
    return items


def extract_programme_milestones(filepath):
    """Extract milestones from master programme markdown."""
    milestones = {}
    with open(filepath) as f:
        content = f.read()
    
    # Parse key milestones table
    lines = content.split('\n')
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if any('milestone' in c.lower() for c in cells):
                in_table = True
                continue
            if in_table and len(cells) >= 3:
                name = cells[0]
                date_str = cells[1]
                d = parse_date(date_str)
                if d:
                    milestones[name] = d
        else:
            if in_table and stripped:
                in_table = False
    
    return milestones


def extract_register_items(filepath):
    """Extract items from the submittal register markdown."""
    items = []
    with open(filepath) as f:
        content = f.read()
    
    lines = content.split('\n')
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if any('ref' in c.lower() for c in cells) and \
               any('subject' in c.lower() for c in cells):
                in_table = True
                continue
            if in_table and len(cells) >= 3:
                items.append({
                    'ref': cells[0] if len(cells) > 0 else '',
                    'description': cells[1] if len(cells) > 1 else '',
                    'discipline': cells[2] if len(cells) > 2 else '',
                    'date': cells[3] if len(cells) > 3 else '',
                    'status': cells[4] if len(cells) > 4 else '',
                })
        else:
            if in_table and stripped:
                in_table = False
    
    return items


def extract_scope_items(filepath):
    """Extract scope items from scope summary markdown."""
    items = []
    with open(filepath) as f:
        content = f.read()
    
    # Parse "In Scope" section
    in_scope = False
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('## In Scope'):
            in_scope = True
            continue
        if stripped.startswith('## ') and in_scope:
            break
        if in_scope and stripped.startswith('- '):
            items.append(stripped[2:])
    
    return items


def extract_dependencies(plan_items):
    """Extract dependency pairs from plan items."""
    deps = []
    for item in plan_items:
        if item.depends_on and item.depends_on not in ('—', '-', ''):
            deps.append((item, item.depends_on))
    return deps


# ─── Validators ─────────────────────────────────────────────────────────────

def check_sow_coverage(plan_items, scope_items, issues):
    """Check 1: SOW Coverage — deliverables in SOW missing from plan."""
    if not scope_items:
        return
    
    plan_descriptions = [normalize(p.description) for p in plan_items]
    
    for scope_item in scope_items:
        norm = normalize(scope_item)
        # Skip generic items
        if not norm or len(norm) < 10:
            continue
        # Check if any plan item covers this scope item
        covered = any(
            any(word in pd for word in norm.split() if len(word) > 3)
            for pd in plan_descriptions
        )
        if not covered:
            issues.append(Issue(
                "HIGH", 1,
                f"SOW item not found in submission plan: '{scope_item[:80]}'",
                "Add this deliverable to the submission plan with a ref, date, and responsible party."
            ))


def check_scope_boundary(plan_items, scope_items, issues):
    """Check 2: Scope Boundary — items in plan not traceable to any SOW."""
    if not scope_items:
        return
    
    scope_norms = [normalize(s) for s in scope_items]
    
    for item in plan_items:
        if not item.description or len(item.description) < 5:
            continue
        norm = normalize(item.description)
        # Check if this item is covered by any scope item
        covered = any(
            any(word in sn for word in norm.split() if len(word) > 4)
            for sn in scope_norms
        )
        if not covered:
            issues.append(Issue(
                "MEDIUM", 2,
                f"Plan item '{item.description[:60]}' has no clear SOW/scope reference",
                f"Add a SOW clause reference to the description or remove if out of scope.",
                item.ref
            ))


def check_schedule_alignment(plan_items, programme_milestones, issues):
    """Check 3: Schedule Alignment — dates match programme milestones."""
    if not programme_milestones:
        return
    
    for item in plan_items:
        if not item.date:
            continue
        # Check against relevant milestones
        for milestone_name, milestone_date in programme_milestones.items():
            if not milestone_date:
                continue
            # Check if this item's description relates to this milestone
            if any(word in normalize(item.description) for word in normalize(milestone_name).split()):
                diff = abs((item.date - milestone_date).days)
                if diff > 5:
                    issues.append(Issue(
                        "HIGH" if diff > 10 else "MEDIUM", 3,
                        f"'{item.description[:50]}' planned {item.date.strftime('%d/%m/%y')} "
                        f"but programme milestone '{milestone_name}' is {milestone_date.strftime('%d/%m/%y')} "
                        f"({diff} day gap)",
                        f"Align date to programme milestone or document the variance.",
                        item.ref
                    ))


def check_dependency_chain(plan_items, issues):
    """Check 4: Dependency Chain — predecessors scheduled after dependents."""
    deps = extract_dependencies(plan_items)
    
    for dependent, predecessor_ref in deps:
        if not dependent.date:
            continue
        # Find predecessor item
        predecessor = None
        for p in plan_items:
            if p.ref and (p.ref in predecessor_ref or predecessor_ref in p.ref):
                predecessor = p
                break
            if p.description and normalize(predecessor_ref) in normalize(p.description):
                predecessor = p
                break
        
        if predecessor and predecessor.date:
            if dependent.date < predecessor.date:
                issues.append(Issue(
                    "CRITICAL", 4,
                    f"'{dependent.description[:50]}' ({dependent.date.strftime('%d/%m/%y')}) "
                    f"scheduled BEFORE predecessor '{predecessor.description[:50]}' "
                    f"({predecessor.date.strftime('%d/%m/%y')})",
                    f"Reschedule '{dependent.description[:40]}' to after {predecessor.date.strftime('%d/%m/%y')} "
                    f"or confirm predecessor can be accelerated.",
                    dependent.ref
                ))


def check_review_buffer(plan_items, issues):
    """Check 5: Review Buffer — insufficient CG review time."""
    # Group by discipline
    discipline_groups = {}
    for item in plan_items:
        disc = item.discipline or "General"
        if disc not in discipline_groups:
            discipline_groups[disc] = []
        discipline_groups[disc].append(item)
    
    for disc, items in discipline_groups.items():
        items_with_dates = [i for i in items if i.date]
        items_with_dates.sort(key=lambda x: x.date)
        
        for i in range(1, len(items_with_dates)):
            gap = (items_with_dates[i].date - items_with_dates[i-1].date).days
            if gap < 7:  # Minimum 7 calendar days ≈ 5 working days
                issues.append(Issue(
                    "HIGH", 5,
                    f"'{disc}' submissions '{items_with_dates[i-1].description[:40]}' → "
                    f"'{items_with_dates[i].description[:40]}' only {gap} day gap "
                    f"(minimum 7 days for CG review)",
                    f"Stagger submissions by at least 7 calendar days (5 working days minimum).",
                    items_with_dates[i].ref
                ))


def check_duplicates(plan_items, all_plan_files, issues):
    """Check 6: Duplicate Detection — same item in multiple plans."""
    # This check requires loading all discipline plans, which is done externally
    # Here we check within a single plan
    seen = {}
    for item in plan_items:
        key = normalize(item.description)[:40]
        if key in seen:
            prev = seen[key]
            issues.append(Issue(
                "MEDIUM", 6,
                f"Duplicate item: '{item.description[:50]}' appears at line {prev.line} and {item.line}",
                f"Remove duplicate entry or clarify the difference between the two items.",
                item.ref
            ))
        else:
            seen[key] = item


def check_cross_register_sync(plan_items, register_items, issues):
    """Check 7: Cross-Register Sync — plan items missing from submittal register."""
    if not register_items:
        return
    
    register_descriptions = [normalize(r['description']) for r in register_items]
    
    for item in plan_items:
        if not item.description:
            continue
        norm = normalize(item.description)
        in_register = any(
            any(word in rd for word in norm.split() if len(word) > 4)
            for rd in register_descriptions
        )
        if not in_register:
            issues.append(Issue(
                "MEDIUM", 7,
                f"Plan item '{item.description[:60]}' not found in submittal register",
                f"Add this item to the submittal register with a proper ref code.",
                item.ref
            ))


def check_gate_compliance(plan_items, issues):
    """Check 8: Gate Compliance — items scheduled after gate deadline."""
    for item in plan_items:
        if not item.date or not item.gate:
            continue
        
        # Determine gate from item
        gate_key = None
        for gk in GATE_DEADLINES:
            if gk in item.gate:
                gate_key = gk
                break
        
        if gate_key and gate_key in GATE_DEADLINES:
            deadline = GATE_DEADLINES[gate_key]
            if item.date > deadline:
                issues.append(Issue(
                    "CRITICAL", 8,
                    f"'{item.description[:50]}' scheduled {item.date.strftime('%d/%m/%y')} "
                    f"but {gate_key} gate deadline is {deadline.strftime('%d/%m/%y')}",
                    f"Accelerate submission or formally request gate extension from CG.",
                    item.ref
                ))


def check_responsibility(plan_items, issues):
    """Check 9: Responsibility — items with no assigned party."""
    for item in plan_items:
        if not item.responsibility or item.responsibility.strip() in ('', '—', '-', 'TBC', 'TBD'):
            issues.append(Issue(
                "MEDIUM", 9,
                f"Item '{item.description[:60]}' has no assigned responsible party",
                f"Assign a responsible party (e.g., NRS, Samaya, Specialist name).",
                item.ref
            ))


def check_linked_activity_ids(plan_items, programme_milestones, issues):
    """Check 10: Linked Activity ID — programme codes missing from plan."""
    # This is a LOW severity check per skill rules
    items_without_id = [i for i in plan_items if not i.activity_id or i.activity_id.strip() in ('', '—', '-')]
    if items_without_id and programme_milestones:
        issues.append(Issue(
            "LOW", 10,
            f"{len(items_without_id)} items have no Linked Activity ID from the programme schedule",
            f"Add activity IDs from the programme schedule when confirmed. Per convention, leave empty until confirmed."
        ))


# ─── Report Generator ────────────────────────────────────────────────────────

def generate_report(issues, plan_items, programme_milestones, plan_name, output_path):
    """Generate a markdown validation report."""
    lines = []
    lines.append(f"# Submission Plan Validation Report")
    lines.append(f"")
    lines.append(f"**Plan:** {plan_name}")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Items Checked:** {len(plan_items)}")
    lines.append(f"**Issues Found:** {len(issues)}")
    lines.append(f"")
    
    # Summary table
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    check_counts = {}
    for iss in issues:
        severity_counts[iss.severity] = severity_counts.get(iss.severity, 0) + 1
        check_counts[iss.check] = check_counts.get(iss.check, 0) + 1
    
    lines.append(f"## Summary")
    lines.append(f"")
    lines.append(f"| Severity | Count |")
    lines.append(f"|----------|-------|")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        c = severity_counts.get(sev, 0)
        icon = "🔴" if sev == "CRITICAL" else "🟠" if sev == "HIGH" else "🟡" if sev == "MEDIUM" else "⚪"
        lines.append(f"| {icon} {sev} | {c} |")
    lines.append(f"")
    
    lines.append(f"| Check | Description | Issues |")
    lines.append(f"|-------|-------------|--------|")
    check_names = {
        1: "SOW Coverage", 2: "Scope Boundary", 3: "Schedule Alignment",
        4: "Dependency Chain", 5: "Review Buffer", 6: "Duplicates",
        7: "Cross-Register Sync", 8: "Gate Compliance", 9: "Responsibility",
        10: "Linked Activity ID"
    }
    for ck in range(1, 11):
        cnt = check_counts.get(ck, 0)
        name = check_names.get(ck, f"Check {ck}")
        icon = "✅" if cnt == 0 else "❌"
        lines.append(f"| {icon} {ck}. {name} | {cnt} |")
    lines.append(f"")
    
    # Issues by severity
    if issues:
        lines.append(f"## Issues")
        lines.append(f"")
        for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            sev_issues = [i for i in issues if i.severity == sev]
            if not sev_issues:
                continue
            icon = "🔴" if sev == "CRITICAL" else "🟠" if sev == "HIGH" else "🟡" if sev == "MEDIUM" else "⚪"
            lines.append(f"### {icon} {sev} ({len(sev_issues)})")
            lines.append(f"")
            lines.append(f"| # | Check | Item | Description | Recommendation |")
            lines.append(f"|---|-------|------|-------------|---------------|")
            for idx, iss in enumerate(sev_issues, 1):
                lines.append(f"| {idx} | {iss.check} | {iss.item_ref or '—'} | {iss.description} | {iss.recommendation} |")
            lines.append(f"")
    
    # Schedule timeline
    lines.append(f"## Schedule Timeline")
    lines.append(f"")
    items_with_dates = [i for i in plan_items if i.date]
    items_with_dates.sort(key=lambda x: x.date)
    
    if items_with_dates:
        min_date = items_with_dates[0].date
        max_date = items_with_dates[-1].date
        total_days = (max_date - min_date).days if max_date > min_date else 30
        
        for item in items_with_dates[:30]:  # Show first 30
            offset = int((item.date - min_date).days / max(total_days, 1) * 40)
            bar = "█" * max(1, offset // 2)
            lines.append(f"  {item.date.strftime('%d/%m')} {bar} {item.description[:60]}")
        
        if len(items_with_dates) > 30:
            lines.append(f"  ... ({len(items_with_dates) - 30} more items)")
    lines.append(f"")
    
    # Dependency graph
    deps = extract_dependencies(plan_items)
    if deps:
        lines.append(f"## Dependency Conflicts")
        lines.append(f"")
        for dependent, predecessor_ref in deps:
            pred = next((p for p in plan_items if p.ref and p.ref in predecessor_ref), None)
            if pred and dependent.date and pred.date:
                if dependent.date < pred.date:
                    lines.append(f"  ❌ {dependent.description[:40]} ← {pred.description[:40]} (INVERTED)")
                else:
                    lines.append(f"  ✅ {dependent.description[:40]} ← {pred.description[:40]}")
            else:
                lines.append(f"  ⚠️ {dependent.description[:40]} ← {predecessor_ref} (predecessor not found)")
        lines.append(f"")
    
    # Action items
    critical_high = [i for i in issues if i.severity in ("CRITICAL", "HIGH")]
    if critical_high:
        lines.append(f"## Action Items (Priority)")
        lines.append(f"")
        for idx, iss in enumerate(critical_high, 1):
            lines.append(f"{idx}. **[{iss.severity}]** {iss.description}")
            lines.append(f"   → {iss.recommendation}")
        lines.append(f"")
    
    # Write report
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))
    
    return output_path


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Validate a submission plan")
    parser.add_argument("--plan", required=True, help="Path to submission plan markdown file")
    parser.add_argument("--programme", help="Path to master programme markdown file")
    parser.add_argument("--register", help="Path to submittal register markdown file")
    parser.add_argument("--scope", help="Path to scope summary markdown file")
    parser.add_argument("--master-plan", help="Path to master submission plan (risk assessment)")
    parser.add_argument("--output", default="validation_report.md", help="Output report path")
    parser.add_argument("--all-plans", nargs="*", help="Paths to all discipline plans for cross-check")
    parser.add_argument("--recheck", action="store_true", help="Re-check mode (skip full extraction)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.plan):
        print(f"ERROR: Plan file not found: {args.plan}")
        sys.exit(1)
    
    # Extract plan items
    plan_items = extract_plan_items_markdown(args.plan)
    
    # Also extract from master plan if provided
    master_items = []
    if args.master_plan and os.path.exists(args.master_plan):
        master_items = extract_plan_items_master(args.master_plan)
        # Merge master items that match this discipline
        plan_name = Path(args.plan).stem.lower()
        for mi in master_items:
            if plan_name in normalize(mi.description):
                # Check if already in plan_items
                if not any(normalize(mi.description) in normalize(p.description) for p in plan_items):
                    plan_items.append(mi)
    
    # Extract programme milestones
    programme_milestones = {}
    if args.programme and os.path.exists(args.programme):
        programme_milestones = extract_programme_milestones(args.programme)
    
    # Extract register items
    register_items = []
    if args.register and os.path.exists(args.register):
        register_items = extract_register_items(args.register)
    
    # Extract scope items
    scope_items = []
    if args.scope and os.path.exists(args.scope):
        scope_items = extract_scope_items(args.scope)
    
    # Run all checks
    issues = []
    
    check_sow_coverage(plan_items, scope_items, issues)
    check_scope_boundary(plan_items, scope_items, issues)
    check_schedule_alignment(plan_items, programme_milestones, issues)
    check_dependency_chain(plan_items, issues)
    check_review_buffer(plan_items, issues)
    check_duplicates(plan_items, [], issues)
    check_cross_register_sync(plan_items, register_items, issues)
    check_gate_compliance(plan_items, issues)
    check_responsibility(plan_items, issues)
    check_linked_activity_ids(plan_items, programme_milestones, issues)
    
    # Generate report
    output_path = generate_report(issues, plan_items, programme_milestones, args.plan, args.output)
    
    print(f"✅ Validation complete: {len(issues)} issues found")
    print(f"   CRITICAL: {sum(1 for i in issues if i.severity == 'CRITICAL')}")
    print(f"   HIGH:     {sum(1 for i in issues if i.severity == 'HIGH')}")
    print(f"   MEDIUM:   {sum(1 for i in issues if i.severity == 'MEDIUM')}")
    print(f"   LOW:      {sum(1 for i in issues if i.severity == 'LOW')}")
    print(f"   Report: {output_path}")
    
    return 0 if not any(i.severity in ("CRITICAL", "HIGH") for i in issues) else 1


if __name__ == "__main__":
    sys.exit(main())
