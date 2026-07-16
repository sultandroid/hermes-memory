#!/usr/bin/env python3
"""
SysLeaders API Data Extractor
Usage: python3 extract.py <project_code>
Example: python3 extract.py 10   # Rateeb Store

Requires: curl, Python 3.7+
Output: /Volumes/MIcro/Work/Sysleaders/<project>_data.json
"""
import subprocess, re, json, sys, os, html as html_mod, tempfile
from pathlib import Path

BASE_URL = "https://www.sysleaders.com/samaya"
USERNAME = "sultan"
PASSWORD = "1batagoniaA"
COOKIE_FILE = "/tmp/sysleaders_cookies.txt"
DATA_DIR = Path("/Volumes/MIcro/Work/Sysleaders")

# === Project Registry ===
# Add new projects here. Discover entity_id and path via browser.
PROJECTS = {
    "10": {"entity_id": 282, "path": 49, "name": "Rateeb Store", "jn": "JN-Rateeb-Shop", "area": 42},
}

def curl(url, post_data=None, headers=None):
    """Run curl with session cookies, return response text via temp file (avoids subprocess truncation)."""
    tmpfile = tempfile.mktemp(suffix='.html')
    cmd = ["curl", "-s", "-L", "--compressed",
           "-b", COOKIE_FILE, "-c", COOKIE_FILE,
           "-o", tmpfile,
           "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"]
    if headers:
        for k, v in headers.items():
            cmd.extend(["-H", f"{k}: {v}"])
    if post_data:
        cmd.extend(["-X", "POST", "-d", post_data])
    cmd.append(url)
    subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        with open(tmpfile, 'r', encoding='utf-8', errors='ignore') as f:
            result = f.read()
    except:
        result = ""
    os.unlink(tmpfile)
    return result

def login():
    """Step 1: GET login page → extract CSRF token → POST login."""
    login_page = curl(f"{BASE_URL}/index.php?module=users/login")
    token_match = re.search(r'form_session_token.*?value="([^"]+)"', login_page)
    if not token_match:
        raise Exception("CSRF token not found")
    token = token_match.group(1)
    post = f"username={USERNAME}&password={PASSWORD}&form_session_token={token}"
    curl(f"{BASE_URL}/index.php?module=users/login&action=login", post_data=post)
    return token

def strip_html(text):
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', ' ', text).strip()
    text = re.sub(r'\s+', ' ', text)
    return html_mod.unescape(text).strip()

def fetch_pos_listing(project):
    """Use the listing API (reports_id=780) to get PO paths."""
    path = project["path"]
    post_data = (
        f"reports_id=780&reports_entities_id={path}&path={path}&page=1"
        f"&redirect_to=report_780&listing_container=entity_items_listing780_{path}"
    )
    html = curl(f"{BASE_URL}/index.php?module=items/listing", post_data=post_data,
                headers={"X-Requested-With": "XMLHttpRequest"})
    
    po_paths = []
    for m in re.finditer(r'href="[^"]*path=(\d+-\d+)[^"]*"', html):
        pp = m.group(1)
        if pp.startswith(f"{path}-"):
            po_paths.append(pp)
    return list(set(po_paths))

def fetch_po_detail(po_path):
    """Fetch PO info page and parse info table."""
    html = curl(f"{BASE_URL}/index.php?module=items/info&path={po_path}")
    
    info = {}
    for m in re.finditer(r'<tr[^>]*>.*?<t[dh][^>]*>(.*?)</t[dh]>\s*<t[dh][^>]*>(.*?)</t[dh]>.*?</tr>', html, re.DOTALL):
        key = strip_html(m.group(1)).rstrip(':').strip()
        val = strip_html(m.group(2)).strip()
        if key in ('SAR', 'SR', 'KWD', 'KD', 'USD', '$', '') or len(key) > 60:
            continue
        if key in ('ID', 'Date Added', 'Created By', 'Status', 'Order DAte', 'Due Date',
                    'Project', 'Ship To', 'Request by', 'Approved', 'Estimated Cost',
                    'Approve date', 'Approved By', 'items Count', 'PO finish'):
            info[key] = val
    
    just_match = re.search(r'Justification[^<]*</h\d>\s*(.*?)\s*<', html, re.DOTALL)
    if just_match:
        info['Justification'] = strip_html(just_match.group(1))
    
    po_num = f"PO{po_path.split('-')[1].zfill(5)}"
    return {"po_path": po_path, "po_number": po_num, "info": info}

def main():
    project_code = sys.argv[1] if len(sys.argv) > 1 else "10"
    if project_code not in PROJECTS:
        print(f"Unknown project. Known: {list(PROJECTS.keys())}")
        print("Add new projects to the PROJECTS dict with entity_id and path.")
        sys.exit(1)
    
    project = PROJECTS[project_code]
    print(f"Logging in...")
    token = login()
    print(f"Token: {token}")
    
    print(f"\nFetching {project['name']} POs...")
    po_paths = fetch_pos_listing(project)
    print(f"Found {len(po_paths)} POs: {po_paths}")
    
    pos = []
    total = 0
    for pp in po_paths:
        detail = fetch_po_detail(pp)
        info = detail["info"]
        cost_str = info.get("Estimated Cost", "0").replace("SAR", "").replace(",", "").strip()
        try:
            total += float(cost_str)
        except:
            pass
        print(f"  {detail['po_number']}: {info.get('Estimated Cost', '?')} | {info.get('Status', '?')}")
        pos.append(detail)
    
    result = {"project": project, "po_total": total, "pos": pos}
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_file = DATA_DIR / f"{project['name'].replace(' ', '_')}_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n=== {project['name']} ===")
    print(f"POs: {len(pos)} | Total: {total:,.2f} SAR")
    print(f"Saved: {output_file}")

if __name__ == "__main__":
    main()
