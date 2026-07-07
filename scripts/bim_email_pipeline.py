#!/usr/bin/env python3
"""
BIM EMAIL PIPELINE v2.1 — Samaya BIM Unit
══════════════════════════════════════════
Checks Outlook every N hours, downloads new emails,
classifies by project, extracts attachments to proper
subfolders, and updates Excel registers.

Architecture:
  Outlook (macOS) → AppleScript → Python Processor
    → Classify (Project + Category)
    → Download Attachments
    → Copy to Project Subfolders
    → Archive as MD
    → Update Excel Registers
"""

import os, re, sys, json, shutil, subprocess, atexit, logging
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

# ──────────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────────
BIM_UNIT = os.environ.get("BIM_UNIT_PATH") or os.path.expanduser(
    "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit"
)
STATE_FILE = os.path.expanduser("~/.hermes/scripts/.email_pipeline_state.json")
LOCK_FILE  = os.path.expanduser("~/.hermes/scripts/.email_pipeline.lock")
LOG_FILE   = os.path.expanduser("~/.hermes/scripts/bim_email_pipeline.log")
ATTACHMENTS_DIR = os.path.expanduser("~/Downloads/_email_attachments")
UNSORTED_EMAILS = os.path.join(BIM_UNIT, "_Unsorted_Emails", "Email_Archive")

MAX_BODY_CHARS       = 5000
MAX_EMAILS_PER_FOLDER = 50
MAX_TRACKED_IDS      = 5000
MAX_ATTACHMENTS      = 20
APPLESCRIPT_TIMEOUT  = 120
ATTACHMENT_CLEANUP_AGE = 7  # days — delete downloaded originals after this

# AppleScript file paths (more reliable than inline -e)
FETCH_SCRIPT_PATH = os.path.expanduser("~/.hermes/scripts/bim_fetch_emails.applescript")
DOWNLOAD_SCRIPT_PATH = os.path.expanduser("~/.hermes/scripts/bim_download_attachment.applescript")

DRY_RUN  = "--dry-run" in sys.argv or "--plan" in sys.argv
VERBOSE  = "-v" in sys.argv or "--verbose" in sys.argv

# ──────────────────────────────────────────────────────────────────────────────
# LOGGING  (rotating)
# ──────────────────────────────────────────────────────────────────────────────
log = logging.getLogger("email_pipeline")
log.setLevel(logging.DEBUG if VERBOSE else logging.INFO)
_fh = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5)
_fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
log.addHandler(_fh)
_ch = logging.StreamHandler(sys.stdout)
_ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
log.addHandler(_ch)

# ──────────────────────────────────────────────────────────────────────────────
# LOCK  (prevent concurrent execution)
# ──────────────────────────────────────────────────────────────────────────────
def acquire_lock() -> None:
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE) as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            log.error(f"Another instance (PID {pid}) is already running. Exiting.")
            sys.exit(1)
        except (ProcessLookupError, ValueError, OSError):
            pass  # stale lock → overwrite
    if not DRY_RUN:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))
    log.debug(f"Lock acquired (PID {os.getpid()})")

def release_lock() -> None:
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
            log.debug("Lock released")
    except OSError:
        pass

atexit.register(release_lock)

# ──────────────────────────────────────────────────────────────────────────────
# STATE  (atomic writes + corruption recovery)
# ──────────────────────────────────────────────────────────────────────────────
def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            log.warning("State file corrupt — backing up and starting fresh")
            try:
                shutil.copy2(STATE_FILE, STATE_FILE + ".bak")
            except OSError:
                pass
            return {"last_run": None, "processed_ids": []}
    return {"last_run": None, "processed_ids": []}

def save_state(state: dict) -> None:
    if DRY_RUN:
        return
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2, default=str)
    os.replace(tmp, STATE_FILE)  # atomic on POSIX

# ──────────────────────────────────────────────────────────────────────────────
# APPLESCRIPT HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def run_osascript(
    script_path: str,
    args: list[str] | None = None,
    timeout: int = APPLESCRIPT_TIMEOUT,
    retries: int = 2,
) -> subprocess.CompletedProcess | None:
    """Run an AppleScript file with retry + exponential backoff."""
    cmd = ["osascript", script_path]
    if args:
        cmd.extend(args)

    for attempt in range(1, retries + 2):
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout
            )
            if proc.returncode == 0:
                return proc
            log.warning(f"osascript attempt {attempt} failed (rc={proc.returncode}): "
                        f"{proc.stderr.strip()[:100]}")
        except subprocess.TimeoutExpired:
            log.warning(f"osascript attempt {attempt} timed out ({timeout}s)")
        except Exception as e:
            log.warning(f"osascript attempt {attempt} error: {e}")

        if attempt < retries + 1:
            import time
            time.sleep(2 ** attempt)  # backoff: 2s, 4s, 8s
    return None

# ──────────────────────────────────────────────────────────────────────────────
# OUTLOOK EMAIL FETCH
# ──────────────────────────────────────────────────────────────────────────────
def fetch_recent_emails(folder_name: str, max_n: int = MAX_EMAILS_PER_FOLDER) -> list[dict]:
    """Fetch the most recent N emails from an Outlook folder.  Returns parsed list."""
    result = run_osascript(FETCH_SCRIPT_PATH, [folder_name, str(max_n)])
    if result is None:
        log.error(f"  AppleScript failed for '{folder_name}' after retries")
        return []
    if result.stdout.startswith("ERR|"):
        log.warning(f"  {result.stdout.strip()}")
        return []
    return _parse_email_dump(result.stdout)

def download_attachment(folder_name: str, msg_id: str, att_name: str, output_dir: str) -> str | None:
    """Download one attachment directly by message ID (O(1) lookup)."""
    safe_name = re.sub(r'[\\/*?:"<>|]', "_", att_name)
    if not safe_name:
        return None
    output_path = os.path.join(output_dir, safe_name)
    if os.path.exists(output_path):
        return output_path

    result = run_osascript(
        DOWNLOAD_SCRIPT_PATH,
        [folder_name, msg_id, att_name, output_path],
    )
    if result and result.stdout.strip() not in ("", "NOT_FOUND") and os.path.exists(result.stdout.strip()):
        path = result.stdout.strip()
        log.info(f"    ✅ Downloaded: {safe_name} ({os.path.getsize(path)} bytes)")
        return path
    log.warning(f"    ⚠️ Failed: {safe_name}")
    return None

def _parse_email_dump(text: str) -> list[dict]:
    """Parse ===EMAIL=== / ===END=== format into list of dicts."""
    emails = []
    for block in text.strip().split("===EMAIL==="):
        block = block.strip()
        if not block:
            continue
        email: dict = {}
        atts: list[str] = []
        lines = block.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("ID:"):
                email["id"] = line[3:].strip()
            elif line.startswith("FROM:"):
                email["sender"] = line[5:].strip()
            elif line.startswith("DATE:"):
                email["date"] = line[5:].strip()
            elif line.startswith("SUBJ:"):
                email["subject"] = line[5:].strip()
            elif line.startswith("BODY:"):
                body_parts: list[str] = []
                i += 1
                while i < len(lines) and not lines[i].startswith("ATT:") and not lines[i].startswith("===END==="):
                    body_parts.append(lines[i])
                    i += 1
                email["body"] = "\n".join(body_parts).strip()
                continue
            elif line.startswith("ATT:"):
                atts.append(line[4:].strip())
            elif line.startswith("===END==="):
                email["attachments"] = atts
                if email.get("id"):
                    emails.append(email)
                break
            i += 1
        if email.get("id") and "attachments" not in email:
            email["attachments"] = atts
            emails.append(email)
    return emails

# ──────────────────────────────────────────────────────────────────────────────
# CLASSIFICATION
# ──────────────────────────────────────────────────────────────────────────────
PROJECT_CONTEXT = {
    "Zamzam": {
        "people": ["almakarem", "aboulmakarem", "m.almakarem", "wesam"],
        "keywords": [r"زمزم", r"zamzam", r"zvc", r"visitor\s*center", r"مركز\s*الزوار"],
        "codes": [r"\bZVC\b", r"\bZM-\d", r"\bZamzam"],
        "folder": "Zamzam Museum"
    },
    "Aser": {
        "people": ["nissen", "jim.r", "rcrc", "egec", "yaser.alattas", "medhat"],
        "keywords": [r"عسير", r"aseer", r"asher", r"nissen", r"متحف\s*عسير", r"regional\s*museum"],
        "codes": [r"\bOC-ASER\b", r"\bASER-\d", r"\bARM\b"],
        "folder": "Aseer-Museum"
    },
    "AlFaw": {
        "people": [],
        "keywords": [r"الفاو", r"alfaw", r"unesco", r"اليونسكو"],
        "codes": [r"\bALF-\d", r"\bAlFaw"],
        "folder": "04_Al_Faw"
    },
    "ElGhamama": {
        "people": [],
        "keywords": [r"غمامة", r"ghamama", r"قهوتنا"],
        "codes": [r"\bEG-\d"],
        "folder": "El-Ghamama Museum"
    },
    "Haramain": {
        "people": [],
        "keywords": [r"حرمين", r"haramain", r"el.haramain"],
        "codes": [r"\bEH-\d"],
        "folder": "El-Haramain Museum"
    },
}

CATEGORY_RULES: list[tuple[str, str | None, str | None]] = [
    ("MAR", r"\bmar\b|material\s*approval", r"مواد|عينة|اعتماد\s*مواد"),
    ("MIR", r"\bmir\b|material\s*inspection", r"فحص\s*مواد"),
    ("IR",  r"\bir\b|inspection\s*request", r"استلام|طلب\s*فحص"),
    ("SDR", r"\bsdr\b|shop\s*drawing", r"مخطط\s*تنفيذي"),
    ("RFI", r"\brfi\b|request\s*for\s*info", r"استفسار|طلب\s*معلومات"),
    ("WIR", r"\bwir\b|work\s*inspection", r"بدء\s*أعمال"),
    ("RFP", r"\brfp\b|request\s*for\s*proposal", r"مقترح|عرض\s*سعر"),
    ("DOC", r"\bdoc\b|transmittal", r"مستند|قائمة|إرسال"),
    ("SCH", r"\bsch\b|schedule|program", r"زمني|برنامج|جدول"),
    ("REP", r"\brep\b|weekly|monthly\s*report", r"تقرير|أسبوعي|شهري"),
    ("SI",  r"\bsi\b|site\s*instruction", r"ملاحظة\s*موقع|تعليمات"),
    ("MIN", r"\bmin\b|minutes|mom|meeting", r"محضر\s*اجتماع"),
    ("NCR", r"\bncr\b|non.conformance", r"عدم\s*مطابقة"),
    ("MSG", None, None),
]

REGISTER_MAP = {
    "SDR": "Submittal_Register", "MAR": "Submittal_Register", "MIR": "Submittal_Register",
    "IR": "Inspection_Register", "RFI": "RFI_Register", "SI": "SI_Register",
    "NCR": "NCR_Register", "MIN": "Meeting_Minutes_Register",
    "DOC": "Transmittal_Register", "SCH": "Submittal_Register",
    "REP": "Submittal_Register", "WIR": "Submittal_Register",
    "RFP": "Submittal_Register", "MSG": "Correspondence_Log",
}

def classify_project(email: dict) -> str:
    """Score each project; return highest-scoring project name or 'General'."""
    text = f"{email.get('subject','')} {email.get('body','')} {email.get('sender','')}".lower()
    scores: dict[str, int] = {}
    for proj, ctx in PROJECT_CONTEXT.items():
        score = 0
        for kw in ctx["keywords"]:
            if re.search(kw, text, re.IGNORECASE):
                score += 10
        for c in ctx["codes"]:
            if re.search(c, text, re.IGNORECASE):
                score += 50
        for p in ctx["people"]:
            if p.lower() in text:
                score += 30
        if score > 0:
            scores[proj] = score
    if not scores:
        return "General"
    return max(scores, key=scores.get)

def classify_category(text: str) -> str:
    """Classify email type. Returns one of CATEGORY_RULES labels or 'MSG'."""
    for label, eng, ar in CATEGORY_RULES:
        if not label or label == "MSG":
            continue
        if eng and re.search(eng, text, re.IGNORECASE):
            return label
        if ar and re.search(ar, text, re.IGNORECASE):
            return label
    return "MSG"

# ──────────────────────────────────────────────────────────────────────────────
# FILE MANAGEMENT
# ──────────────────────────────────────────────────────────────────────────────
def get_discipline_subfolder(filename: str, category: str) -> str:
    """Map file to project subfolder based on category and filename hints."""
    n = filename.lower()
    if category == "SDR":
        return "02_Submittals/01_Shop Drawings"
    elif category == "MAR":
        return "02_Submittals/02_Material Samples"
    elif category == "RFI":
        return "02_Submittals/03_Method Statements"
    elif category in ("IR", "MIR"):
        return "09_Site/01_Inspection Requests"
    elif category == "SI":
        return "09_Site/00_Site Instructions"
    elif category == "MIN":
        return "07_Meetings/00_Minutes of Meetings"
    elif category == "REP":
        return "08_Schedules/02_Progress Reports"
    elif category == "SCH":
        return "08_Schedules/00_Master Program"
    elif category == "NCR":
        return "09_Site/03_Snag Lists"
    elif category == "DOC":
        return "00_Admin/01_Correspondence"
    # Discipline fallback
    if re.search(r'\b(struc|str\.|structural)\b', n):
        return "04_Drawings/01_Structural"
    elif re.search(r'\b(arch|ar\.|architectural)\b', n):
        return "04_Drawings/00_Architectural"
    elif re.search(r'\b(mep|mech|hvac|elec|plumb|fire)\b', n):
        return "04_Drawings/02_MEP"
    elif re.search(r'\b(landscape|external)\b', n):
        return "04_Drawings/03_Landscape"
    elif re.search(r'\b(interior|finish|ff&e|furniture)\b', n):
        return "04_Drawings/04_Interior"
    return "01_Client Inbox"

def unique_path(directory: str, filename: str) -> str:
    """Return a path that does not already exist (append _1, _2, ...)."""
    target = os.path.join(directory, filename)
    if not os.path.exists(target):
        return target
    stem, ext = os.path.splitext(filename)
    for c in range(1, 100):
        candidate = os.path.join(directory, f"{stem}_{c}{ext}")
        if not os.path.exists(candidate):
            return candidate
    return os.path.join(directory, f"{stem}_{os.urandom(4).hex()}{ext}")

def copy_to_project(
    att_path: str, project_key: str, category: str, filename: str
) -> str | None:
    """Copy attachment to the correct BIM project subfolder."""
    ctx = PROJECT_CONTEXT.get(project_key)
    if not ctx or project_key == "General":
        target_dir = os.path.join(UNSORTED_EMAILS, "..", "attachments")
    else:
        subfolder = get_discipline_subfolder(filename, category)
        target_dir = os.path.join(BIM_UNIT, ctx["folder"], subfolder)
    os.makedirs(target_dir, exist_ok=True)
    target = unique_path(target_dir, filename)

    if not DRY_RUN:
        shutil.copy2(att_path, target)
        rel = os.path.relpath(target, BIM_UNIT)
        log.info(f"    📁 → {rel}")
    else:
        log.info(f"    📁 [DRY] → {os.path.relpath(target, BIM_UNIT)}")
    return target

# ──────────────────────────────────────────────────────────────────────────────
# EMAIL ARCHIVING
# ──────────────────────────────────────────────────────────────────────────────
def archive_email(email: dict, project: str, category: str, att_paths: list[str]) -> str | None:
    """Save email as Markdown (YAML frontmatter) to Email_Archive."""
    date_str = (email.get("date") or "unknown")[:10]
    safe_subj = re.sub(r'[\\/*?:"<>|]', "_", (email.get("subject") or "no-subject"))[:60]
    filename = f"{date_str} - {safe_subj}.md"
    archive_dir = UNSORTED_EMAILS
    os.makedirs(archive_dir, exist_ok=True)
    filepath = unique_path(archive_dir, filename)

    body = (email.get("body") or "")[:MAX_BODY_CHARS]
    content = f"""---
date: {email.get('date','?')}
from: {email.get('sender','?')}
subject: {email.get('subject','?')}
project: {project}
category: {category}
archived: {datetime.now().isoformat()}
attachments: {len(att_paths)}
---

# {email.get('subject','No Subject')}

**From:** {email.get('sender','?')}
**Date:** {email.get('date','?')}
**Project:** {project}
**Category:** {category}

---

{body}

---
"""
    for ap in att_paths:
        content += f"- {ap}\n"

    if not DRY_RUN:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        log.info(f"    📝 Archived: {os.path.basename(filepath)}")
    return filepath

# ──────────────────────────────────────────────────────────────────────────────
# REGISTER UPDATE (v2.1 stub — full integration in v2.2)
# ──────────────────────────────────────────────────────────────────────────────
def update_register(project_key: str, category: str) -> str:
    """Route an email to the correct Excel register."""
    register = REGISTER_MAP.get(category, "Submittal_Register")
    log.info(f"    📊 Register: {register} ← entry pending")
    return register

# ──────────────────────────────────────────────────────────────────────────────
# ATTACHMENT CLEANUP
# ──────────────────────────────────────────────────────────────────────────────
def cleanup_old_downloads() -> int:
    """Remove downloaded attachment originals older than ATTACHMENT_CLEANUP_AGE days."""
    if DRY_RUN or not os.path.exists(ATTACHMENTS_DIR):
        return 0
    now = datetime.now()
    removed = 0
    for root, dirs, files in os.walk(ATTACHMENTS_DIR):
        for f in files:
            fp = os.path.join(root, f)
            try:
                age_hours = (now - datetime.fromtimestamp(os.path.getmtime(fp))).total_seconds()
                if age_hours > ATTACHMENT_CLEANUP_AGE * 86400:
                    os.remove(fp)
                    removed += 1
            except OSError:
                pass
    if removed:
        log.info(f"  🧹 Cleaned {removed} old downloaded attachments")
    return removed

# ──────────────────────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ──────────────────────────────────────────────────────────────────────────────
def process_folder(folder_name: str, state: dict) -> int:
    """Fetch, classify, archive, copy, and register-update new emails from one folder."""
    log.info(f"\n📬 Checking '{folder_name}'...")
    emails = fetch_recent_emails(folder_name, MAX_EMAILS_PER_FOLDER)
    if not emails:
        return 0

    processed = 0
    processed_set = set(state.get("processed_ids", []))

    for email in emails:
        eid = email.get("id")
        if not eid or eid in processed_set:
            continue

        subject = (email.get("subject") or "?")[:70]
        log.info(f"  📧 [{eid[:8]}…] {subject}")

        combined_text = f"{subject} {email.get('body','')}"
        project = classify_project(email)
        category = classify_category(combined_text)
        log.info(f"    → {project} / {category}")

        att_paths: list[str] = []
        for att_name in (email.get("attachments") or [])[:MAX_ATTACHMENTS]:
            att_dir = os.path.join(ATTACHMENTS_DIR, folder_name, eid)
            os.makedirs(att_dir, exist_ok=True)
            ap = download_attachment(folder_name, eid, att_name, att_dir)
            if ap:
                copied = copy_to_project(ap, project, category, att_name)
                if copied:
                    att_paths.append(copied)

        archive_email(email, project, category, att_paths)
        update_register(project, category)

        processed_set.add(eid)
        state["processed_ids"] = list(processed_set)
        processed += 1

    # Prune to MAX_TRACKED_IDS
    if len(state["processed_ids"]) > MAX_TRACKED_IDS:
        state["processed_ids"] = state["processed_ids"][-MAX_TRACKED_IDS:]

    return processed

def main() -> None:
    has_errors = False
    start = datetime.now()
    log.info("=" * 60)
    log.info(f"BIM EMAIL PIPELINE v2.1  |  Mode: {'DRY-RUN' if DRY_RUN else 'LIVE'}")
    log.info(f"Start: {start.isoformat()}")
    log.info("=" * 60)

    if not DRY_RUN:
        acquire_lock()

    state = load_state()
    processed_count = len(state.get("processed_ids", []))
    log.info(f"Previously tracked: {processed_count} emails")
    if state.get("last_run"):
        last = state["last_run"]
        try:
            delta = start - datetime.fromisoformat(last)
            log.info(f"Last run: {last}  ({delta.total_seconds()/3600:.1f}h ago)")
        except Exception:
            log.info(f"Last run: {last}")

    total = 0
    for folder in ["Inbox"]:
        try:
            total += process_folder(folder, state)
        except Exception as e:
            log.error(f"Fatal error on '{folder}': {e}", exc_info=VERBOSE)
            has_errors = True

    state["last_run"] = start.isoformat()
    if total > 0:
        save_state(state)

    cleanup_old_downloads()

    elapsed = (datetime.now() - start).total_seconds()
    log.info(f"\n{'=' * 60}")
    log.info(f"Done in {elapsed:.1f}s  |  New: {total}  |  Tracked: {len(state.get('processed_ids',[]))}")
    log.info(f"{'=' * 60}")

    # Exit codes for cron monitoring
    if has_errors:
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
