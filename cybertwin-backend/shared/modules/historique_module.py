"""Module historique"""

from domain.repositories.historique_repository import HistoriqueRepository
from services.historique_service import HistoriqueService
from shared.dto.mappers.historique_dto_mapper import HistoriqueDTOMapper

_repository = HistoriqueRepository()
_mapper = HistoriqueDTOMapper()
_service = HistoriqueService(_repository, _mapper)

historique_module = {
    "service": _service, 
    "dto_mapper": _mapper
}