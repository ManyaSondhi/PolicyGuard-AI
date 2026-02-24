from database import DB_PATH
import sqlite3


def get_dashboard_stats():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # TOTAL
    cursor.execute("SELECT COUNT(*) FROM submissions")
    total = cursor.fetchone()[0]

    # ACCEPT
    cursor.execute("SELECT COUNT(*) FROM submissions WHERE decision='ACCEPT'")
    accepted = cursor.fetchone()[0]

    # REJECT
    cursor.execute("SELECT COUNT(*) FROM submissions WHERE decision='REJECT'")
    rejected = cursor.fetchone()[0]

    # MINOR
    cursor.execute("SELECT COUNT(*) FROM submissions WHERE decision='MINOR REVISION'")
    minor = cursor.fetchone()[0]

    # MAJOR
    cursor.execute("SELECT COUNT(*) FROM submissions WHERE decision='MAJOR REVISION'")
    major = cursor.fetchone()[0]

    # AVERAGE RISK
    cursor.execute("SELECT AVG(risk_score) FROM submissions")
    avg_risk = cursor.fetchone()[0]
    avg_risk = round(avg_risk, 2) if avg_risk else 0

    # RECENT 5
    cursor.execute("""
        SELECT title, decision, risk_score, email, timestamp
        FROM submissions
        ORDER BY id DESC
        LIMIT 5
    """)
    recent = cursor.fetchall()

    conn.close()

    return {
        "total": total,
        "accepted": accepted,
        "rejected": rejected,
        "minor": minor,
        "major": major,
        "avg_risk": avg_risk,
        "recent": recent
    }