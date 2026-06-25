"""Module auth"""

from domain.repositories.utilisateur_repository import UtilisateurRepository
from services.auth_service import AuthService
from shared.dto.mappers.utilisateur_dto_mapper import UtilisateurDTOMapper
from shared.dto.schemas.utilisateur_dto import login_dto, register_dto, change_password_dto, change_role_dto

_repository = UtilisateurRepository()
_mapper = UtilisateurDTOMapper()
_service = AuthService(_repository, _mapper)

auth_module = {
    "service": _service,
    "dto_mapper": _mapper,
    "register_schema": register_dto,
    "login_schema": login_dto,
    "change_password_schema": change_password_dto,
    "change_role_schema": change_role_dto
}