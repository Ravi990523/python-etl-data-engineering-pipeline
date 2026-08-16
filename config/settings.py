import os 
from dotenv  import load_dotenv
from pathlib import Path

# Get project root folder
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

print(f"Loading .env from: {ENV_PATH}")

# Load .env file
load_dotenv(BASE_DIR / ".env")

# Database Configuration
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
API_URL=os.getenv("API_URL")
API_TIMEOUT=int(os.getenv("API_TIMEOUT"))
API_TOKEN=os.getenv("API_TOKEN")

# for the load_to_mysql 
LOAD_MODE= "append"
CHUNK_SIZE=2

#-------CHANGE HERE THE DATA SOURCE------
DATA_SOURCE="api"

#creating seperator to use everywhere
SEPARATOR=("="*60)

#API retry configuratuion settings
MAX_RETRIES=3
RETRY_DELAY=5

#API pagination
API_LIMIT=30