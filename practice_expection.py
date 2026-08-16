'''
keep all the log report and error reports in single file it helps to keep maintainacne
'''



import logging

from pathlib import Path

# Create logs directory if it doesn't exist
log_directory = Path("logs")
log_directory.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=log_directory / "etl_exception.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Create logger object
logger = logging.getLogger(__name__)

try:
    logger.info("="*50)
    logger.info("ETL Pipeline Started")
    
    number=10/2
    
    logger.info(f"Division Successfully:{number}")

except ZeroDivisionError:
    logger.error(f"Error: Cannnot divide by zero")
    
else:
    logger.info("No Exception Occured")
    
finally:
    logger.info("ETL Pipeline Finished")
    logger.info("="*50)