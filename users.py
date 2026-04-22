import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

db_server = os.getenv("DB_SERVER", "localhost")
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "")
db_databasename = os.getenv("DB_DATABASE", "athlete_dashboard")

def connect_db():
    return pymysql.connect(
        host=db_server,
        user=db_user,
        password=db_password,
        database=db_databasename,
        cursorclass=pymysql.cursors.Cursor,
        autocommit=True
    )

def create_user():
    username = input("Username: ")
    password = input("Password: ")
    role = input("Role (admin/viewer): ").strip().lower()

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (username, password, role)
        VALUES (%s, %s, %s)
    """, (username, password, role))

    conn.close()
    print(" User created")

def list_users():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, username, role FROM users")
    users = cur.fetchall()

    for u in users:
        print(f"{u[0]} | {u[1]} | {u[2]}")

    conn.close()

def delete_user():
    user_id = input("User ID to delete: ")

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))

    conn.close()
    print("User deleted")

def menu():
    while True:
        print("\n--- USER MANAGER ---")
        print("1. Create user")
        print("2. List users")
        print("3. Delete user")
        print("4. Exit")

        choice = input("> ")

        if choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            delete_user()
        elif choice == "4":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    menu()