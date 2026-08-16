
import pandas as pd

def get_csv_data():
    
    df= pd.read_csv("data/sales.csv")
    
    return df