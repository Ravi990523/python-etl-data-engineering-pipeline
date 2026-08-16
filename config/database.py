from sqlalchemy import create_engine
#Here we can import all the DB connection or simply * but import each varibale is better practice 
from config.settings import (DB_HOST,
                             DB_NAME,
                             DB_PASSWORD,
                             DB_PORT,
                             DB_USER
                             )

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine= create_engine(DATABASE_URL)
