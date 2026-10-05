import pandas as pd

def clean_students(df):
    df = df.copy()

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    if "student_name" in df.columns:
        df["student_name"] = (
            df["student_name"].astype("string").str.strip().str.title()
        )

    if "city" in df.columns:
        df["city"] = (
            df["city"].astype("string").str.strip().str.title()
        )

    df["student_id"] = pd.to_numeric(df["student_id"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    df = df.drop_duplicates(subset=["student_id"])

    return df
