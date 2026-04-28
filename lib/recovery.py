from flask import Blueprint, render_template, request, redirect
from lib.connect_db import connect_db


recovery_bp = Blueprint("recovery", __name__)
edit_recovery_single_bp = Blueprint("edit_recovery_single", __name__)

# Edit recoverys individualy
@recovery_bp.route("/edit/recovery/<int:athlete_id>", methods=["GET"])
def edit_recovery_list(athlete_id):
    """
    Edit recovery logs
    """
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT recovery_id, sleep_hours, soreness_level, stress_level, recovery_score, log_date
        FROM recovery_logs
        WHERE athlete_id=%s
        ORDER BY log_date DESC
    """, (athlete_id,))

    logs = cur.fetchall()
    conn.close()

    return render_template("edit_recovery.html", logs=logs, athlete_id=athlete_id)

@edit_recovery_single_bp.route("/edit/recovery/single/<int:recovery_id>", methods=["GET", "POST"])
def edit_recovery_single(recovery_id):
    conn = connect_db()
    cur = conn.cursor()

    if request.method == "POST":
        cur.execute("""
            UPDATE recovery_logs
            SET sleep_hours=%s, soreness_level=%s, stress_level=%s, recovery_score=%s, log_date=%s
            WHERE recovery_id=%s
        """, (
            request.form["sleep_hours"],
            request.form["soreness_level"],
            request.form["stress_level"],
            request.form["recovery_score"],
            request.form["log_date"],
            recovery_id
        ))

        conn.commit()
        return redirect("/athletes")

    cur.execute("""
        SELECT * FROM recovery_logs WHERE recovery_id=%s
    """, (recovery_id,))

    log = cur.fetchone()
    conn.close()

    return render_template("edit_recovery_single.html", log=log)