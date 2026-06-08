import sqlite3

# CONNECT DATABASE
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

# CREATE PREDICTION TABLE
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