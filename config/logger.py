import logging
from pathlib import Path

# Create logs directory if it doesn't exist
BASE_DIR = Path(__file__).resolve().parent.parent
log_directory = BASE_DIR / "logs"
log_directory.mkdir(exist_ok=True)

# Log file
log_file = log_directory / "etl.log"

# Create logger
logger = logging.getLogger("etl_logger")
logger.setLevel(logging.INFO)

# Prevent duplicate log messages
logger.propagate = False

# Avoid adding handlers multiple times
if not logger.handlers:

    # File Handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Common format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)