import sqlite3
import pandas as pd

def extract_database(db_path="database/students.db"):
    conn = sqlite3.connect(db_path)

    courses = pd.read_sql_query("SELECT * FROM courses", conn)
    enrollments = pd.read_sql_query("""
        SELECT student_id, course_id, semester, score
        FROM enrollments
    """, conn)

    conn.close()

    result = enrollments.merge(courses, on="course_id", how="left")
    return result
