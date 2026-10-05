import pandas as pd


def validate_records(df):
    valid_rows = []
    rejected_rows = []

    for _, row in df.iterrows():
        errors = []

        # التحقق من student_id
        if pd.isna(row.get("student_id")):
            errors.append("Missing student_id")

        # التحقق من العمر
        age = row.get("age")

        if pd.notna(age) and not (16 <= float(age) <= 80):
            errors.append("Invalid Age")

        # التحقق من GPA
        gpa = row.get("gpa")

        if pd.notna(gpa) and not (0 <= float(gpa) <= 4):
            errors.append("Invalid GPA")

        # التحقق من الدرجة
        score = row.get("average_score")

        if pd.notna(score) and not (0 <= float(score) <= 100):
            errors.append("Invalid Score")

        # التحقق من الحضور
        attendance = row.get("attendance")

        if pd.notna(attendance) and not (0 <= float(attendance) <= 100):
            errors.append("Invalid Attendance")

        # تسجيل البيانات المرفوضة
        if errors:
            rejected_rows.append({
                "student_id": row.get("student_id"),
                "error_reason": "; ".join(errors)
            })
        else:
            valid_rows.append(row)

    return pd.DataFrame(valid_rows), pd.DataFrame(rejected_rows)