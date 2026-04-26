from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import pymysql
from dotenv import load_dotenv
from lib.nutrition import nutrition_bp
from lib.athletes import athlete_list_bp, add_athlete_bp, delete_athlete_bp, edit_athlete_bp
from lib.graphs import generate_recovery_chart, generate_training_chart

load_dotenv()

# Dotenv stuffs
db_server = os.getenv("DB_SERVER", "localhost")
db_user = os.getenv("DB_USER", 'root')
db_password = os.getenv("DB_PASSWORD", "")
db_databasename = os.getenv("DB_DATABASE", "athlete_dashboard")
db_port = int(os.getenv("DB_PORT", 6969))

# adds error handling using secrert key
app = Flask(__name__)
app.secret_key = "Koishi11"

# Register components
app.register_blueprint(nutrition_bp)
app.register_blueprint(athlete_list_bp)
app.register_blueprint(add_athlete_bp)
app.register_blueprint(delete_athlete_bp)
app.register_blueprint(edit_athlete_bp)

# for login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # pyright: ignore[reportAttributeAccessIssue]


def connect_db():
    return pymysql.connect(
        host=db_server,
        user=db_user,
        password=db_password,
        database=db_databasename,
        cursorclass=pymysql.cursors.Cursor,
        autocommit=False
    )

# User class
class User(UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def is_admin(self):
        return self.role == "admin"


# User loader
@login_manager.user_loader
def load_user(user_id):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, username, password, role FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()

    conn.close()

    if user:
        return User(user[0], user[1], user[2], user[3])
    return None

# login page landing
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("SELECT id, username, password, role FROM users WHERE username=%s", (username,))
        user = cur.fetchone()

        conn.close()

        if user and user[2] == password:
            login_user(User(user[0], user[1], user[2], user[3]))
            return redirect("/")
        else:
            flash("Invalid login", "error")

    return render_template("login.html")

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

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

# Landing pege
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/athlete/<int:athlete_id>")
def athlete(athlete_id):
    conn = connect_db()
    cur = conn.cursor()

    # Fetch all Lists
    cur.execute("SELECT * FROM nutrition_logs WHERE athlete_id=%s ORDER BY log_date DESC", (athlete_id,))
    nutrition_logs = cur.fetchall()

    cur.execute("SELECT * FROM training_sessions WHERE athlete_id=%s ORDER BY session_date DESC", (athlete_id,))
    training_sessions = cur.fetchall()

    cur.execute("SELECT * FROM recovery_logs WHERE athlete_id=%s ORDER BY log_date DESC", (athlete_id,))
    recovery_logs = cur.fetchall()

    cur.execute("SELECT * FROM goals WHERE athlete_id=%s", (athlete_id,))
    goals = cur.fetchall()


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
        nutrition_logs=nutrition_logs,
        training_sessions=training_sessions,
        recovery_logs=recovery_logs,
        goals=goals,
        calories=total_calories,
        training=total_training,
        recovery=round(avg_recovery, 2),
        calorie_chart=calorie_chart,
        training_chart=training_chart,
        recovery_chart=recovery_chart,
        athlete_id=athlete_id,
    )

if __name__ == "__main__":
    app.run(debug=True, port=db_port, host="0.0.0.0")