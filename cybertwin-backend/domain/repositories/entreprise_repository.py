"""Repository de l'entreprise."""

from typing import List, Optional

from domain.entities.entreprise import Entreprise
from infra.db.database import db


class EntrepriseRepository:
    def find_all(self) -> List[Entreprise]:
        return Entreprise.query.order_by(Entreprise.created_at.desc()).all()

    def find_by_id(self, entreprise_id: str) -> Optional[Entreprise]:
        return db.session.get(Entreprise, entreprise_id)

    def exists_by_nom(self, nom: str, exclude_id: str = None) -> bool:
        query = Entreprise.query.filter(Entreprise.nom == nom)
        if exclude_id is not None:
            query = query.filter(Entreprise.id != exclude_id)
        return db.session.query(query.exists()).scalar()

    def create_entreprise(self, entreprise: Entreprise) -> Entreprise:
        db.session.add(entreprise)
        db.session.commit()
        db.session.refresh(entreprise)
        return entreprise

    def update_entreprise(self, entreprise: Entreprise) -> Entreprise:
        db.session.commit()
        db.session.refresh(entreprise)
        return entreprise

    def delete_entreprise(self, entreprise: Entreprise) -> None:
        db.session.delete(entreprise)
        db.session.commit()