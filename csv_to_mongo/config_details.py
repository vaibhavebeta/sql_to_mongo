import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch values
DB_NAME = os.getenv("DB_NAME")
DB_URL = os.getenv("DB_URL")

print(f"DB_NAME: {DB_NAME}")
print(f"DB_URL: {DB_URL}")
