from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()

@router.post("/", response_model=UserResponse, summary="Create a new user", description="Create a new user with the provided details.")
def create_user(user: UserCreate, current_user: str = Depends(get_current_user)):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user_service.create_user(user)

@router.get("/", response_model=List[UserResponse], summary="Get all users", description="Retrieve a list of all users.")
def get_users(current_user: str = Depends(get_current_user)):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user_service.get_users()

@router.get("/{user_id}", response_model=UserResponse, summary="Get a user by ID", description="Retrieve the details of a specific user by their ID.")
def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    if "admin" not in current_user.roles and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user_service.get_user(user_id)

@router.put("/{user_id}", response_model=UserResponse, summary="Update a user", description="Update the details of a specific user by their ID.")
def update_user(user_id: str, user: UserUpdate, current_user: str = Depends(get_current_user)):
    if "admin" not in current_user.roles and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user_service.update_user(user_id, user)

@router.delete("/{user_id}", summary="Delete a user", description="Delete a specific user by their ID.")
def delete_user(user_id: str, current_user: str = Depends(get_current_user)):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Not authorized")
    user_service.delete_user(user_id)
    return {"message": "User deleted"}
