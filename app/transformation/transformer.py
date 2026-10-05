import pandas as pd

def transform_data(df):
    df = df.copy()

    # Simple missing-value rules.
    if "age" in df.columns:
        df["age"] = df["age"].fillna(df["age"].median())

    if "average_score" in df.columns:
        df["average_score"] = df["average_score"].fillna(0)

    if "courses_count" in df.columns:
        df["courses_count"] = df["courses_count"].fillna(0).astype(int)

    # Two derived columns required by the assignment.
    def performance(score):
        if pd.isna(score):
            return "At Risk"
        if score >= 90:
            return "Excellent"
        if score >= 80:
            return "Very Good"
        if score >= 70:
            return "Good"
        if score >= 60:
            return "Acceptable"
        return "At Risk"

    df["performance_level"] = df["average_score"].apply(performance)

    if "attendance" in df.columns:
        df["attendance_status"] = df["attendance"].apply(
            lambda x: "Good" if pd.notna(x) and x >= 75 else "Low"
        )

    return df
