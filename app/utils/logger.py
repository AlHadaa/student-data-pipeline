import logging
from pathlib import Path

def get_logger():
    Path("logs").mkdir(exist_ok=True)

    logger = logging.getLogger("student_pipeline")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler("logs/pipeline.log", encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
