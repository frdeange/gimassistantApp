import os
from azure.cosmos import CosmosClient, PartitionKey
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

# Ensure the notifications container exists
container_name = "notifications"
try:
    database.create_container_if_not_exists(id=container_name, partition_key=PartitionKey(path="/user_id"))
except Exception as e:
    raise ConnectionError(f"Failed to create or access the container: {e}")

# Ensure the users container exists
user_container_name = "users"
try:
    database.create_container_if_not_exists(id=user_container_name, partition_key=PartitionKey(path="/id"))
except Exception as e:
    raise ConnectionError(f"Failed to create or access the container: {e}")

# Ensure the trainings container exists
training_container_name = "trainings"
try:
    database.create_container_if_not_exists(id=training_container_name, partition_key=PartitionKey(path="/id"))
except Exception as e:
    raise ConnectionError(f"Failed to create or access the container: {e}")

# Ensure the availabilities container exists
availability_container_name = "availabilities"
try:
    database.create_container_if_not_exists(id=availability_container_name, partition_key=PartitionKey(path="/id"))
except Exception as e:
    raise ConnectionError(f"Failed to create or access the container: {e}")
