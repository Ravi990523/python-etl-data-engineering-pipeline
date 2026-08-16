import json
from pathlib import Path
from config.logger import logger
from config.settings import SEPARATOR as s
import pandas as pd

#file path to store the timestamp
#metadata file
WATERMARK_FILE = Path("metadata/watermark.json")

#Read last processed watermark
def read_watermark( table_name):
    logger.info(s)
    logger.info("READING WATERMARK")
    logger.info(s)
    
    if not WATERMARK_FILE.exists():
        logger.info("Watermark File not Found")
        return None
    
    #read json
    with open(WATERMARK_FILE, "r") as file:
        data=json.load(file)
        
    watermark=data.get(table_name)
    
    logger.info(f"Current Watermark :{watermark}")
    return watermark       
    
# Save latest processed watermark
def save_watermark(table_name, watermark):
    logger.info(s)
    logger.info("SAVING WATERMARK")
    logger.info(s)
    
    if WATERMARK_FILE.exists():
        with open(WATERMARK_FILE,"r") as file:
            data=json.load(file)
    else:
        data={}
    # Update current table watermark
    data[table_name] = str(watermark)

    # Save JSON
    with open(WATERMARK_FILE, "w") as file:
        json.dump(data, file, indent=4)

    logger.info(f"Watermark Saved : {watermark}")


def filter_watermark(df, watermark, timestamp_column):
    """
    Keep only records newer than watermark
    """

    logger.info(s)
    logger.info("FILTERING USING WATERMARK")
    logger.info(s)

    # First run
    if watermark is None:
        logger.info("No Watermark Found")
        logger.info("Loading Complete Dataset")
        return df

    # Convert timestamp column
    df[timestamp_column] = pd.to_datetime(
    df[timestamp_column],
    errors="coerce"
)

    watermark = pd.to_datetime(watermark)

    new_df = df[
        df[timestamp_column] > watermark
    ]

    logger.info(f"New Records : {len(new_df)}")

    return new_df


def get_latest_watermark(df, timestamp_column):
    """
    Return latest timestamp from dataframe
    """

    df[timestamp_column] = pd.to_datetime(
    df[timestamp_column],
    errors="coerce"
    )

    latest = df[timestamp_column].max()

    logger.info(f"Latest Watermark : {latest}")

    return latest


