import pandas as pd

def extract_csv(path="data/raw/students.csv"):
    return pd.read_csv(path)
