import sqlite3
from pathlib import Path

DB_PATH = "database/students.db"

def create_database():
    Path("database").mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    conn.executescript("""
    DROP TABLE IF EXISTS courses;
    DROP TABLE IF EXISTS enrollments;

    CREATE TABLE courses (
        course_id INTEGER PRIMARY KEY,
        course_name TEXT,
        credit_hours INTEGER
    );

    CREATE TABLE enrollments (
        student_id INTEGER,
        course_id INTEGER,
        semester TEXT,
        score REAL
    );
    """)

    courses = [
        (1, "Python", 3),
        (2, "Database", 3),
        (3, "Data Engineering", 3),
    ]

    enrollments = [
        (1, 1, "2026-1", 92),
        (1, 2, "2026-1", 88),
        (2, 1, "2026-1", 76),
        (2, 3, "2026-1", 81),
        (3, 1, "2026-1", 65),
        (3, 2, "2026-1", 72),
        (4, 3, "2026-1", 95),
        (5, 1, "2026-1", 58),
    ]

    conn.executemany(
        "INSERT INTO courses VALUES (?, ?, ?)", courses
    )
    conn.executemany(
        "INSERT INTO enrollments VALUES (?, ?, ?, ?)", enrollments
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("SQLite database created.")
