import sqlite3
import os
from datetime import datetime

# 🔥 Define base directory properly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔥 Data folder inside project
DATA_DIR = os.path.join(BASE_DIR, "AutoGovX_Data")

# 🔥 Final database path
DB_PATH = os.path.join(DATA_DIR, "database.db")


def init_db():
    # Create folder if not exists
    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            decision TEXT,
            risk_score INTEGER,
            email TEXT,
            file_path TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_submission(title, decision, risk_score, email, file_path):
    conn = sqlite3.connect(DB_PATH, timeout=20)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO submissions
        (title, decision, risk_score, email, file_path, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        decision,
        risk_score,
        email,
        file_path,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()