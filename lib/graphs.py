import os
from matplotlib import pyplot as plt
from lib.connect_db import connect_db

# Generate training chart
def generate_training_chart(athlete_id):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT session_date, SUM(duration_minutes)
        FROM training_sessions
        WHERE athlete_id = %s
        GROUP BY session_date
        ORDER BY session_date
    """, (athlete_id,))

    data = cur.fetchall()
    conn.close()

    if not data:
        return None

    dates = [str(r[0]) for r in data]
    duration = [r[1] for r in data]

    plt.figure()
    plt.plot(dates, duration, marker='o')
    plt.title("Training Load Over Time")
    plt.xlabel("Date")
    plt.ylabel("Minutes")

    os.makedirs("static", exist_ok=True)
    path = f"static/training_{athlete_id}.png"
    plt.savefig(path, bbox_inches='tight')
    plt.close()

    return path

# Generates Recovery Graphs using matplotlib
def generate_recovery_chart(athlete_id):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT log_date, AVG(recovery_score)
        FROM recovery_logs
        WHERE athlete_id = %s
        GROUP BY log_date
        ORDER BY log_date
    """, (athlete_id,))

    data = cur.fetchall()
    conn.close()

    if not data:
        return None

    dates = [str(r[0]) for r in data]
    score = [r[1] for r in data]

    plt.figure()
    plt.plot(dates, score, marker='o')
    plt.title("Recovery Score Over Time")
    plt.xlabel("Date")
    plt.ylabel("Recovery Score")

    os.makedirs("static", exist_ok=True)
    path = f"static/recovery_{athlete_id}.png"
    plt.savefig(path, bbox_inches='tight')
    plt.close()

    return path