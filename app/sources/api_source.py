import requests
import pandas as pd


API_URL = "https://dummyjson.com/users?limit=100"


def extract_api():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    data = response.json()

    rows = []

    for user in data.get("users", []):
        student_id = user.get("id")

        # Academic data for the pipeline
        gpa = round(2.5 + (student_id % 16) * 0.1, 2)
        attendance = 70 + (student_id * 3) % 31

        rows.append({
            "student_id": student_id,
            "gpa": gpa,
            "attendance": attendance,
            "status": "Active" if attendance >= 80 else "Inactive"
        })

    return pd.DataFrame(rows)