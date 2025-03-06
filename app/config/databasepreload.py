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

# Crear la colección de usuarios
user_container = database.create_container_if_not_exists(
    id="users",
    partition_key=PartitionKey(path="/id"),
)

# Crear la colección de entrenamientos
training_container = database.create_container_if_not_exists(
    id="trainings",
    partition_key=PartitionKey(path="/id"),
)

# Crear la colección de disponibilidades
availability_container = database.create_container_if_not_exists(
    id="availabilities",
    partition_key=PartitionKey(path="/id"),
)

print("Colecciones creadas correctamente.")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Datos de prueba para la colección de usuarios
user_container = database.get_container_client("users")
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

# Datos de prueba para la colección de entrenamientos
training_container = database.get_container_client("trainings")
training_container.upsert_item({
    "id": "1",
    "trainer_id": "2",
    "user_id": "1",
    "start_time": "2023-10-01T10:00:00Z",
    "end_time": "2023-10-01T11:00:00Z",
    "status": "scheduled"
})

# Datos de prueba para la colección de disponibilidades
availability_container = database.get_container_client("availabilities")
availability_container.upsert_item({
    "id": "1",
    "trainer_id": "2",
    "center_id": "1",
    "available_times": ["2023-10-01T10:00:00Z", "2023-10-01T11:00:00Z"]
})

print("Datos de prueba agregados correctamente.")