"""
Entite Vulnerabilite (modele SQLAlchemy).

"""
import enum
from datetime import datetime

from infra.db.database import db


class Criticite(enum.Enum):
    FAIBLE = "FAIBLE"
    MOYENNE = "MOYENNE"
    ELEVEE = "ELEVEE"
    CRITIQUE = "CRITIQUE"


NIVEAUX_CRITICITE = [c.value for c in Criticite]

# Poids utilise pour le calcul du score de risque.
POIDS_CRITICITE = {
    Criticite.FAIBLE: 1,
    Criticite.MOYENNE: 2,
    Criticite.ELEVEE: 3,
    Criticite.CRITIQUE: 5,
}


class Vulnerabilite(db.Model):
    __tablename__ = "vulnerabilite"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actif_id = db.Column(
        db.Integer,
        db.ForeignKey("actif.id", ondelete="CASCADE"),
        nullable=False,
    )
    libelle = db.Column(db.String(255), nullable=False)
    criticite = db.Column(db.Enum(Criticite), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Relation vers l'actif (backref `actif.vulnerabilites`, cascade ORM).
    actif = db.relationship(
        "Actif",
        backref=db.backref("vulnerabilites", cascade="all, delete-orphan"),
    )

    @classmethod
    def create(cls, libelle, criticite, actif_id, description=None):
        """Fabrique une Vulnerabilite. `criticite` = string ou enum."""
        return cls(
            libelle=libelle,
            criticite=Criticite(criticite),
            actif_id=actif_id,
            description=description,
        )

    def __repr__(self):
        return f"<Vulnerabilite id={self.id} libelle={self.libelle!r} criticite={self.criticite}>"