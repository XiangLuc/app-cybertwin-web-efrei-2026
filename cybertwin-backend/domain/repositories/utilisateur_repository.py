"""Repository de l'utilisateur (CRUD via SQLAlchemy)."""
from typing import List, Optional

from domain.entities.utilisateur import Utilisateur
from infra.db.database import db


class UtilisateurRepository:
    def find_all(self) -> List[Utilisateur]:
        return Utilisateur.query.order_by(Utilisateur.created_at.desc()).all()

    def find_by_id(self, utilisateur_id: int) -> Optional[Utilisateur]:
        return db.session.get(Utilisateur, utilisateur_id)

    def find_by_email(self, email: str) -> Optional[Utilisateur]:
        return Utilisateur.query.filter(Utilisateur.email == email).first()

    def exists_by_email(self, email: str) -> bool:
        return db.session.query(
            Utilisateur.query.filter(Utilisateur.email == email).exists()
        ).scalar()

    def count(self) -> int:
        return Utilisateur.query.count()

    def create_utilisateur(self, utilisateur: Utilisateur) -> Utilisateur:
        db.session.add(utilisateur)
        db.session.commit()
        db.session.refresh(utilisateur)
        return utilisateur

    def delete_utilisateur(self, utilisateur: Utilisateur) -> None:
        db.session.delete(utilisateur)
        db.session.commit()