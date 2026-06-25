"""Repository des notifications (SQLAlchemy)."""

from typing import List, Optional
from domain.entities.notification import Notification
from infra.db.database import db

class NotificationRepository:
    def find_by_utilisateur(self, utilisateur_id: int, limite: int = 50) -> List[Notification]:
        return (
            Notification.query.filter(Notification.utilisateur_id == utilisateur_id)
            .order_by(Notification.created_at.desc())
            .limit(limite)
            .all()
        )

    def count_non_lues(self, utilisateur_id: int) -> int:
        return Notification.query.filter(
            Notification.utilisateur_id == utilisateur_id, Notification.lu.is_(False)
        ).count()

    def find_by_id(self, notification_id: int) -> Optional[Notification]:
        return db.session.get(Notification, notification_id)

    def create_notification(self, notification: Notification) -> Notification:
        db.session.add(notification)
        db.session.commit()
        db.session.refresh(notification)
        return notification

    def marquer_toutes_lues(self, utilisateur_id: int) -> int:
        nb = Notification.query.filter(
            Notification.utilisateur_id == utilisateur_id, Notification.lu.is_(False)
        ).update({Notification.lu: True})
        db.session.commit()
        return nb

    def save(self, notification: Notification) -> Notification:
        db.session.commit()
        db.session.refresh(notification)
        return notification

    def delete_notification(self, notification: Notification) -> None:
        db.session.delete(notification)
        db.session.commit()