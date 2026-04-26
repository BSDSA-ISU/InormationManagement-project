import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

# Dotenv stuffs
db_server = os.getenv("DB_SERVER", "localhost")
db_user = os.getenv("DB_USER", 'root')
db_password = os.getenv("DB_PASSWORD", "")
db_databasename = os.getenv("DB_DATABASE", "athlete_dashboard")
db_port = int(os.getenv("DB_PORT", 6969))

def connect_db():
    """
    connects the database using pymysql
    """
    return pymysql.connect(
        host=db_server,
        user=db_user,
        password=db_password,
        database=db_databasename,
        cursorclass=pymysql.cursors.Cursor,
        autocommit=False
    )