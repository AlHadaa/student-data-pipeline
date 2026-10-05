from app.sources.csv_source import extract_csv
from app.sources.api_source import extract_api
from app.sources.database_source import extract_database
from app.sources.mongo_source import extract_mongo

from app.transformation.cleaner import clean_students
from app.transformation.integration import integrate_data
from app.transformation.transformer import transform_data

from app.validation.quality import validate_records
from app.output.csv_writer import save_csv
from app.utils.logger import get_logger

def run_pipeline():
    logger = get_logger()

    logger.info("CSV extraction started")
    csv_data = extract_csv()
    logger.info("CSV records: %s", len(csv_data))

    logger.info("API extraction started")
    api_data = extract_api()
    logger.info("API records: %s", len(api_data))

    logger.info("SQLite extraction started")
    database_data = extract_database()
    logger.info("SQLite records: %s", len(database_data))

    logger.info("MongoDB extraction started")
    mongo_data = extract_mongo()
    logger.info("MongoDB records: %s", len(mongo_data))

    logger.info("Cleaning started")
    csv_data = clean_students(csv_data)

    logger.info("Integration started")
    integrated = integrate_data(
        csv_data, api_data, database_data, mongo_data
    )

    logger.info("Transformation started")
    transformed = transform_data(integrated)

    logger.info("Final validation started")
    valid_data, rejected_data = validate_records(transformed)

    save_csv(
        valid_data,
        "data/processed/final_dataset.csv"
    )

    save_csv(
        rejected_data,
        "data/rejected/rejected_records.csv"
    )

    logger.info("Final dataset created: %s records", len(valid_data))
    logger.info("Rejected records: %s", len(rejected_data))

    print("Pipeline completed successfully.")
    print(f"Valid records: {len(valid_data)}")
    print(f"Rejected records: {len(rejected_data)}")
    print("Output: data/processed/final_dataset.csv")
    print("Rejected: data/rejected/rejected_records.csv")

if __name__ == "__main__":
    run_pipeline()
