"""Entite Notification (modele SQLAlchemy)"""

import enum
from datetime import datetime
from infra.db.database import db

class TypeNotification(enum.Enum):
    INFO = "INFO"
    SUCCES = "SUCCES"
    ALERTE = "ALERTE"

TYPES_NOTIFICATION = [t.value for t in TypeNotification]

class Notification(db.Model):
    __tablename__ = "notification"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utilisateur_id = db.Column(
        db.Integer, db.ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=False
    )
    titre = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    type = db.Column(db.Enum(TypeNotification), nullable=False, default=TypeNotification.INFO)
    lu = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    utilisateur = db.relationship(
        "Utilisateur",
        backref=db.backref("notifications", cascade="all, delete-orphan"),
    )

    @classmethod
    def create(cls, utilisateur_id, titre, message, type=TypeNotification.INFO):
        return cls(
            utilisateur_id=utilisateur_id,
            titre=titre,
            message=message,
            type=TypeNotification(type) if not isinstance(type, TypeNotification) else type,
        )