import requests
import pandas as pd
from config.settings import (
    API_URL,
    API_TIMEOUT,
    API_TOKEN,
    API_LIMIT,
    MAX_RETRIES,
    RETRY_DELAY,
    SEPARATOR as s
    )
from config.logger import logger 
import time

def get_api_data():
    '''
    extract data from REST API
    return:
    pandas DataFrame
    
    '''
    
    try:
        logger.info(s)
        logger.info("API EXTRACTION STARTED")
        logger.info(s)
        logger.info(f"API URL       : {API_URL}")
        logger.info(f"Timeout       :{API_TIMEOUT} seconds")
        
        headers = {
        "Accept": "application/json"
            }

        if API_TOKEN:
            headers["Authorization"] = f"Bearer {API_TOKEN}"
        
        all_products=[]# store all products from every page
                
        #pagination variable    
        skip=0
        limit=API_LIMIT
        total=None
                
        #running loop until all records found
        logger.info("Starting Pagination...")
        logger.info(f"Initial Skip : {skip}")
        logger.info(f"Initial Limit : {limit}")
        logger.info(f"Initial Total : {total}")
        while   total is None or skip <total:
            logger.info(f"Pagination Loop -> Skip={skip}, Total={total}")
            params={
            "limit":limit,
                "skip":skip
                }
        # Retry API request on temporary failures
            for attempt in range(1, MAX_RETRIES +1):
                try:                
                    logger.info(f"API Request Attempt   :{attempt}")
                    logger.info("Sending API Request...")
                    response = requests.get(
                        API_URL,
                        headers=headers,
                        params=params,
                        timeout=API_TIMEOUT
                    )     
                    logger.info("API Response Received")
                    response.raise_for_status()
                    logger.info(f"HTTP Status Code : {response.status_code}")
                    logger.info("API Request Successful")
                    break 
                
                except requests.exceptions.HTTPError as e:
                    
                    status_code=e.response.status_code
                    
                    logger.warning(f"Attempt {attempt}/{MAX_RETRIES} Failed "
                                f"(HTTP {status_code}):{e}")
                    
                    #retry for temporary server errors
                    if( status_code in[500, 502,503,504] and attempt <MAX_RETRIES):
                        logger.info(
                            f"Retrying in {RETRY_DELAY} seconds..."
                            )
                        time.sleep(RETRY_DELAY)
                        
                    else:
                        logger.error(f"HTTP {status_code} is not Retryable")
                        raise
                
                except(requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError,
                        ) as e:
                    logger.warning(f"Attempt {attempt}/{MAX_RETRIES} failed   :{e}")
                    
                    if attempt < MAX_RETRIES:
                        logger.info(
                            f"Retrying in {RETRY_DELAY} seconds..."
                            )
                        time.sleep(RETRY_DELAY)
                        
                    else:
                        logger.error("Maximum Retry Attempt Reached.")
                    
                        raise
                    

        
            #convert json into pandas dataframe
            data= response.json()
            logger.info("JSON Parsed Successfully")
            #read total only once as we dont need to read total on every request
            if total is None:
                total= data["total"]
                logger.info(f"Total Record Available   :{total}")

            #store current pages
            products=data["products"]
            all_products.extend(products)
            
            logger.info(f"Record Fetched    :{len(products)} | "
                        f"Total Collected   :{len(all_products)}"
             )
            
            #move to next pagee
            skip +=limit
            logger.info(f"Next Skip Value : {skip}")
            
        df=pd.json_normalize(all_products) # we are using https://dummyjson.com/products api whihc has product access only
        logger.info(f"Columns : {list(df.columns)}")       
        logger.info("API Data Retrieved Successfully")
        logger.info(f"Records Received : {len(df)}")
        return df
    
    except requests.exceptions.Timeout:
        logger.error("API Request Timed Out")
        raise

    except requests.exceptions.ConnectionError:
        logger.error("Unable to Connect to the API Server")
        raise

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error Occurred : {e}")
        raise

    except requests.exceptions.RequestException as e:
        logger.error(f"API Request Failed : {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected Error : {e}")
        raise
        