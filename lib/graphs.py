import os
from matplotlib import pyplot as plt
from lib.connect_db import connect_db
from lib.clean_graphs import clean

# Initialize directory clean-up
clean()

def save_and_close(athlete_id, chart_type):
    """Helper function to handle sizing, formatting, and saving."""
    plt.xticks(rotation=90)  # Standing labels
    plt.tight_layout()       # Ensures labels fit within the image
    
    os.makedirs("static/graphs", exist_ok=True)
    path = f"static/graphs/{chart_type}_{athlete_id}.png"
    plt.savefig(path, bbox_inches='tight', dpi=100)
    plt.close()
    return path

# generates calories graph
def generate_calorie_chart(athlete_id):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT log_date, SUM(calories)
        FROM nutrition_logs
        WHERE athlete_id = %s
        GROUP BY log_date
        ORDER BY log_date
    """, (athlete_id,))

    data = cur.fetchall()
    conn.close()

    if not data:
        return None

    dates = [str(row[0]) for row in data]
    calories = [row[1] for row in data]

    # Width=12, Height=5 makes it a wide "web-style" banner
    plt.figure(figsize=(12, 5))
    plt.plot(dates, calories, color='orange', linewidth=2)
    plt.title("Daily Calorie Intake")
    plt.xlabel("Date")
    plt.ylabel("Calories")

    return save_and_close(athlete_id, "calories")

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

    plt.figure(figsize=(12, 5))
    plt.plot(dates, duration, marker='o', linestyle='-', color='blue')
    plt.title("Training Load Over Time")
    plt.xlabel("Date")
    plt.ylabel("Minutes")

    return save_and_close(athlete_id, "training")

# Generates Recovery Graphs
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

    plt.figure(figsize=(12, 5))
    plt.plot(dates, score, marker='o', linestyle='-', color='green')
    plt.title("Recovery Score Over Time")
    plt.xlabel("Date")
    plt.ylabel("Recovery Score")

    return save_and_close(athlete_id, "recovery")