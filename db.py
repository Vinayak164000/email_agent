import sqlite3
import bcrypt

DB_NAME = "users.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_user_table():
    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )''')
        conn.commit()

def register_user(username, name, password):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO users (username, name, password) VALUES (?, ?, ?)",
                         (username, name, hashed_pw))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False  # Username already exists

def login_user(username, password):
    with get_connection() as conn:
        cursor = conn.execute("SELECT name, password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            name, hashed_pw = result
            if bcrypt.checkpw(password.encode(), hashed_pw):
                return name
    return None
