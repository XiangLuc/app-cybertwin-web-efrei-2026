"""Repository de l'historique des analyses (SQLAlchemy)."""

from typing import List
from domain.entities.historique import Historique
from infra.db.database import db

class HistoriqueRepository:
    def find_by_entreprise(self, entreprise_id: int, limite: int = 50) -> List[Historique]:
        return (
            Historique.query.filter(Historique.entreprise_id == entreprise_id)
            .order_by(Historique.created_at.desc())
            .limit(limite)
            .all()
        )

    def create_entree(self, entree: Historique) -> Historique:
        db.session.add(entree)
        db.session.commit()
        db.session.refresh(entree)
        return entree