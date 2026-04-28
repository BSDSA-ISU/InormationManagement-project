from flask import Blueprint, render_template, request, redirect
from lib.connect_db import connect_db


goals_bp = Blueprint("goals", __name__)
edit_goals_single_bp = Blueprint("edit_goals_single", __name__)

# Edit goalss individualy
@goals_bp.route("/edit/goals/<int:athlete_id>", methods=["GET"])
def edit_goals_list(athlete_id):
    """
    Edit goals list
    """
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT goal_id, goal_type, target_value, current_value, start_date, end_date
        FROM goals
        WHERE athlete_id=%s
        ORDER BY start_date DESC
    """, (athlete_id,))

    logs = cur.fetchall()
    conn.close()

    return render_template("edit_goals.html", logs=logs, athlete_id=athlete_id)

@edit_goals_single_bp.route("/edit/goals/single/<int:goal_id>", methods=["GET", "POST"])
def edit_goals_single(goal_id):
    conn = connect_db()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute("""
            UPDATE goals
            SET goal_type=%s, target_value=%s, current_value=%s, start_date=%s, end_date=%s
            WHERE goal_id=%s
        """, (
            request.form["goal_type"],
            request.form["target_value"],
            request.form["current_value"],
            request.form["start_date"],
            request.form["end_date"],
            goal_id
        ))

        conn.commit()
        return redirect("/athletes")

    cur.execute("""
        SELECT * FROM goals WHERE goal_id=%s
    """, (goal_id,))

    log = cur.fetchone()
    conn.close()

    return render_template("edit_goals_single.html", log=log)