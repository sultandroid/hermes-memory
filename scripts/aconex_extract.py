#!/usr/bin/env python3
"""
Aconex Daily Extractor — Aseer Museum
Logs into ksa1.aconex.com via Playwright headless browser,
extracts mail, documents, and workflow data,
saves snapshot for comparison.
"""
import asyncio, json, os, sys
from datetime import datetime
from playwright.async_api import async_playwright

HUB_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT_DIR = os.path.join(HUB_DIR, "05_Comms")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)
SNAPSHOT_FILE = os.path.join(SNAPSHOT_DIR, "aconex_snapshot_latest.json")
LOG_FILE = os.path.join(SNAPSHOT_DIR, "aconex_daily_sync.log")

USERNAME = "sultan@samayainvest.com"
PASSWORD = "1batagoniaA@25"

def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

async def extract():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        log("Navigating to Aconex login...")
        await page.goto("https://ksa1.aconex.com/Logon", timeout=60000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        
        # Fill Oracle JET login
        oj_inputs = await page.query_selector_all('oj-input-text')
        await oj_inputs[0].evaluate('el => el.value = "' + USERNAME + '"')
        await oj_inputs[0].evaluate('el => el.dispatchEvent(new Event("change"))')
        await oj_inputs[1].evaluate('el => el.value = "' + PASSWORD + '"')
        await oj_inputs[1].evaluate('el => el.dispatchEvent(new Event("change"))')
        
        oj_buttons = await page.query_selector_all('oj-button')
        await oj_buttons[0].click()
        await page.wait_for_timeout(15000)
        
        # Oracle IDCS password page
        pwd_field = await page.query_selector('input[type="password"]')
        if pwd_field:
            await pwd_field.fill(PASSWORD)
            signin = await page.query_selector('button:has-text("Sign In")')
            if signin:
                await signin.click()
                await page.wait_for_timeout(10000)
        
        log(f"Logged in. URL: {page.url}")
        
        # Navigate to hub and wait for full load
        await page.goto("https://ksa1.aconex.com/hub/index.html", timeout=30000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(5000)
        
        # Click "My mail received today" to trigger mail load
        search_link = await page.query_selector('a:has-text("My mail received today")')
        if search_link:
            await search_link.click()
            await page.wait_for_timeout(5000)
        
        # Also click "View All" for documents to expand
        view_all = await page.query_selector('a:has-text("View All")')
        if view_all:
            await view_all.click()
            await page.wait_for_timeout(3000)
        
        # Get tasks iframe content (has mail + document counts)
        tasks_frame = await page.query_selector('iframe[name="main"]')
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "mail": {},
            "documents": [],
            "transmittals": []
        }
        
        if tasks_frame:
            frame = await tasks_frame.content_frame()
            if frame:
                # Wait for content to load
                await page.wait_for_timeout(2000)
                text = await frame.inner_text('body')
                lines = text.split('\n')
                
                # Parse mail counts
                for line in lines:
                    line = line.strip()
                    if 'Unread To(' in line:
                        snapshot['mail']['unread_to'] = int(line.split('(')[1].split(')')[0])
                    elif 'Unread Cc(' in line:
                        snapshot['mail']['unread_cc'] = int(line.split('(')[1].split(')')[0])
                    elif 'Outstanding(' in line:
                        snapshot['mail']['outstanding'] = int(line.split('(')[1].split(')')[0])
                    elif 'Overdue(' in line:
                        snapshot['mail']['overdue'] = int(line.split('(')[1].split(')')[0])
                    elif 'Awaiting your Approval(' in line:
                        snapshot['mail']['awaiting_approval'] = int(line.split('(')[1].split(')')[0])
                
                # Parse transmittals
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    if line.startswith('SIC.-TRANSMIT') or line.startswith('CGP-TRANSMIT') or line.startswith('CGP-WTRAN'):
                        ref = line
                        subject = lines[i+1].strip() if i+1 < len(lines) else ""
                        sender = lines[i+2].strip() if i+2 < len(lines) else ""
                        date = lines[i+3].strip() if i+3 < len(lines) else ""
                        snapshot['transmittals'].append({
                            'ref': ref,
                            'subject': subject,
                            'from': sender,
                            'date': date
                        })
                        i += 4
                    else:
                        i += 1
        
        # Save snapshot
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        with open(SNAPSHOT_FILE, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        log(f"Snapshot saved: {len(snapshot['transmittals'])} transmittals, {snapshot.get('mail', {})}")
        
        # Compare with previous snapshot if exists
        prev_file = SNAPSHOT_FILE.replace('_latest.json', '_prev.json')
        if os.path.exists(SNAPSHOT_FILE):
            # Rotate: current becomes previous
            os.rename(SNAPSHOT_FILE, prev_file)
        
        # Save as current
        with open(SNAPSHOT_FILE, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        # Check for new items
        new_items = []
        if os.path.exists(prev_file):
            with open(prev_file) as f:
                prev = json.load(f)
            prev_refs = {t['ref'] for t in prev.get('transmittals', [])}
            for t in snapshot['transmittals']:
                if t['ref'] not in prev_refs:
                    new_items.append(t)
        
        if new_items:
            log(f"NEW ITEMS FOUND: {len(new_items)}")
            for item in new_items:
                log(f"  NEW: {item['ref']} — {item['subject']} ({item['date']})")
        else:
            log("No new items since last sync")
        
        await browser.close()
        return snapshot, new_items

if __name__ == "__main__":
    try:
        snapshot, new_items = asyncio.run(extract())
        print(json.dumps({"status": "ok", "count": len(snapshot['transmittals']), "new": len(new_items)}))
    except Exception as e:
        log(f"ERROR: {e}")
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
