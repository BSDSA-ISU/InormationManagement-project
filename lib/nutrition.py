from flask import Blueprint, render_template, request, redirect
from lib.connect_db import connect_db


nutrition_bp = Blueprint("nutrition", __name__)
edit_nutrition_single_bp = Blueprint("edit_nutrition_single", __name__)

# Edit nutritions individualy
@nutrition_bp.route("/edit/nutrition/<int:athlete_id>", methods=["GET"])
def edit_nutrition_list(athlete_id):
    """
    Edit nutrition list
    """
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT nutrition_id, meal_type, calories, protein, carbs, fats, log_date
        FROM nutrition_logs
        WHERE athlete_id=%s
        ORDER BY log_date DESC
    """, (athlete_id,))

    logs = cur.fetchall()
    conn.close()

    return render_template("edit_nutrition.html", logs=logs, athlete_id=athlete_id)

@edit_nutrition_single_bp.route("/edit/nutrition/single/<int:nutrition_id>", methods=["GET", "POST"])
def edit_nutrition_single(nutrition_id):
    conn = connect_db()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute("""
            UPDATE nutrition_logs
            SET meal_type=%s, calories=%s, protein=%s, carbs=%s, fats=%s, log_date=%s
            WHERE nutrition_id=%s
        """, (
            request.form["meal_type"],
            request.form["calories"],
            request.form["protein"],
            request.form["carbs"],
            request.form["fats"],
            request.form["log_date"],
            nutrition_id
        ))

        conn.commit()
        return redirect("/athletes")

    cur.execute("""
        SELECT * FROM nutrition_logs WHERE nutrition_id=%s
    """, (nutrition_id,))

    log = cur.fetchone()
    conn.close()

    return render_template("edit_nutrition_single.html", log=log)