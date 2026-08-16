from config.database import engine
from config.logger import logger
from config.settings import (DB_NAME, LOAD_MODE, CHUNK_SIZE) 


def load_to_mysql(df,table_name):
    
    rows_to_load=len(df)
    
    try:
        logger.info("=" *50)
        logger.info("DATABASE LOAD STARTED")
        logger.info("=" *50)    
        
        logger.info(f"Database Name :{DB_NAME}")
        logger.info(f"Target Table  :{table_name}")
        logger.info(f"Load Mode     :{LOAD_MODE}")
        logger.info(f"Rows to Load  :{rows_to_load:,}")
        logger.info(f"Chunk Size    :{CHUNK_SIZE:,}")
        
        with engine.begin() as connection:
            df.to_sql(
                name=table_name,
                con=connection,
                if_exists=LOAD_MODE,
                index=False,
                chunksize=CHUNK_SIZE
            )
        logger.info(f"Rows Loaded Successfully  :{rows_to_load:,}")
        logger.info("=" *50)
        logger.info("DATABASE LOAD COMPLETED")
        logger.info("=" *50)

    except Exception as e:
        logger.error(f"Error while loading data into MySQL: {e}")
        raise







'''


old code fo sql connection
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:1234@localhost/retail_db"
)

try:
    conn = engine.connect()
    print("Database Connected Successfully")
    conn.close()

except Exception as e:
    print("Connection Failed")
    print(e)
    
    
from sqlalchemy import create_engine

def load_to_mysql(df):

    engine = create_engine(
        "mysql+pymysql://root:1234@localhost/retail_db"
    )

    df.to_sql(
        name="sales_report",
        con=engine,
        if_exists="append",
        index=False
    )

    print("Data Loaded Successfully")
    
'''