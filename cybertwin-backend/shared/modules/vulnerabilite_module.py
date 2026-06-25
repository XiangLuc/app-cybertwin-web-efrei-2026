"""Module vulnerabilite"""

from domain.repositories.actif_repository import ActifRepository
from domain.repositories.vulnerabilite_repository import VulnerabiliteRepository
from services.vulnerabilite_service import VulnerabiliteService
from shared.dto.mappers.vulnerabilite_dto_mapper import VulnerabiliteDTOMapper
from shared.dto.schemas.vulnerabilite_dto import (
    vulnerabilite_dto,
    vulnerabilite_patch_dto,
)

_repository = VulnerabiliteRepository()
_actif_repository = ActifRepository()
_mapper = VulnerabiliteDTOMapper()
_service = VulnerabiliteService(_repository, _actif_repository, _mapper)

vulnerabilite_module = {
    "service": _service,
    "dto_mapper": _mapper,
    "dto_schema": vulnerabilite_dto,
    "dto_patch_schema": vulnerabilite_patch_dto,
}