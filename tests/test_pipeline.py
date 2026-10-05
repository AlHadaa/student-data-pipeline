import pandas as pd
from app.transformation.transformer import transform_data
from app.validation.quality import validate_records

def test_derived_columns():
    df = pd.DataFrame({
        "student_id": [1],
        "age": [21],
        "average_score": [92],
        "attendance": [90]
    })
    result = transform_data(df)
    assert "performance_level" in result.columns
    assert "attendance_status" in result.columns

def test_invalid_record_is_rejected():
    df = pd.DataFrame({
        "student_id": [1, 2],
        "age": [21, 15],
        "average_score": [90, 80],
        "attendance": [90, 90]
    })
    valid, rejected = validate_records(df)
    assert len(valid) == 1
    assert len(rejected) == 1
