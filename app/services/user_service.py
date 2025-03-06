from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from typing import List, Optional
from passlib.context import CryptContext
from app.config.database import database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self):
        self.container = database.get_container_client("users")

    def create_user(self, user: UserCreate) -> User:
        hashed_password = pwd_context.hash(user.password)
        new_user = User(
            id="1",  # Generar un ID único
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            roles=["user"]
        )
        self.container.create_item(new_user.dict(by_alias=True))
        return new_user

    def get_users(self) -> List[User]:
        query = "SELECT * FROM users"
        items = list(self.container.query_items(query, enable_cross_partition_query=True))
        for item in items:
            item["_id"] = item.get("id", item.get("_id"))  # Map 'id' to '_id' if 'id' exists
        return [User(**item) for item in items]

    def get_user(self, user_id: str) -> User:
        item = self.container.read_item(item=user_id, partition_key=user_id)
        item["_id"] = item.get("id", item.get("_id"))  # Map 'id' to '_id' if 'id' exists
        return User(**item)

    def update_user(self, user_id: str, user: UserUpdate) -> User:
        item = self.container.read_item(item=user_id, partition_key=user_id)
        updated_user = User(**{**item, **user.dict(exclude_unset=True)})
        self.container.replace_item(item=user_id, body=updated_user.dict(by_alias=True))
        return updated_user

    def delete_user(self, user_id: str) -> None:
        self.container.delete_item(item=user_id, partition_key=user_id)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        query = f"SELECT * FROM users u WHERE u.username = '{username}'"
        items = list(self.container.query_items(query, enable_cross_partition_query=True))
        if not items:
            return None
        user_data = items[0]
        user_data["_id"] = user_data["id"]  # Map 'id' to '_id'
        user = User(**user_data)
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        query = f"SELECT * FROM users u WHERE u.username = '{username}'"
        items = list(self.container.query_items(query, enable_cross_partition_query=True))
        if not items:
            return None
        user_data = items[0]
        user_data["_id"] = user_data.get("id", user_data.get("_id"))  # Map 'id' to '_id' if 'id' exists
        return User(**user_data)
