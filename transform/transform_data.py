import pandas as pd

# validation business logic for csv file
def validate_data(df):
    errors=[]
    
    #null check
    if df.isnull().sum().sum()>0 :
        errors.append("Null value found")
    
    #dulicate_check
    if df.duplicated().sum()>0:
        errors.append("duplicate records found ")
    
    #negative value
    if (df["quantity"]<0).any():
        errors.append("Negative quantity found")
        
        
    # Required columns
    required_columns = [
        "order_id",
        "product",
        "quantity",
        "price"
    ]

    for col in required_columns:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")

    return errors
    
        
            
def clean_data(df):
    
    df["quantity"]=df["quantity"].fillna(1)
    
    df=df.drop_duplicates()
    
    df=df[df["quantity"]>=0]
    
    df["total_amount"]=df["quantity"]* df["price"]
    return df 

    
    
    
    
    






'''
print("data:")
print(df)

print("\n shape:")
print(df.shape)

print("\n column:")
print(df.columns)

print("\n first 3 ")
print(df.head(3))

print("\n last 2")
print(df.tail(2))

print("\n null values")
print(df.isnull().sum())

print("\n Duplicates")
print(df.duplicated().sum())      
print("\nCheck negative values")


invalid_qty = df[df["quantity"] < 0]
if not invalid_qty.empty:
    print("Invalid quantity found\n")
else:
    print("No negative value found\n")
    
    
required_columns = [
    "order_id",
    "product",
    "quantity",
    "price",
]

missing_columns=[]
for cols in required_columns:
    if cols not in df.columns:
        missing_columns.append(cols)
        
if missing_columns:
    print("Missing Column:", missing_columns)
else:
    print("All columns presnt")


print("\nlength:", len(df))
'''