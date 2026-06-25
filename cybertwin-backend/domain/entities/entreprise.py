"""
Entite Entreprise (modele SQLAlchemy).

"""
from datetime import datetime

from infra.db.database import db


class Entreprise(db.Model):
    __tablename__ = "entreprise"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(255), nullable=False, unique=True)
    secteur_activite = db.Column(db.String(255), nullable=False)
    nombre_employes = db.Column(db.Integer, nullable=False, default=0)
    nombre_serveurs = db.Column(db.Integer, nullable=False, default=0)
    nombre_postes_clients = db.Column(db.Integer, nullable=False, default=0)
    services_exposes = db.Column(db.JSON, nullable=False, default=list)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    @classmethod
    def create(cls, nom, secteur_activite, nombre_employes, nombre_serveurs,
               nombre_postes_clients, services_exposes=None):
        """Fabrique une instance Entreprise (id genere par la base)."""
        return cls(
            nom=nom,
            secteur_activite=secteur_activite,
            nombre_employes=nombre_employes,
            nombre_serveurs=nombre_serveurs,
            nombre_postes_clients=nombre_postes_clients,
            services_exposes=services_exposes or [],
        )

    def __repr__(self):
        return f"<Entreprise id={self.id} nom={self.nom!r}>"