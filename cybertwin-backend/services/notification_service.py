"""Service des notifications.
Expose `notifier(...)` utilise par les autres services pour creer une
notification destinee a un utilisateur, et les operations de consultation /
marquage / suppression."""

from domain.entities.notification import Notification, TypeNotification
from utils.exceptions import NotFoundError
from domain.repositories.notification_repository import NotificationRepository
from shared.dto.mappers.notification_dto_mapper import NotificationDTOMapper

class NotificationService:
    def __init__(self, repository: NotificationRepository, mapper: NotificationDTOMapper):
        self.repository = repository
        self.mapper = mapper

    def notifier(self, utilisateur_id, titre, message, type=TypeNotification.INFO):
        notification = Notification.create(utilisateur_id, titre, message, type)
        return self.repository.create_notification(notification)

    def lister(self, utilisateur_id):
        return self.repository.find_by_utilisateur(utilisateur_id)

    def compter_non_lues(self, utilisateur_id):
        return self.repository.count_non_lues(utilisateur_id)

    def marquer_lue(self, notification_id, utilisateur_id):
        notification = self._require(notification_id, utilisateur_id)
        notification.lu = True
        return self.repository.save(notification)

    def marquer_toutes_lues(self, utilisateur_id):
        return self.repository.marquer_toutes_lues(utilisateur_id)

    def supprimer(self, notification_id, utilisateur_id):
        notification = self._require(notification_id, utilisateur_id)
        self.repository.delete_notification(notification)

    def _require(self, notification_id, utilisateur_id):
        notification = self.repository.find_by_id(notification_id)
        # On verifie aussi que la notification appartient bien a l'utilisateur.
        if notification is None or notification.utilisateur_id != utilisateur_id:
            raise NotFoundError(f"Notification '{notification_id}' introuvable.")
        return notification