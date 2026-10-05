from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"

def seed():
    client = MongoClient(MONGO_URI)
    collection = client["student_pipeline"]["student_extra"]

    collection.delete_many({})

    collection.insert_many([
        {"student_id": 1, "scholarship_status": "Active", "projects_count": 3},
        {"student_id": 2, "scholarship_status": "Inactive", "projects_count": 1},
        {"student_id": 3, "scholarship_status": "Active", "projects_count": 2},
        {"student_id": 4, "scholarship_status": "Active", "projects_count": 4},
        {"student_id": 5, "scholarship_status": "Inactive", "projects_count": 0},
    ])

    client.close()
    print("MongoDB collection seeded.")

if __name__ == "__main__":
    seed()
