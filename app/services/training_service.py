from app.models.training import Training, Availability
from app.schemas.training import TrainingCreate, TrainingUpdate, AvailabilityCreate, AvailabilityUpdate
from typing import List
from datetime import datetime, timedelta
from app.config.database import database

class TrainingService:
    def __init__(self):
        self.training_container = database.get_container_client("trainings")
        self.availability_container = database.get_container_client("availabilities")

    def create_training(self, training: TrainingCreate) -> Training:
        new_training = Training(
            id="1",  # Generar un ID único
            trainer_id=training.trainer_id,
            user_id=training.user_id,
            start_time=training.start_time,
            end_time=training.end_time,
            status=training.status
        )
        self.training_container.create_item(new_training.dict(by_alias=True))
        return new_training

    def get_trainings(self) -> List[Training]:
        query = "SELECT * FROM trainings"
        items = list(self.training_container.query_items(query, enable_cross_partition_query=True))
        for item in items:
            item["_id"] = item.get("id", item.get("_id"))  # Map 'id' to '_id' if 'id' exists
        return [Training(**item) for item in items]

    def get_training(self, training_id: str) -> Training:
        item = self.training_container.read_item(item=training_id, partition_key=training_id)
        return Training(**item)

    def update_training(self, training_id: str, training: TrainingUpdate) -> Training:
        item = self.training_container.read_item(item=training_id, partition_key=training_id)
        existing_training = Training(**item)
        if existing_training.start_time - datetime.utcnow() < timedelta(hours=24):
            raise ValueError("Cannot modify training session within 24 hours of its start time.")
        updated_training = Training(**{**item, **training.dict(exclude_unset=True)})
        self.training_container.replace_item(item=training_id, body=updated_training.dict(by_alias=True))
        return updated_training

    def delete_training(self, training_id: str) -> None:
        self.training_container.delete_item(item=training_id, partition_key=training_id)

    def create_availability(self, availability: AvailabilityCreate) -> Availability:
        new_availability = Availability(
            id="1",  # Generar un ID único
            trainer_id=availability.trainer_id,
            center_id=availability.center_id,
            available_times=availability.available_times
        )
        self.availability_container.create_item(new_availability.dict(by_alias=True))
        return new_availability

    def get_availabilities(self) -> List[Availability]:
        query = "SELECT * FROM availabilities"
        items = list(self.availability_container.query_items(query, enable_cross_partition_query=True))
        return [Availability(**item) for item in items]

    def get_availability(self, availability_id: str) -> Availability:
        item = self.availability_container.read_item(item=availability_id, partition_key=availability_id)
        return Availability(**item)

    def update_availability(self, availability_id: str, availability: AvailabilityUpdate) -> Availability:
        item = self.availability_container.read_item(item=availability_id, partition_key=availability_id)
        updated_availability = Availability(**{**item, **availability.dict(exclude_unset=True)})
        self.availability_container.replace_item(item=availability_id, body=updated_availability.dict(by_alias=True))
        return updated_availability

    def delete_availability(self, availability_id: str) -> None:
        self.availability_container.delete_item(item=availability_id, partition_key=availability_id)
