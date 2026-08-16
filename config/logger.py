import logging
from pathlib import Path

# Create logs directory if it doesn't exist
log_directory = Path("logs")
log_directory.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=log_directory / "etl.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Create logger object
logger = logging.getLogger(__name__)
