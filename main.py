''' here we are loading the extract csv file from extract folder and then importing the function in our main file
Flow:
1. Extract Data
2. Validate Raw Data
3. Save Validation Reports
4. Transform Data
5. Validate Clean Data
6. Save Clean CSV
7. Load into MySQL
'''

from extract.extract_csv import get_csv_data
from extract.extract_api import get_api_data
from transform.transform_data import (validate_data, clean_data)
from transform.validate_product import validate_product
from transform.schema_mapping import map_api_schema
from transform.incremental_load import filter_new_records
from transform.watermark import (read_watermark,save_watermark,filter_watermark,get_latest_watermark
)
from load.load_mysql import load_to_mysql
from config.logger import logger 
from config.settings import (DATA_SOURCE, SEPARATOR as s)
import time



#This stores the current time in seconds.
start_time=time.time()  

total_records = 0
duplicate_count = 0
negative_count = 0
null_count = 0
clean_records = 0
etl_status = "FAILED"

source=DATA_SOURCE.lower() #creating constant name 
logger.info(s)
logger.info("ETL PIPELINE STARTED")
logger.info(s)

try:
#extract layer
    if source == "csv":
        logger.info("Data Source : CSV")
        df = get_csv_data()

    elif source== "api":
        logger.info("Data Source : REST API")
        df = get_api_data()
        df = map_api_schema(df)

    else:
        raise ValueError(
            f"Invalid DATA_SOURCE : {DATA_SOURCE}"
        )
        
    logger.info("Data Extracted Successfully")
    
    # Incremental Loading Strategy

    # Decide target table
    if source == "csv":
        table_name = "sales_report"

    elif source == "api":
        table_name = "product_master"
    
    if source == "csv":

        df = filter_new_records(
            df,
            table_name
        )

    elif source == "api":

        watermark = read_watermark(
            table_name
        )

        df = filter_watermark(
            df,
            watermark,
            "meta.updatedAt"
        )
        
        df=filter_new_records(
            df,
            table_name
        )

        if df.empty:
            logger.info("No New Records Found")
            etl_status = "SUCCESS"
            raise SystemExit

    total_records = len(df)
    logger.info(f"Total Records Read : {total_records}")
    
    #Validation Layer
    logger.info("Running Raw Data Validation")
    if source=="csv":
        errors=validate_data(df)
        
    elif source=="api":
        errors=validate_product(df)

    if errors:
        for error in errors:
            logger.warning(error)
    else:
        logger.info("Validation Passed Successfully")
        
        
    #using log report saved in csv file
    if source=="csv":
        logger.info("Saving Validation Reports For CSV File")
        # Negative quantity records
        negative_quantity_records = df[(df["quantity"] < 0)]
        
        negative_quantity_records.to_csv(
            "logs/negative_quantity_records.csv",
            index=False
        )
        
        # Duplicate records
        duplicate_records = df[df.duplicated()]

        duplicate_records.to_csv(
            "logs/duplicate_records.csv",
            index=False
        )

        # Null quantity records     
        null_quantity_records = df[(df["quantity"].isnull())]
        
        null_quantity_records.to_csv(
            "logs/null_quantity_records.csv",
            index=False
        )
        
        # created combined rejected records file
        negative_rejected=negative_quantity_records.copy()
        negative_rejected["rejection_reason"]="Negative Quantity"
        
        duplicate_rejected=duplicate_records.copy()
        duplicate_rejected["rejection_reason"]="Duplicate Record"
        
        null_rejected=null_quantity_records.copy()
        null_rejected["rejection_reason"]="Null Quantity"
        
        #combine all rejected records   
        rejected_records=pd.concat(
            [negative_rejected,duplicate_rejected,null_rejected],
            ignore_index=True
        )
        
        # Merge same rejected rows into one record and combine rejection reasons
        rejected_records=(
            rejected_records.groupby(
                ["order_id","product","quantity","price"],
                dropna=False,
                as_index=False
            )["rejection_reason"].apply(lambda x: ", ".join(sorted(set(x))))
        )   
        
        rejected_records.to_csv(
            "logs/rejected_records.csv",
            index=False
        )
                                        
        duplicate_count = len(duplicate_records)
        negative_count = len(negative_quantity_records)
        null_count = len(null_quantity_records)
        
        logger.info(f"Duplicate Records Saved : {duplicate_count}")
        
        logger.info(f"Negative Quantity Records : {negative_count}")

        logger.info(f"Null Quantity Records : {null_count}")
                    
        logger.info(f"Rejected Records Saved :{len(rejected_records)}")
        
    elif source=="api":
        logger.info(
        "Product Validation Reports Not Required"
    )
    
    #cleaning layer
    logger.info("Starting Data Cleaning")
    
    if source=="csv":
        df=clean_data(df)
        
    elif source=="api":
        #product cleaning will add here
        pass
    
    logger.info("Data Cleaning Completed")
    
    clean_records=len(df)
    logger.info(f"Records After Cleaning :{clean_records}")

    #post clean validation layer
    logger.info("Running Post Cleaning Validation")
    
    if source=="csv":
        errors=validate_data(df)
        
    elif source=="api":
        errors=validate_product(df)

    if errors:
        for error in errors:
            logger.warning(error)
            raise ValueError("Validation Failed")
    else:
        logger.info("Post Cleaning Validation Passed")
        
        
    #this is to keep the clean data records
    logger.info("Saving Clean CSV File")
    if source=="csv":
        output_file="data/clean_sales.csv"
    elif source=="api":
        output_file="data/clean_products.csv"
        
    df.to_csv(
        output_file, 
        index= False    
    )
    logger.info("Clean CSV Saved Successfully")

    #loading layer
    logger.info("Loading Data into MySQL")
    if source == "api":
        # Save watermark before removing timestamp column
        latest = get_latest_watermark(
        df,
        "meta.updatedAt"
        )
        
        df = df[
            [
                "order_id",
                "product",
                "category",
                "price",
                "stock"
            ]
        ]    

    #loading tha data int MySQL done here
    if len(df) > 0: 
        
        load_to_mysql(
            df=df,
            table_name=table_name
            )
    
        # Save latest watermark
        if source == "api":
            save_watermark(
                table_name,
                latest
            )
    else:
        logger.info("No New Record Found. Skipping Database load")
        
    etl_status= "SUCCESS"
    logger.info("ETL Pipeline Completed Successfully")


except FileNotFoundError:
    logger.error("CSV File not Found")
    raise

except PermissionError:
    logger.error("Permission denied while accessing the file")
    raise

except KeyError as e:
    logger.error(f"Missing Required Column: {e} ")
    raise

except Exception as e:
    logger.error(f"Unexpected error occured :{e}")
    raise

finally:
    end_time = time.time()
    execution_time = end_time - start_time

    logger.info("=" * 25 + " ETL SUMMARY " + "=" * 25)
    logger.info(f"Total Records Read        : {total_records}")
    logger.info(f"Duplicate Records         : {duplicate_count}")
    logger.info(f"Negative Quantity Records : {negative_count}")
    logger.info(f"Null Quantity Records     : {null_count}")
    logger.info(f"Records After Cleaning    : {clean_records}")
    logger.info(f"Execution Time            : {execution_time:.2f} seconds")
    logger.info(f"Status                    : {etl_status}")
    logger.info("=" * 63)

    logger.info(s)
    logger.info("ETL PIPELINE FINISHED")
    logger.info(s)