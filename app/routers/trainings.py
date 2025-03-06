from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.training import TrainingCreate, TrainingUpdate, TrainingResponse, AvailabilityCreate, AvailabilityUpdate, AvailabilityResponse
from app.services.training_service import TrainingService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/trainings", tags=["trainings"])
training_service = TrainingService()

@router.post("/", response_model=TrainingResponse, summary="Create a new training session", description="Create a new training session with the provided details.")
def create_training(training: TrainingCreate, current_user: str = Depends(get_current_user)):
    if "trainer" not in current_user.roles and "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Not authorized")
    return training_service.create_training(training)

@router.get("/", response_model=List[TrainingResponse], summary="Get all training sessions", description="Retrieve a list of all training sessions.")
def get_trainings(current_user: str = Depends(get_current_user)):
    return training_service.get_trainings()

@router.get("/{training_id}", response_model=TrainingResponse, summary="Get a training session by ID", description="Retrieve the details of a specific training session by its ID.")
def get_training(training_id: str, current_user: str = Depends(get_current_user)):
    return training_service.get_training(training_id)

@router.put("/{training_id}", response_model=TrainingResponse, summary="Update a training session", description="Update the details of a specific training session by its ID.")
def update_training(training_id: str, training: TrainingUpdate, current_user: str = Depends(get_current_user)):
    if "trainer" not in current_user.roles and "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Not authorized")
    return training_service.update_training(training_id, training)

@router.delete("/{training_id}", summary="Delete a training session", description="Delete a specific training session by its ID.")
def delete_training(training_id: str, current_user: str = Depends(get_current_user)):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Not authorized")
    training_service.delete_training(training_id)
    return {"message": "Training deleted"}

@router.post("/availability", response_model=AvailabilityResponse, summary="Create a new availability", description="Create a new availability for a trainer.")
def create_availability(availability: AvailabilityCreate, current_user: str = Depends(get_current_user)):
    if "trainer" not in current_user.roles and "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Not authorized")
    return training_service.create_availability(availability)

@router.get("/availability", response_model=List[AvailabilityResponse], summary="Get all availabilities", description="Retrieve a list of all availabilities.")
def get_availabilities(current_user: str = Depends(get_current_user)):
    return training_service.get_availabilities()

@router.get("/availability/{availability_id}", response_model=AvailabilityResponse, summary="Get an availability by ID", description="Retrieve the details of a specific availability by its ID.")
def get_availability(availability_id: str, current_user: str = Depends(get_current_user)):
    return training_service.get_availability(availability_id)

@router.put("/availability/{availability_id}", response_model=AvailabilityResponse, summary="Update an availability", description="Update the details of a specific availability by its ID.")
def update_availability(availability_id: str, availability: AvailabilityUpdate, current_user: str = Depends(get_current_user)):
    if "trainer" not in current_user.roles and "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Not authorized")
    return training_service.update_availability(availability_id, availability)

@router.delete("/availability/{availability_id}", summary="Delete an availability", description="Delete a specific availability by its ID.")
def delete_availability(availability_id: str, current_user: str = Depends(get_current_user)):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Not authorized")
    training_service.delete_availability(availability_id)
    return {"message": "Availability deleted"}
