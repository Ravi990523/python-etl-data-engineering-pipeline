'''Customer validation module

'''
import re
import pandas as pd
from config.logger import logger
from config.settings import SEPARATOR as s


def validate_customer(df):
    errors=[]
    rejected_records=[]
    
    
    logger.info(s)
    logger.info("CUSTOMER VALIDATION STARTED")
    logger.info(s)
    
    #validation lgic for customer id
    if (df["customer_id"].isnull().sum()>0):
        errors.append("Customer ID contains null values")
    
    #validation logic for name
    df["name"]=(df["name"].fillna("").str.strip())
    if (df["name"].eq("").sum() >0):
        errors.append("Customer Name contain empty value")
    
    #validation logic for email    
    email_pattern=(
        r"^[A-Za-z][A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}$"
    )
    
    invalid_email_found=False
    for email in df["email"]:
        if not re.match(email_pattern, str(email)):
            invalid_email_found=True
            break
    if invalid_email_found:
        errors.append("Invalid Email Format Found")
            
            
    logger.info("Customer Valiation Completed") 
    
    return errors