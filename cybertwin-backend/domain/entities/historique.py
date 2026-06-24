"""Entite Historique (modele SQLAlchemy)"""

from datetime import datetime
from infra.db.database import db

class Historique(db.Model):
    __tablename__ = "analyse_historique"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entreprise_id = db.Column(db.Integer, db.ForeignKey("entreprise.id", ondelete="CASCADE"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    niveau_risque = db.Column(db.String(20), nullable=False)
    nombre_actifs = db.Column(db.Integer, nullable=False, default=0)
    nombre_vulnerabilites = db.Column(db.Integer, nullable=False, default=0)
    
    # Auteur de l'analyse (denormalise pour l'affichage meme si le compte est supprime).
    utilisateur_id = db.Column(db.Integer, nullable=True)
    utilisateur_email = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    entreprise = db.relationship(
        "Entreprise",
        backref=db.backref("analyses", cascade="all, delete-orphan"),
    )

    @classmethod
    def create(cls, entreprise_id, score, niveau_risque, nombre_actifs,
               nombre_vulnerabilites, utilisateur_id=None, utilisateur_email=None):
        return cls(
            entreprise_id=entreprise_id,
            score=score,
            niveau_risque=niveau_risque,
            nombre_actifs=nombre_actifs,
            nombre_vulnerabilites=nombre_vulnerabilites,
            utilisateur_id=utilisateur_id,
            utilisateur_email=utilisateur_email,
        )