import pandas as pd

def integrate_data(csv_data, api_data, database_data, mongo_data):
    result = csv_data.merge(api_data, on="student_id", how="left")

    # Aggregate SQLite records so one student remains one row.
    if not database_data.empty:
        db_summary = (
            database_data.groupby("student_id", as_index=False)
            .agg(
                average_score=("score", "mean"),
                courses_count=("course_id", "nunique")
            )
        )
        result = result.merge(db_summary, on="student_id", how="left")

    result = result.merge(mongo_data, on="student_id", how="left")

    return result
