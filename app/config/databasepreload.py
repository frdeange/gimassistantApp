from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv
import os
from passlib.context import CryptContext

load_dotenv()

COSMOS_DB_ENDPOINT = os.getenv("COSMOS_DB_ENDPOINT")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY")
COSMOS_DB_DATABASE = os.getenv("COSMOS_DB_DATABASE")

client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
database = client.create_database_if_not_exists(id=COSMOS_DB_DATABASE)

# Ensure the containers from environment variables exist
containers = {
    "users": os.getenv("COSMOS_CONTAINERS_USERS"),
    "trainings": os.getenv("COSMOS_CONTAINERS_TRAININGS"),
    "availabilities": os.getenv("COSMOS_CONTAINERS_AVAILABILITIES"),
    "notifications": os.getenv("COSMOS_CONTAINERS_NOTIFICATIONS")
}

for container_name, partition_key in containers.items():
    if container_name and partition_key:
        try:
            database.create_container_if_not_exists(id=container_name, partition_key=PartitionKey(path=f"/{partition_key}"))
        except Exception as e:
            raise ConnectionError(f"Failed to create or access the container {container_name}: {e}")

print("Containers created successfully.")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Add test data for users
user_container = database.get_container_client(containers["users"])
user_container.upsert_item({
    "id": "1",
    "username": "user1",
    "email": "user1@example.com",
    "hashed_password": pwd_context.hash("password1"),
    "roles": ["user"]
})
user_container.upsert_item({
    "id": "2",
    "username": "trainer1",
    "email": "trainer1@example.com",
    "hashed_password": pwd_context.hash("password2"),
    "roles": ["trainer"]
})
user_container.upsert_item({
    "id": "3",
    "username": "admin1",
    "email": "admin1@example.com",
    "hashed_password": pwd_context.hash("password3"),
    "roles": ["admin"]
})

# Add test data for trainings
training_container = database.get_container_client(containers["trainings"])
training_container.upsert_item({
    "id": "1",
    "trainer_id": "2",
    "user_id": "1",
    "start_time": "2023-10-01T10:00:00Z",
    "end_time": "2023-10-01T11:00:00Z",
    "status": "scheduled"
})

# Add test data for availabilities
availability_container = database.get_container_client(containers["availabilities"])
availability_container.upsert_item({
    "id": "1",
    "trainer_id": "2",
    "center_id": "1",
    "available_times": ["2023-10-01T10:00:00Z", "2023-10-01T11:00:00Z"]
})

print("Test data added successfully.")