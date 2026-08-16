"""
Schema Mapping Module

This module standardizes data coming from different
sources into a common business schema.
"""

# API → Product Business Schema
from config.logger import logger
from config.settings import SEPARATOR as s


API_COLUMN_MAPPING = {
    "id":"order_id",
    "title":"product",
    "price":"price",
    "stock":"stock",
    "category":"category"
    }

def map_api_schema(df):
    logger.info(s)
    logger.info(f"Starting Schema mapping")
    logger.info(f"Renaming Columns using Business Schema Mapping")
    df=df.rename(columns=API_COLUMN_MAPPING)
    logger.info(f"Columns After Mapping :{list(df.columns)}")
    
    #check for required columns present or not.
    required_columns = [
        "order_id",
        "product",
        "stock",
        "price",
        "category"
    ]
 
    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing Required Columns : {missing}"
        )
    
    logger.info(f"Schema Mapping Completed")
    
    return df