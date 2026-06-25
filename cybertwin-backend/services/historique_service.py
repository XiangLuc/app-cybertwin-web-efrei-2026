"""Service de l'historique."""

from domain.entities.historique import Historique
from domain.repositories.historique_repository import HistoriqueRepository
from shared.dto.mappers.historique_dto_mapper import HistoriqueDTOMapper

class HistoriqueService:
    def __init__(self, repository: HistoriqueRepository, mapper: HistoriqueDTOMapper):
        self.repository = repository
        self.mapper = mapper

    def enregistrer(self, analyse: dict, utilisateur_id=None, utilisateur_email=None):
        """Persiste le resultat d'un calcul de risque (dict renvoye par AnalyseService)."""
        entree = Historique.create(
            entreprise_id=analyse["entreprise_id"],
            score=analyse["score"],
            niveau_risque=analyse["niveau_risque"],
            nombre_actifs=analyse.get("nombre_actifs", 0),
            nombre_vulnerabilites=analyse.get("nombre_vulnerabilites", 0),
            utilisateur_id=utilisateur_id,
            utilisateur_email=utilisateur_email,
        )
        return self.repository.create_entree(entree)

    def lister(self, entreprise_id: int):
        return self.repository.find_by_entreprise(entreprise_id)