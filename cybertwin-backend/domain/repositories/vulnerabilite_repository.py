"""Repository de la vulnerabilite (CRUD via SQLAlchemy)."""
from typing import List, Optional

from domain.entities.actif import Actif
from domain.entities.vulnerabilite import Vulnerabilite
from infra.db.database import db


class VulnerabiliteRepository:
    def find_all(self, actif_id: int = None) -> List[Vulnerabilite]:
        query = Vulnerabilite.query
        if actif_id is not None:
            query = query.filter(Vulnerabilite.actif_id == actif_id)
        return query.order_by(Vulnerabilite.created_at.desc()).all()

    def find_by_entreprise(self, entreprise_id: int) -> List[Vulnerabilite]:
        """Toutes les vulnerabilites des actifs d'une entreprise (jointure)."""
        return (
            Vulnerabilite.query.join(Actif)
            .filter(Actif.entreprise_id == entreprise_id)
            .order_by(Vulnerabilite.created_at.desc())
            .all()
        )

    def find_by_id(self, vulnerabilite_id: int) -> Optional[Vulnerabilite]:
        return db.session.get(Vulnerabilite, vulnerabilite_id)

    def create_vulnerabilite(self, vulnerabilite: Vulnerabilite) -> Vulnerabilite:
        db.session.add(vulnerabilite)
        db.session.commit()
        db.session.refresh(vulnerabilite)
        return vulnerabilite

    def update_vulnerabilite(self, vulnerabilite: Vulnerabilite) -> Vulnerabilite:
        db.session.commit()
        db.session.refresh(vulnerabilite)
        return vulnerabilite

    def delete_vulnerabilite(self, vulnerabilite: Vulnerabilite) -> None:
        db.session.delete(vulnerabilite)
        db.session.commit()