"""
Entite Actif (modele SQLAlchemy).

"""
import enum
from datetime import datetime

from infra.db.database import db


class TypeActif(enum.Enum):
    SERVEUR_WEB = "SERVEUR_WEB"
    BASE_DE_DONNEES = "BASE_DE_DONNEES"
    POSTE_UTILISATEUR = "POSTE_UTILISATEUR"
    ROUTEUR = "ROUTEUR"
    PARE_FEU = "PARE_FEU"
    APPLICATION_METIER = "APPLICATION_METIER"


# Liste des valeurs autorisees, reutilisee par le schema de validation.
TYPES_ACTIF = [t.value for t in TypeActif]


class Actif(db.Model):
    __tablename__ = "actif"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entreprise_id = db.Column(
        db.Integer,
        db.ForeignKey("entreprise.id", ondelete="CASCADE"),
        nullable=False,
    )
    nom = db.Column(db.String(255), nullable=False)
    type_actif = db.Column(db.Enum(TypeActif), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Relation vers l'entreprise. Le backref ajoute `entreprise.actifs` et la
    # suppression d'une entreprise supprime ses actifs (cascade ORM).
    entreprise = db.relationship(
        "Entreprise",
        backref=db.backref("actifs", cascade="all, delete-orphan"),
    )

    @classmethod
    def create(cls, nom, type_actif, entreprise_id, description=None):
        """Fabrique un Actif (id genere par la base). `type_actif` = string ou enum."""
        return cls(
            nom=nom,
            type_actif=TypeActif(type_actif),
            entreprise_id=entreprise_id,
            description=description,
        )

    def __repr__(self):
        return f"<Actif id={self.id} nom={self.nom!r} type={self.type_actif}>"