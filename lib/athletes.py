from lib.connect_db import connect_db
from flask import Blueprint, Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

athlete_list_bp = Blueprint("athlete_list", __name__)
add_athlete_bp = Blueprint("add_athlete", __name__)
delete_athlete_bp = Blueprint("delete_athlete", __name__)
edit_athlete_bp = Blueprint("edit_athlete", __name__)

# get all athletes from db
def get_all_athletes():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT athlete_id, name FROM athletes")
    athletes = cur.fetchall()

    conn.close()
    return athletes

# Athlete webpge
@athlete_list_bp.route("/athletes")
def athlete_list():
    search = request.args.get("search", "")

    conn = connect_db()
    cur = conn.cursor()

    if search:
        cur.execute("""
            SELECT athlete_id, name
            FROM athletes
            WHERE name LIKE %s
        """, (f"%{search}%",))
    else:
        cur.execute("""
            SELECT athlete_id, name
            FROM athletes
        """)

    athletes = cur.fetchall()
    conn.close()

    return render_template("athlete_list.html", athletes=athletes, search=search)

# Add athlete
@add_athlete_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_athlete():
    if not current_user.is_admin():
        flash("🚫 Admins only! Please login as admin first", "error")
        return redirect(url_for('login', error='admins_only'))
    
    conn = connect_db()
    cur = conn.cursor()

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
        conn.close()

        flash("✅ Athlete added!", "success")
        return redirect("/athletes")

    conn.close()
    return render_template("add_athlete.html")

# EDit athletes
@edit_athlete_bp.route("/edit/<int:athlete_id>", methods=["GET", "POST"])
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
                if (
                    meal_types[i].strip() and
                    calories[i].strip() and
                    protein[i].strip() and
                    carbs[i].strip() and
                    fats[i].strip()
                ):
                    cur.execute("""
                        INSERT INTO nutrition_logs
                        (athlete_id, meal_type, calories, protein, carbs, fats, log_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        athlete_id,
                        meal_types[i],
                        int(calories[i]),
                        float(protein[i]),
                        float(carbs[i]),
                        float(fats[i]),
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


# delete entry
@delete_athlete_bp.route("/delete/<int:athlete_id>", methods=["POST"])
@login_required
def delete_athlete(athlete_id):
    
    # returns error if not an admin
    if not current_user.is_admin():
        flash("🚫 Admins only!", "error")
        return redirect(url_for('login', error='admins_only'))

    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM athletes WHERE athlete_id=%s", (athlete_id,))
        conn.commit()
        flash("Athlete deleted 🗑", "success")

    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "error")

    finally:
        conn.close()

    return redirect("/athletes")
