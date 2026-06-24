"""Mapper de sortie pour l'historique."""

from domain.entities.historique import Historique
from domain.kernel.mapper import BaseMapper

class HistoriqueDTOMapper(BaseMapper[Historique, dict]):
    def to_domain(self, dto: dict) -> Historique:
        raise NotImplementedError("L'historique est genere par le service d'analyse.")

    def to_external(self, entree: Historique) -> dict:
        return {
            "id": entree.id,
            "entreprise_id": entree.entreprise_id,
            "score": entree.score,
            "niveau_risque": entree.niveau_risque,
            "nombre_actifs": entree.nombre_actifs,
            "nombre_vulnerabilites": entree.nombre_vulnerabilites,
            "utilisateur_email": entree.utilisateur_email,
            "created_at": entree.created_at.isoformat() if entree.created_at else None,
        }