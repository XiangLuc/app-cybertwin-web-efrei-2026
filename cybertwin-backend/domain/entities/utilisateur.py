"""
Entite Utilisateur (modele SQLAlchemy).

"""
import enum
from datetime import datetime

from infra.db.database import db


class Role(enum.Enum):
    ADMIN = "ADMIN"
    ANALYSTE = "ANALYSTE"
    LECTEUR = "LECTEUR"


ROLES = [r.value for r in Role]


class Utilisateur(db.Model):
    __tablename__ = "utilisateur"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(255), nullable=False)  # hash bcrypt
    nom = db.Column(db.String(255), nullable=True)
    prenom = db.Column(db.String(255), nullable=True)
    role = db.Column(db.Enum(Role), nullable=False, default=Role.LECTEUR)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    @classmethod
    def create(cls, email, mot_de_passe_hash, role, nom=None, prenom=None):
        """Fabrique un Utilisateur. `role` = string ou enum ; mot de passe deja hashe."""
        return cls(
            email=email,
            mot_de_passe=mot_de_passe_hash,
            role=Role(role),
            nom=nom,
            prenom=prenom,
        )

    def __repr__(self):
        return f"<Utilisateur id={self.id} email={self.email!r} role={self.role}>"