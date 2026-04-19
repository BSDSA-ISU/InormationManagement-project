from flask import Flask, render_template, request, redirect, flash, url_for
import matplotlib.pyplot as plt
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

# Dotenv stuffs
db_server = os.getenv("DB_SERVER", "localhost")
db_user = os.getenv("DB_USER", 'root')
db_password = os.getenv("DB_PASSWORD", "")
db_databasename = os.getenv("DB_DATABASE", "athlete_dashboard")
db_port = int(os.getenv("DB_PORT", 6969))

app = Flask(__name__)
app.secret_key = "Koishi11"

def connect_db():
    return pymysql.connect(
        host=db_server,
        user=db_user,
        password=db_password,
        database=db_databasename,
        cursorclass=pymysql.cursors.Cursor,
        autocommit=False
    )

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

    plt.figure()
    plt.plot(dates, calories)
    plt.xticks(rotation=45)
    plt.title("Calories Over Time")
    plt.xlabel("Date")
    plt.ylabel("Calories")

    os.makedirs("static", exist_ok=True)
    path = f"static/calories_{athlete_id}.png"
    plt.savefig(path, bbox_inches='tight')
    plt.close()

    return path

# 🏠 Homepage → list athletes
@app.route("/", methods=["GET", "POST"])
def index():
    conn = connect_db()
    cur = conn.cursor()

    # ➕ CREATE new athlete
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        sex = request.form["sex"]
        weight = request.form["weight"]
        height = request.form["height"]

        cur.execute("""
            INSERT INTO athletes (name, age, sex, weight, height)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, age, sex, weight, height))

        conn.commit()
        return redirect("/")

    # 📥 READ athletes
    cur.execute("SELECT athlete_id, name FROM athletes")
    athletes = cur.fetchall()

    conn.close()
    return render_template("index.html", athletes=athletes)

@app.route("/athlete/<int:athlete_id>")
def athlete(athlete_id):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""SELECT name, age, weight, height
    FROM athletes WHERE athlete_id = %s
    """,
    (athlete_id,))
    
    athlete = cur.fetchone()

    cur.execute("""SELECT SUM(calories) FROM nutrition_logs
    WHERE athlete_id = %s""",
    (athlete_id,))
    
    total_calories = cur.fetchone()[0] or 0  # pyright: ignore[reportOptionalSubscript]

    cur.execute("""SELECT SUM(duration_minutes) FROM
    training_sessions WHERE athlete_id = %s""",
    (athlete_id,))
    
    total_training = cur.fetchone()[0] or 0  # pyright: ignore[reportOptionalSubscript]

    cur.execute("""SELECT AVG(recovery_score) FROM recovery_logs
    WHERE athlete_id = %s""",
    (athlete_id,))
    
    avg_recovery = cur.fetchone()[0] or 0  # pyright: ignore[reportOptionalSubscript]

    # 📊 charts
    calorie_chart = generate_calorie_chart(athlete_id)
    training_chart = generate_training_chart(athlete_id)
    recovery_chart = generate_recovery_chart(athlete_id)

    cur.execute("""
    SELECT goal_type, target_value, current_value, start_date, end_date
    FROM goals
    WHERE athlete_id = %s
    """, (athlete_id,))

    goals = cur.fetchall()

    conn.close()

    return render_template(
        "athlete.html",
        athlete=athlete,
        calories=total_calories,
        training=total_training,
        recovery=round(avg_recovery, 2),
        calorie_chart=calorie_chart,
        training_chart=training_chart,
        recovery_chart=recovery_chart,
        athlete_id=athlete_id,
        goals=goals
    )

@app.route("/edit/<int:athlete_id>", methods=["GET", "POST"])
def edit_athlete(athlete_id):
    conn = connect_db()
    cur = conn.cursor()

    # UPDATE + INSERT
    if request.method == "POST":
        try:

            # Update athlete info
            name = request.form["name"]
            age = request.form["age"]
            sex = request.form["sex"]
            weight = request.form["weight"]
            height = request.form["height"]

            cur.execute("""
                UPDATE athletes
                SET name=%s, age=%s, sex=%s, weight=%s, height=%s
                WHERE athlete_id=%s
            """, (name, age, sex, weight, height, athlete_id))


            # Insert training session
            session_types = request.form.getlist("session_type[]")
            durations = request.form.getlist("duration_minutes[]")
            intensities = request.form.getlist("intensity[]")
            calories = request.form.getlist("calories_burned[]")
            dates = request.form.getlist("session_date[]")

            for i in range(len(session_types)):
                if session_types[i].strip():  # ignore empty rows
                    cur.execute("""
                        INSERT INTO training_sessions
                        (athlete_id, session_type, duration_minutes, intensity, calories_burned, session_date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        athlete_id,
                        session_types[i],
                        durations[i],
                        intensities[i],
                        calories[i],
                        dates[i]
                    ))

            # Insert recovery log
            sleep_hours = request.form.getlist("sleep_hours[]")
            soreness = request.form.getlist("soreness_level[]")
            stress = request.form.getlist("stress_level[]")
            recovery = request.form.getlist("recovery_score[]")
            recovery_dates = request.form.getlist("recovery_log_date[]")

            for i in range(len(sleep_hours)):
                if sleep_hours[i].strip():
                    cur.execute("""
                        INSERT INTO recovery_logs
                        (athlete_id, sleep_hours, soreness_level, stress_level, recovery_score, log_date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        athlete_id,
                        sleep_hours[i],
                        soreness[i],
                        stress[i],
                        recovery[i],
                        recovery_dates[i] if recovery_dates[i] else None
                    ))

            # Nutrition logs
            meal_types = request.form.getlist("meal_type[]")
            calories = request.form.getlist("calories[]")
            protein = request.form.getlist("protein[]")
            carbs = request.form.getlist("carbs[]")
            fats = request.form.getlist("fats[]")
            nutrition_dates = request.form.getlist("nutrition_log_date[]")

            for i in range(len(meal_types)):
                if meal_types[i].strip():
                    cur.execute("""
                        INSERT INTO nutrition_logs
                        (athlete_id, meal_type, calories, protein, carbs, fats, log_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        athlete_id,
                        meal_types[i],
                        calories[i],
                        protein[i],
                        carbs[i],
                        fats[i],
                        nutrition_dates[i] if nutrition_dates[i] else None
                    ))

            # 🎯 Goals (MULTIPLE)
            goal_types = request.form.getlist("goal_type[]")
            target_values = request.form.getlist("target_value[]")
            current_values = request.form.getlist("current_value[]")
            start_dates = request.form.getlist("start_date[]")
            end_dates = request.form.getlist("end_date[]")

            for i in range(len(goal_types)):
                if goal_types[i].strip():
                    cur.execute("""
                        INSERT INTO goals
                        (athlete_id, goal_type, target_value, current_value, start_date, end_date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        athlete_id,
                        goal_types[i],
                        target_values[i],
                        current_values[i],
                        start_dates[i],
                        end_dates[i]
                    ))

            conn.commit()
            return redirect(f"/athlete/{athlete_id}")
        except Exception as e:
            conn.rollback()
            flash(f"❌ Error: {str(e)}", "error")
            return redirect(url_for("edit_athlete", athlete_id=athlete_id))

    # LOAD athlete data
    cur.execute("""
        SELECT name, age, sex, weight, height
        FROM athletes
        WHERE athlete_id=%s
    """, (athlete_id,))

    athlete = cur.fetchone()

    conn.close()

    return render_template("edit.html", athlete=athlete, athlete_id=athlete_id)

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

if __name__ == "__main__":
    app.run(debug=True, port=db_port, host="0.0.0.0")