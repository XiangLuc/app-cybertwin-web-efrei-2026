"""Module notification"""

from domain.repositories.notification_repository import NotificationRepository
from services.notification_service import NotificationService
from shared.dto.mappers.notification_dto_mapper import NotificationDTOMapper

_repository = NotificationRepository()
_mapper = NotificationDTOMapper()
_service = NotificationService(_repository, _mapper)

notification_module = {
    "service": _service, 
    "dto_mapper": _mapper
}