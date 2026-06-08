import sqlite3

# DATABASE CONNECTION
conn = sqlite3.connect(
    "database/lie_detection.db",
    check_same_thread=False
)

cursor = conn.cursor()

# CREATE USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT
)
""")

# CREATE PREDICTIONS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    result TEXT,

    truth_score REAL,

    lie_score REAL,

    accuracy REAL,

    audio_path TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# REGISTER USER
def register_user(username, password):

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()

# LOGIN USER
def login_user(username, password):

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    return cursor.fetchone()

# SAVE PREDICTION
def save_prediction(
    username,
    result,
    truth_score,
    lie_score,
    accuracy,
    audio_path
):

    cursor.execute("""
    INSERT INTO predictions (

        username,
        result,
        truth_score,
        lie_score,
        accuracy,
        audio_path

    )

    VALUES (?, ?, ?, ?, ?, ?)
    """, (

        username,
        result,
        truth_score,
        lie_score,
        accuracy,
        audio_path
    ))

    conn.commit()

# GET USER HISTORY
def get_user_history(username):

    cursor.execute("""
    SELECT

        result,
        truth_score,
        lie_score,
        accuracy,
        created_at

    FROM predictions

    WHERE username=?

    ORDER BY id DESC
    """, (username,))

    return cursor.fetchall()