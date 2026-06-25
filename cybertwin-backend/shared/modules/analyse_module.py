"""Module analyse"""

from domain.repositories.actif_repository import ActifRepository
from domain.repositories.entreprise_repository import EntrepriseRepository
from domain.repositories.vulnerabilite_repository import VulnerabiliteRepository
from services.analyse_service import AnalyseService
from shared.dto.mappers.actif_dto_mapper import ActifDTOMapper
from shared.dto.mappers.entreprise_dto_mapper import EntrepriseDTOMapper
from shared.dto.mappers.vulnerabilite_dto_mapper import VulnerabiliteDTOMapper
from shared.dto.schemas.risk_dto import risk_dto

_service = AnalyseService(
    EntrepriseRepository(),
    ActifRepository(),
    VulnerabiliteRepository(),
    EntrepriseDTOMapper(),
    ActifDTOMapper(),
    VulnerabiliteDTOMapper(),
)

analyse_module = {
    "service": _service,
    "risk_schema": risk_dto,
}