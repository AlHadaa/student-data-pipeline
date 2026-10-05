import pandas as pd
from pymongo import MongoClient

def extract_mongo(
    uri="mongodb://localhost:27017/",
    database_name="student_pipeline",
    collection_name="student_extra"
):
    client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    client.admin.command("ping")

    collection = client[database_name][collection_name]
    rows = list(collection.find({}, {"_id": 0}))

    client.close()

    if not rows:
        raise ValueError("MongoDB collection is empty.")

    return pd.DataFrame(rows)
