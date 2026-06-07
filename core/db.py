import sqlite3
import os

from config import DB_PATH


# ==========================================
# CONNECTION
# ==========================================

def get_connection():

    os.makedirs(
        "data",
        exist_ok=True
    )

    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False,
        timeout=30
    )

    conn.row_factory = sqlite3.Row

    # ======================================
    # PERFORMANCE
    # ======================================

    conn.execute(
        "PRAGMA journal_mode=WAL;"
    )

    conn.execute(
        "PRAGMA foreign_keys=ON;"
    )

    conn.execute(
        "PRAGMA synchronous=NORMAL;"
    )

    return conn


# ==========================================
# INIT DATABASE
# ==========================================

def init_db():

    conn = get_connection()

    cur = conn.cursor()

    # ======================================
    # TASK TABLE
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        recipient TEXT NOT NULL,

        recipient_type TEXT NOT NULL,

        message TEXT NOT NULL,

        schedule_time TEXT,

        status TEXT DEFAULT 'PENDING',

        retry_count INTEGER DEFAULT 0,

        processing_time REAL,

        created_at TEXT
    )
    """)

    # ======================================
    # LOG TABLE
    # ======================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        task_id INTEGER,

        status TEXT,

        processing_time REAL,

        timestamp TEXT,

        remark TEXT
    )
    """)

    conn.commit()

    conn.close()

    print(
        "Database Initialized Successfully"
    )