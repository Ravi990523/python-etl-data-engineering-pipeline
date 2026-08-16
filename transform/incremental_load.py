from sqlalchemy import text
from config.database import engine
from config.logger import logger
from config.settings import SEPARATOR as s
import pandas as pd

def get_existing_order_ids(table_name):
    logger.info(s)
    logger.info("READING FROM EXISTING DATA")
    logger.info(s)
    logger.info(f"Source Table      :{table_name}")
    
    query=text(f"""
        SELECT order_id
        from {table_name};
        """)
    
    with engine.connect() as connection:
        result =connection.execute(query)
        
        existing_ids= {
            row.order_id
            for row in result
        }
    logger.info(f"Existing Records  :{len(existing_ids)}")
    
    return existing_ids

def filter_new_records(df, table_name):
    logger.info(s)
    logger.info("INCREMENTAL LOADING STARTED")
    logger.info(s)
    
    existing_ids=get_existing_order_ids(table_name)
    
    new_df=df[
        ~df["order_id"].isin(existing_ids)
    ]
    
    logger.info(f"New Record Found          :{len(new_df)}")
    logger.info(f"Existing Records Skipped  :{len(df) - len(new_df)}")#subtracting original df to new df
    
    logger.info(s)
    logger.info("INCREMENTAL LOAD COMPLETED")
    logger.info(s)
    
    return new_df