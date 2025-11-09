import sqlite3
from config import DATABASE_PATH

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,  -- 'admin', 'worker', 'observer'
            is_active BOOLEAN DEFAULT 1,
            joined_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            location TEXT,
            latitude REAL,
            longitude REAL,
            datetime TEXT,
            additional_params TEXT, -- JSON-like string
            photos TEXT,            -- comma-separated file_ids
            assigned_to TEXT,       -- 'self', 'user_id', 'group', 'all'
            created_by INTEGER,
            status TEXT DEFAULT 'pending', -- 'pending', 'done', 'cancelled'
            FOREIGN KEY (created_by) REFERENCES users (user_id)
        )
    """)

    conn.commit()
    conn.close()

def add_user(user_id, name, role):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO users (user_id, name, role, is_active, joined_at) VALUES (?, ?, ?, 1, datetime('now'))",
        (user_id, name, role)
    )
    conn.commit()
    conn.close()

def get_user_role(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
