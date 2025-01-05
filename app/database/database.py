import pyodbc
import os
from dotenv import load_dotenv

# Завантаження змінних середовища (якщо використовуєте .env)
load_dotenv()

# Параметри підключення
SERVER = os.getenv("DB_SERVER", "projectname.db.win.net")
DATABASE = os.getenv("DB_NAME", "dbname")
USERNAME = os.getenv("DB_USER", "username")
PASSWORD = os.getenv("DB_PASSWORD", "supersecretpassword")
DRIVER = "{ODBC Driver 18 for SQL Server}"

# Функція для підключення до бази даних

def get_db_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={DRIVER};SERVER={SERVER};PORT=1433;DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}"
        )
        print("Підключення до бази даних успішне!")
        return conn
    except pyodbc.Error as e:
        print(f"Помилка підключення до бази даних: {e}")
        return None
