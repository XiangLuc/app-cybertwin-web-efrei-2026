"""Module actif"""

from domain.repositories.actif_repository import ActifRepository
from domain.repositories.entreprise_repository import EntrepriseRepository
from services.actif_service import ActifService
from shared.dto.mappers.actif_dto_mapper import ActifDTOMapper
from shared.dto.schemas.actif_dto import actif_dto, actif_patch_dto

_actif_repository = ActifRepository()
_entreprise_repository = EntrepriseRepository()
_mapper = ActifDTOMapper()
_service = ActifService(_actif_repository, _entreprise_repository, _mapper)

actif_module = {
    "service": _service,
    "dto_mapper": _mapper,
    "dto_schema": actif_dto,
    "dto_patch_schema": actif_patch_dto,
}