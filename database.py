import sqlite3
import os
from datetime import datetime

DB_PATH = "C:/AutoGovX_Data/database.db"


def init_db():
    os.makedirs("C:/AutoGovX_Data", exist_ok=True)

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