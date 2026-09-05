# Normalized Submission DB — Build Pattern & Pitfalls

Session: 2026-09-05. Built `08_Document_Index/submission.db` as the single source
of truth for Aseer submission status, replacing three divergent markdown systems.

## Schema DDL

```sql
PRAGMA foreign_keys = ON;
CREATE TABLE discipline (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
CREATE TABLE doc_type   (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
CREATE TABLE status     (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE NOT NULL, label TEXT NOT NULL);
CREATE TABLE vendor     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
CREATE TABLE submission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_no TEXT NOT NULL,
    revision TEXT NOT NULL DEFAULT '',
    title TEXT,
    discipline_id INTEGER REFERENCES discipline(id),
    type_id INTEGER REFERENCES doc_type(id),
    status_id INTEGER REFERENCES status(id),
    vendor_id INTEGER REFERENCES vendor(id),
    submitted_date TEXT,
    days_silent INTEGER,
    source TEXT,
    updated_at TEXT,
    UNIQUE(doc_no, revision)          -- natural PK: prevents duplicate rows
);
CREATE INDEX idx_submission_docno ON submission(doc_no);
CREATE INDEX idx_submission_status ON submission(status_id);
CREATE INDEX idx_submission_discipline ON submission(discipline_id);
```

## Status code mapping (Aconex free-text → canonical)

```python
ACONEX_STATUS_TO_CODE = {
    'A - Approved': 'A', 'B - Approved with Comments': 'B',
    'C - Revise and Resubmit': 'C', 'D - Rejected': 'D',
    'E - Review Not Required': 'E',
    'For Information': 'F', 'For Approval': 'F',
    'For Review': 'U', 'Open': 'U', 'Pending': 'U', 'Under Review': 'U',
    'Closed': 'CL',
}
```

## Ingestion order (multi-source, one DB)

1. **Aconex export** — parse `Docs` sheet (header row 11, data from row 12),
   dedupe attachment copies by `(base_docno, revision)`, compute `days_silent`
   from `min(Revision Date, Date Modified)`.
2. **CG codes from repo registers** — regex-extract `{docno: code}` from
   `submittal_register.md` + `submission_tracker.md`. Only override an Aconex
   status if current is awaiting (`U`) OR the merge code is a definitive B/C/D.
3. **IFC packages** — NOT in the Aconex export. Parse rows like
   `| IFC-0003 | Flooring | 2026-04-22 | — | **DA** |` from the repo registers
   and upsert separately with `type='IFC'`, `discipline='IFC'`.

## Pitfalls (all hit this session)

- **`re.sub` replacement with `\u` escapes → `bad escape \u`.** When injecting a
  JS object containing `\uXXXX` (or any backslash) via `re.sub`, the replacement
  string is parsed as a template. Fix: use a lambda — `re.sub(pattern, lambda m: new_data, html)`.
- **`datetime.strptime('22-Apr', '%d-%b')` defaults to year 1900.** Any
  day-month date without a year parses as 1900 → `days_silent` becomes ~46000
  and the dashboard shows "1900-". Fix: after parsing, if `year == 1900`,
  `replace(year=datetime.now().year)`.
- **IFC-0005 with code `—` (no code) is missed by a regex that only matches
  `[A-E]|DA|TBV`.** Include `—` in the alternation and map it to `U`.
- **HSE table polluted by NCRs / Site Instructions / reports.** Filter the HSE
  query to plan-type doc_types only (`NOT IN ('Non-Conformance Report',
  'Site Instruction', 'HSE Report', 'Weekly Progress Report', 'Daily Progress Report')`).
- **Deemed Approved (DA) is DERIVED, not stored.** Aconex never stores DA. In
  the dashboard query, treat `status='DA'` OR (`status='U'` AND `days_silent > 14`)
  as deemed approved (ER §2.4.A).
- **`.gitignore` must exclude `*.xlsx` and `*.db`** so the snapshot files and the
  DB are never committed — the repo stays clean and the DB is rebuilt on demand.

## Dashboard queries (the 6 DATA sections)

- `total` → `SELECT COUNT(*) FROM submission`
- `categories` → aggregate by mapped doc_type→category, count by status code
- `deemedApproved` → DA or (U AND days>14), ordered by days_silent DESC
- `ifc` → `doc_no LIKE '%IFC%'`
- `hse` → discipline='Health & Safety' AND plan-type doc_types
- `overdue` → status='U' AND days_silent > 14

## Verification

```bash
# No duplicate rows (natural PK holds):
SELECT doc_no, revision, COUNT(*) c FROM submission GROUP BY doc_no, revision HAVING c>1;
# Lookup tables hold each value once:
SELECT COUNT(*) FROM discipline;  -- 14
SELECT COUNT(*) FROM doc_type;     -- 25
SELECT COUNT(*) FROM status;       -- 8
SELECT COUNT(*) FROM vendor;       -- 103
```
