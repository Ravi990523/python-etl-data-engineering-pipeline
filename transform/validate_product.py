'''
validation rule:
1. Required Columns
2. Product Name cannot be NULL
3. Product Name cannot be Empty
4. Price >= 0
5. Stock >= 0
6. No Duplicate Product IDs
'''

import pandas as pd
from config.logger import logger
from config.settings import SEPARATOR as s

def validate_product(df):
    errors=[]
    
    logger.info(s)
    logger.info("PRODUCT VALIDATION STARTED")
    logger.info(s)
    
    #required column check
    
    required_columns=[
        "order_id",
        "product",
        "stock",
        "price",
        "category"
    ]
    missing_columns=[
        col for col in required_columns
        if col not in df.columns
    ]
    if missing_columns:
        errors.append(
            f"Missing Required Column   : {missing_columns}"
        )   
    if errors:
        logger.warning(errors[0])
        return errors
    
    #Product ID duplicate count
    duplicate_count=df["order_id"].duplicated().sum()
    
    if duplicate_count > 0 :
        errors.append(
            f"Duplicate Product IDs found   : {duplicate_count}"
        )
    
    #Product name validation
    df["product"]=(
        df["product"]
        .fillna("")
        .str.strip()
    )
    empty_products=df["product"] .eq("").sum()
    
    if empty_products > 0:
        errors.append(
            f"Empty Product Name Found  :{empty_products}"
        )
        
    #Price Validation 
    negative_price= (df["price"] < 0).sum()
    
    if negative_price >0:
        errors.append(
            f"Negative Price Found  :{negative_price}"
        )
        
    #Stock Validation
    negative_stock=(df["stock"] <0).sum()
    if negative_stock >0:
        errors.append(
            f"Negative Stock found  :{negative_stock}"
        )
    
    if errors:
        logger.warning("Product Validation Failed")
        
        for error in errors:
            logger.warning(error)
        else:
            logger.info("Product Validation Passed Successfully")
        logger.info("PRODUCT VALIDATION COMPLETED")
        
    return errors