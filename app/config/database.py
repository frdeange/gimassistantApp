import os
from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Get the environment variables
COSMOS_DB_ENDPOINT = os.getenv("COSMOS_DB_ENDPOINT")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY")
COSMOS_DB_DATABASE = os.getenv("COSMOS_DB_DATABASE")
COSMOS_CONTAINER_USERS = os.getenv("COSMOS_CONTAINERS_USERS")
COSMOS_CONTAINER_TRAININGS = os.getenv("COSMOS_CONTAINERS_TRAININGS")
COSMOS_CONTAINER_AVAILABILITIES = os.getenv("COSMOS_CONTAINERS_AVAILABILITIES")
COSMOS_CONTAINER_NOTIFICATIONS = os.getenv("COSMOS_CONTAINERS_NOTIFICATIONS")

# Create a DefaultAzureCredential object
credential = DefaultAzureCredential()

# Validate that the required environment variables are set
if not COSMOS_DB_ENDPOINT or not COSMOS_DB_DATABASE:
    raise ValueError("Please set the COSMOS_DB_ENDPOINT and COSMOS_DB_DATABASE environment variables.")

# First, try authentication using the key
try:
    client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
    database = client.get_database_client(COSMOS_DB_DATABASE)
except Exception as e:
    print("Key-based authentication failed, trying with DefaultAzureCredential:", e)
    try:
        # If key-based authentication fails, try using DefaultAzureCredential
        client = CosmosClient(COSMOS_DB_ENDPOINT, credential=credential)
        database = client.get_database_client(COSMOS_DB_DATABASE)
    except Exception as e:
        raise ConnectionError(f"Failed to connect to CosmosDB using DefaultAzureCredential: {e}")

# Ensure the notifications container exists
notifications_container_name = COSMOS_CONTAINER_NOTIFICATIONS
if notifications_container_name:
    try:
        database.create_container_if_not_exists(id=notifications_container_name, partition_key=PartitionKey(path="/user_id"))
    except Exception as e:
        raise ConnectionError(f"Failed to create or access the container: {e}")
else:
    raise ValueError("COSMOS_CONTAINER_NOTIFICATIONS environment variable is not set")

# Ensure the users container exists
user_container_name = COSMOS_CONTAINER_USERS
if user_container_name:
    try:
        database.create_container_if_not_exists(id=user_container_name, partition_key=PartitionKey(path="/id"))
    except Exception as e:
        raise ConnectionError(f"Failed to create or access the container: {e}")
else:
    raise ValueError("COSMOS_CONTAINER_USERS environment variable is not set")

# Ensure the trainings container exists
training_container_name = COSMOS_CONTAINER_TRAININGS
if training_container_name:
    try:
        database.create_container_if_not_exists(id=training_container_name, partition_key=PartitionKey(path="/id"))
    except Exception as e:
        raise ConnectionError(f"Failed to create or access the container: {e}")
else:
    raise ValueError("COSMOS_CONTAINER_TRAININGS environment variable is not set")

# Ensure the availabilities container exists
availability_container_name = COSMOS_CONTAINER_AVAILABILITIES
if availability_container_name:
    try:
        database.create_container_if_not_exists(id=availability_container_name, partition_key=PartitionKey(path="/id"))
    except Exception as e:
        raise ConnectionError(f"Failed to create or access the container: {e}")
else:
    raise ValueError("COSMOS_CONTAINER_AVAILABILITIES environment variable is not set")
