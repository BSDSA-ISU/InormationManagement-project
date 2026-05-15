import os
from matplotlib import pyplot as plt
from lib.connect_db import connect_db
import hashlib
import json

CHART_CONFIG = {
    "text_color": "#ffffff",
    "grid_color": "#444444",
    "axis_color": "#888888",
    "calories_line": "orange",
    "training_line": "blue",
    "recovery_line": "green",
    
    # --- FONT SIZE SETTERS ---
    "title_size": 20,
    "label_size": 15,
    "tick_size": 13
}

def get_data_hash(data):
    data_string = json.dumps(data, sort_keys=True, default=str)
    return hashlib.md5(data_string.encode('utf-8')).hexdigest()

def apply_theme(ax):
    """Applies transparency, colors, and font sizes to the plot axes."""
    ax.patch.set_alpha(0.0) 
    
    # Apply sizes and colors to Title and Labels
    ax.title.set_size(CHART_CONFIG["title_size"])
    ax.title.set_color(CHART_CONFIG["text_color"])
    
    ax.xaxis.label.set_size(CHART_CONFIG["label_size"])
    ax.xaxis.label.set_color(CHART_CONFIG["text_color"])
    
    ax.yaxis.label.set_size(CHART_CONFIG["label_size"])
    ax.yaxis.label.set_color(CHART_CONFIG["text_color"])
    
    # Apply sizes to the numbers on the axes (Ticks)
    ax.tick_params(axis='both', which='major', 
                   labelsize=CHART_CONFIG["tick_size"], 
                   colors=CHART_CONFIG["text_color"])
    
    # Set colors for the spines (The chart border)
    for spine in ax.spines.values():
        spine.set_edgecolor(CHART_CONFIG["axis_color"])


def save_and_close(athlete_id, chart_type, data_hash):
    os.makedirs("static/graphs", exist_ok=True)
    path = f"static/graphs/{chart_type}_{athlete_id}.svg"
    hash_path = f"static/graphs/{chart_type}_{athlete_id}.hash"
    
    plt.xticks(rotation=90)
    plt.tight_layout()
    
    # IMPORTANT: transparent=True makes the figure background clear
    plt.savefig(path, bbox_inches='tight', dpi=100, transparent=True)
    plt.close()
    
    with open(hash_path, "w") as f:
        f.write(data_hash)
    return path

def is_cache_valid(athlete_id, chart_type, current_hash):
    path = f"static/graphs/{chart_type}_{athlete_id}.svg"
    hash_path = f"static/graphs/{chart_type}_{athlete_id}.hash"
    if os.path.exists(path) and os.path.exists(hash_path):
        with open(hash_path, "r") as f:
            return f.read().strip() == current_hash
    return False

# Example of updated generation function
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

    # 1. Generate hash of the data
    current_hash = get_data_hash(data)
    path = f"static/graphs/calories_{athlete_id}.svg"

    # 2. Check if we can skip rendering
    if is_cache_valid(athlete_id, "calories", current_hash):
        return path

    dates = [str(row[0]) for row in data]
    calories = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15, 5))
    fig.patch.set_alpha(0.0) 

    dates = [str(row[0]) for row in data]
    calories = [row[1] for row in data]

    ax.plot(dates, calories, color=CHART_CONFIG["calories_line"], linewidth=2)
    ax.set_title("Daily Calorie Intake")
    ax.set_xlabel("Date")
    ax.set_ylabel("Calories")
    
    apply_theme(ax)

    return save_and_close(athlete_id, "calories", current_hash)

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
    
    current_hash = get_data_hash(data)
    path = f"static/graphs/training_{athlete_id}.svg"

    if is_cache_valid(athlete_id, "training", current_hash):
        return path

    dates = [str(row[0]) for row in data]
    calories = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(15, 5))
    fig.patch.set_alpha(0.0) 

    dates = [str(row[0]) for row in data]
    minutes = [row[1] for row in data]

    ax.plot(dates, minutes, color=CHART_CONFIG["training_line"], linewidth=2)
    ax.set_title("Training Load Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Minutes")
    
    apply_theme(ax)

    return save_and_close(athlete_id, "training", current_hash)


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
    
    current_hash = get_data_hash(data)
    path = f"static/graphs/recovery_{athlete_id}.svg"

    if is_cache_valid(athlete_id, "recovery", current_hash):
        return path

    fig, ax = plt.subplots(figsize=(15, 5))
    fig.patch.set_alpha(0.0) 

    dates = [str(row[0]) for row in data]
    score = [row[1] for row in data]

    ax.plot(dates, score, color=CHART_CONFIG["recovery_line"], linewidth=2)
    ax.set_title("Recovery analysis")
    ax.set_xlabel("Date")
    ax.set_ylabel("Calories")
    
    apply_theme(ax)

    """
    plt.figure(figsize=(8, 5))
    plt.plot(dates, score, marker='o', linestyle='-', color='green')
    plt.title("Recovery Score Over Time")
    plt.xlabel("Date")
    plt.ylabel("Recovery Score")
    """

    return save_and_close(athlete_id, "recovery", current_hash)
