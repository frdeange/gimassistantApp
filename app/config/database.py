import os
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

load_dotenv()

COSMOS_DB_ENDPOINT = os.getenv("COSMOS_DB_ENDPOINT")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY")
COSMOS_DB_DATABASE = os.getenv("COSMOS_DB_DATABASE")

if not COSMOS_DB_ENDPOINT or not COSMOS_DB_KEY or not COSMOS_DB_DATABASE:
    raise ValueError("Please set COSMOS_DB_ENDPOINT, COSMOS_DB_KEY, and COSMOS_DB_DATABASE environment variables.")

try:
    client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
    database = client.get_database_client(COSMOS_DB_DATABASE) 
except Exception as e:
    raise ConnectionError(f"Failed to connect to CosmosDB: {e}")
