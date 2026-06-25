"""Repository de l'actif (CRUD via SQLAlchemy)."""
from typing import List, Optional

from domain.entities.actif import Actif
from infra.db.database import db


class ActifRepository:
    def find_all(self, entreprise_id: int = None) -> List[Actif]:
        query = Actif.query
        if entreprise_id is not None:
            query = query.filter(Actif.entreprise_id == entreprise_id)
        return query.order_by(Actif.created_at.desc()).all()

    def find_by_id(self, actif_id: int) -> Optional[Actif]:
        return db.session.get(Actif, actif_id)

    def create_actif(self, actif: Actif) -> Actif:
        db.session.add(actif)
        db.session.commit()
        db.session.refresh(actif)
        return actif

    def update_actif(self, actif: Actif) -> Actif:
        db.session.commit()
        db.session.refresh(actif)
        return actif

    def delete_actif(self, actif: Actif) -> None:
        db.session.delete(actif)
        db.session.commit()