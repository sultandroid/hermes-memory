#!/usr/bin/env python3
"""
Factory Warehouse Receipt Monitor — CORRECTED VERSION
Checks stock pickings on FA/WH/FA (Factory Warehouse) and flags only those
whose purchase order's project_id is NOT Samaya Factory (244).

Classification logic:
  - Get all stock pickings on FA/WH/FA warehouse (location_dest_id = 45)
  - For each, get the origin (PO reference)
  - Look up the PO's project_id
  - If project_id != 244 (Samaya Factory) → flag as wrong warehouse
  - If project_id == 244 → correct, skip

Usage:
  python3 factory_warehouse_monitor.py [--days 7] [--delete-notes]

Output:
  Prints summary to stdout. Posts notes to Odoo chatter if --delete-notes is set.
"""

import os
import sys
import re
import xmlrpc.client
from datetime import datetime, timedelta

ODOO_URL = os.environ.get('ODOO_URL', 'https://samayainv.odoo.com')
ODOO_DB = os.environ.get('ODOO_DB', 'peerless-tech-samaya-18-0-18447146')
ODOO_USER = os.environ.get('ODOO_USER', 'sultan@samayainvest.com')

def _load_api_key():
    """Load ODOO_API_KEY from ~/.config/samaya/odoo.env (cron has no env vars)."""
    key = os.environ.get('ODOO_API_KEY', '')
    if key:
        return key
    env_path = os.path.expanduser('~/.config/samaya/odoo.env')
    try:
        with open(env_path) as f:
            for line in f:
                if line.startswith('ODOO_API_KEY='):
                    return line.split('=', 1)[1].strip()
    except OSError:
        pass
    return ''

ODOO_KEY = _load_api_key()

FACTORY_PROJECT_ID = 244
FACTORY_WAREHOUSE_LOCATION_ID = 45  # Physical Locations/Factory

def connect():
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_KEY, {})
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return uid, models

def get_recent_factory_pickings(uid, models, days=7):
    """Get all stock pickings on FA/WH/FA warehouse in last N days."""
    since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
    pickings = models.execute_kw(ODOO_DB, uid, ODOO_KEY, 'stock.picking', 'search_read',
        [[
            ['location_dest_id', '=', FACTORY_WAREHOUSE_LOCATION_ID],
            ['date_done', '>=', since],
            ['state', '=', 'done'],
            ['picking_type_code', '=', 'incoming'],
        ]],
        {'fields': ['name', 'id', 'origin', 'date_done'], 'limit': 200})
    return pickings

def get_po_project(uid, models, po_name):
    """Get project_id for a PO. Returns (id, name) or (0, 'Unknown')."""
    pos = models.execute_kw(ODOO_DB, uid, ODOO_KEY, 'purchase.order', 'search_read',
        [[['name', '=', po_name]]],
        {'fields': ['name', 'project_id'], 'limit': 1})
    if pos and pos[0].get('project_id'):
        return pos[0]['project_id']
    return [0, 'Unknown']

def post_note(uid, models, picking_id, message):
    """Post a note to the picking's chatter."""
    models.execute_kw(ODOO_DB, uid, ODOO_KEY, 'stock.picking', 'message_post',
        [picking_id], {'body': message, 'message_type': 'comment'})

NOTE_MARKER = 'تأكيد مخزن المصنع'

def already_noted(uid, models, picking_id):
    """True if this monitor already posted its marker note to this picking's chatter."""
    msgs = models.execute_kw(ODOO_DB, uid, ODOO_KEY, 'mail.message', 'search_read',
        [[
            ['model', '=', 'stock.picking'],
            ['res_id', '=', picking_id],
            ['body', 'ilike', NOTE_MARKER],
        ]],
        {'fields': ['id'], 'limit': 1})
    return bool(msgs)

def main():
    days = 7
    delete_notes = False
    
    for arg in sys.argv[1:]:
        if arg.startswith('--days='):
            days = int(arg.split('=')[1])
        elif arg == '--delete-notes':
            delete_notes = True

    uid, models = connect()
    pickings = get_recent_factory_pickings(uid, models, days)
    
    wrong = []
    correct = []
    untrackable = []
    already_flagged = []
    
    for p in pickings:
        origin = p.get('origin', '')
        if not origin:
            untrackable.append(p)
            continue
        
        # Extract PO number from origin
        po_match = re.search(r'P\d+', origin)
        if not po_match:
            untrackable.append(p)
            continue
        
        po_name = po_match.group(0)
        proj = get_po_project(uid, models, po_name)
        proj_id = proj[0]
        proj_name = proj[1]
        
        if proj_id == FACTORY_PROJECT_ID:
            correct.append(p)
        else:
            if already_noted(uid, models, p['id']):
                already_flagged.append({'picking': p, 'po': po_name, 'project': proj_name, 'project_id': proj_id})
            else:
                wrong.append({'picking': p, 'po': po_name, 'project': proj_name, 'project_id': proj_id})
    
    # Output — plain text, no icons, no tags
    print(f'Warehouse Receipt Check ({datetime.now().strftime("%Y-%m-%d %H:%M")})')
    print(f'Period: last {days} days')
    print(f'Total receipts on FA/WH/FA: {len(pickings)}')
    print(f'Correct (factory PO): {len(correct)}')
    print(f'Wrong warehouse, already flagged (skipped): {len(already_flagged)}')
    print(f'Wrong warehouse, new: {len(wrong)}')
    print(f'Untrackable: {len(untrackable)}')
    print()
    
    if wrong:
        print('WRONG WAREHOUSE — receipts on factory warehouse for non-factory POs:')
        print()
        for w in wrong:
            p = w['picking']
            print(f'  {p["name"]} ({p.get("date_done","?")[:10]})')
            print(f'    PO: {w["po"]} | Project: {w["project"]} (ID {w["project_id"]})')
            print(f'    Link: {ODOO_URL}/web#id={p["id"]}&model=stock.picking&view_type=form')
            print()
        
        if delete_notes:
            for w in wrong:
                p = w['picking']
                msg = (
                    f'[تأكيد المخزن]\n'
                    f'تم استلام هذا الأمر على مخزن المصنع لكن طلب الشراء '
                    f'({w["po"]}) يخص مشروع: {w["project"]} — وليس المصنع.'
                )
                post_note(uid, models, p['id'], msg)
                print(f'  Note posted to {p["name"]}')
    
    if correct:
        print(f'Correct receipts (factory POs, skipped): {len(correct)}')
    
    if untrackable:
        print(f'Untrackable (no PO reference): {len(untrackable)}')

if __name__ == '__main__':
    main()
