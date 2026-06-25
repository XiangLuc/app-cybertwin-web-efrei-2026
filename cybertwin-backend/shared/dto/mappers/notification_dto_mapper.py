"""Mapper de sortie pour les notifications."""

from domain.entities.notification import Notification
from domain.kernel.mapper import BaseMapper

class NotificationDTOMapper(BaseMapper[Notification, dict]):
    def to_domain(self, dto: dict) -> Notification:
        raise NotImplementedError("Les notifications sont creees par le service.")

    def to_external(self, notification: Notification) -> dict:
        return {
            "id": notification.id,
            "titre": notification.titre,
            "message": notification.message,
            "type": notification.type.value if notification.type else None,
            "lu": notification.lu,
            "created_at": notification.created_at.isoformat() if notification.created_at else None,
        }