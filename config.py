import os
import platform

from pathlib import Path

# ==========================================
# SYSTEM INFO
# ==========================================

OS_NAME = platform.system()

BASE_DIR = Path(__file__).resolve().parent

# ==========================================
# DATA DIRECTORY
# ==========================================

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    exist_ok=True
)

# ==========================================
# UPLOADS DIRECTORY
# ==========================================

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    exist_ok=True
)

# ==========================================
# LOGS DIRECTORY
# ==========================================

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    exist_ok=True
)

# ==========================================
# DATABASE
# ==========================================

DB_PATH = DATA_DIR / "automation.db"

# ==========================================
# CHROME PROFILE
# ==========================================

PROFILE_PATH = (
    BASE_DIR / "chrome_profile"
)

PROFILE_PATH.mkdir(
    exist_ok=True
)

# ==========================================
# EXCEL SETTINGS
# ==========================================

ALLOWED_EXTENSIONS = [
    ".xlsx",
    ".xls"
]

MAX_EXCEL_ROWS = 10000

# ==========================================
# MESSAGE LIMITS
# ==========================================

MAX_MESSAGE_LENGTH = 4000

MAX_RECIPIENT_LENGTH = 200

# ==========================================
# RETRY CONFIG
# ==========================================

MAX_RETRY = 2

RETRY_DELAY = 5

# ==========================================
# POLLING
# ==========================================

POLL_INTERVAL = 5

# ==========================================
# DELAY CONFIG
# ==========================================

MIN_DELAY = 4

MAX_DELAY = 8

# ==========================================
# BATCH CONFIG
# ==========================================

BATCH_SIZE = 5

BATCH_COOLDOWN = 15

# ==========================================
# WORKER SETTINGS
# ==========================================

WORKER_NAME = "worker-1"

HEARTBEAT_INTERVAL = 30

# ==========================================
# CHROME SETTINGS
# ==========================================

HEADLESS = False

CHROME_START_MAXIMIZED = True

PAGE_LOAD_TIMEOUT = 60

IMPLICIT_WAIT = 10

# ==========================================
# WHATSAPP SETTINGS
# ==========================================

WHATSAPP_URL = (
    "https://web.whatsapp.com"
)

WHATSAPP_LOAD_TIMEOUT = 120

SEARCH_DELAY = 3

CHAT_OPEN_DELAY = 2

MESSAGE_PASTE_DELAY = 2

MESSAGE_SEND_DELAY = 3

# ==========================================
# TASK STATUS
# ==========================================

STATUS_PENDING = "PENDING"

STATUS_PROCESSING = "PROCESSING"

STATUS_SENT = "SENT"

STATUS_FAILED = "FAILED"

STATUS_RETRY = "RETRY"

# ==========================================
# LOG STATUS
# ==========================================

LOG_REQUEST_INITIATED = (
    "REQUEST_INITIATED"
)

LOG_PROCESSING = (
    "PROCESSING"
)

LOG_SENT = "SENT"

LOG_FAILED = "FAILED"

LOG_RETRY = "RETRY"

# ==========================================
# DASHBOARD
# ==========================================

DASHBOARD_PAGE_LIMIT = 50

# ==========================================
# SQLITE PERFORMANCE
# ==========================================

SQLITE_TIMEOUT = 30

ENABLE_WAL_MODE = True

# ==========================================
# SECURITY
# ==========================================

ENABLE_DUPLICATE_PROTECTION = True

ENABLE_TASK_LOCKING = True

# ==========================================
# RATE LIMIT SAFETY
# ==========================================

SAFE_MESSAGES_PER_MIN = 25

LONG_BREAK_AFTER = 25

LONG_BREAK_DURATION = 60

# ==========================================
# DEBUG
# ==========================================

DEBUG = True

VERBOSE_LOGGING = True

# ==========================================
# TERMINAL BANNER
# ==========================================

print("\n==============================")
print("SYSTEM CONFIGURATION")
print("==============================")

print(f"OS: {OS_NAME}")

print(f"BASE_DIR: {BASE_DIR}")

print(f"DB_PATH: {DB_PATH}")

print(f"PROFILE_PATH: {PROFILE_PATH}")

print("==============================\n")