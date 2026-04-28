from flask import Blueprint, render_template, request, redirect
from lib.connect_db import connect_db


training_bp = Blueprint("training", __name__)
edit_training_single_bp = Blueprint("edit_training_single", __name__)

# Edit trainings individualy
@training_bp.route("/edit/training/<int:athlete_id>", methods=["GET"])
def edit_training_list(athlete_id):
    """
    Edit training logs
    """
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT session_id, session_type, duration_minutes, intensity, calories_burned, session_date
        FROM training_sessions
        WHERE athlete_id=%s
        ORDER BY session_date DESC
    """, (athlete_id,))

    logs = cur.fetchall()
    conn.close()

    return render_template("edit_training.html", logs=logs, athlete_id=athlete_id)

@edit_training_single_bp.route("/edit/training/single/<int:session_id>", methods=["GET", "POST"])
def edit_training_single(session_id):
    conn = connect_db()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute("""
            UPDATE training_sessions
            SET session_type=%s, duration_minutes=%s, intensity=%s, calories_burned=%s, session_date=%s
            WHERE session_id=%s
        """, (
            request.form["session_type"],
            request.form["duration_minutes"],
            request.form["intensity"],
            request.form["calories_burned"],
            request.form["session_date"],
            session_id
        ))

        conn.commit()
        return redirect("/athletes")

    cur.execute("""
        SELECT * FROM training_sessions WHERE session_id=%s
    """, (session_id,))

    log = cur.fetchone()
    conn.close()

    return render_template("edit_training_single.html", log=log)