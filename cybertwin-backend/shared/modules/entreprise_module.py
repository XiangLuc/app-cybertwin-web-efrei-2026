"""Module entreprise"""

from domain.repositories.entreprise_repository import EntrepriseRepository
from services.entreprise_service import EntrepriseService
from shared.dto.mappers.entreprise_dto_mapper import EntrepriseDTOMapper
from shared.dto.schemas.entreprise_dto import entreprise_dto, entreprise_patch_dto

_repository = EntrepriseRepository()
_mapper = EntrepriseDTOMapper()
_service = EntrepriseService(_repository, _mapper)

entreprise_module = {
    "service": _service,
    "dto_mapper": _mapper,
    "dto_schema": entreprise_dto,
    "dto_patch_schema": entreprise_patch_dto,
}