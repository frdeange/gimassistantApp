from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate
from typing import List
from app.services.user_service import UserService
from app.config.database import database
from azure.communication.email import EmailClient
import os
from uuid import uuid4
from datetime import datetime, timezone

class NotificationService:
    def __init__(self):
        self.container = database.get_container_client("notifications")
        self.user_service = UserService()
        self.email_client = EmailClient.from_connection_string(
            os.getenv("AZURE_COMMUNICATION_SERVICE_CONNECTION_STRING")
        )

    def send_email(self, to_email: str, subject: str, body: str):
        email_message = {
            "senderAddress": os.getenv("EMAIL_ADDRESS"),
            "recipients": {
                "to": [{"address": to_email}]
            },
            "content": {
                "subject": subject,
                "plainText": body
            }
        }

        try:
            poller = self.email_client.begin_send(email_message)
            result = poller.result()
            print("Email sent successfully:", result)
        except Exception as e:
            print(f"Failed to send email: {e}")

    def create_notification(self, notification: NotificationCreate) -> Notification:
        # Mantener created_at como datetime (si no se proporciona, se asigna el tiempo actual)
        created_at = notification.created_at or datetime.now(timezone.utc)
        
        new_notification = Notification(
            id=str(uuid4()),  # Genera un ID único
            user_id=notification.user_id,
            message=notification.message,
            read=notification.read,
            created_at=created_at  # Se guarda como datetime
        )
        
        # Convertir a diccionario y luego transformar el datetime a ISO solo para enviar a CosmosDB
        notification_data = new_notification.model_dump(by_alias=True)
        if isinstance(notification_data.get("created_at"), datetime):
            notification_data["created_at"] = notification_data["created_at"].isoformat()
        
        self.container.create_item(notification_data)

        # Enviar correo electrónico
        user = self.user_service.get_user(notification.user_id) 
        self.send_email(user.email, "New Notification", notification.message)

        return new_notification

    def get_notifications(self, user_id: str) -> List[Notification]:
        query = f"SELECT * FROM notifications n WHERE n.user_id = '{user_id}'"
        items = list(self.container.query_items(query, enable_cross_partition_query=True))
        return [Notification(**item) for item in items]

    def update_notification(self, notification_id: str, notification: NotificationUpdate) -> Notification:
        item = self.container.read_item(item=notification_id, partition_key=notification_id)
        updated_notification = Notification(**{**item, **notification.dict(exclude_unset=True)})
        self.container.replace_item(item=notification_id, body=updated_notification.dict(by_alias=True))
        return updated_notification

    def delete_notification(self, notification_id: str) -> None:
        self.container.delete_item(item=notification_id, partition_key=notification_id)
