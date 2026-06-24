"""
Mapper DTO <-> entite Utilisateur.

"""
from domain.entities.utilisateur import Utilisateur
from domain.kernel.mapper import BaseMapper


class UtilisateurDTOMapper(BaseMapper[Utilisateur, dict]):
    def to_domain(self, dto: dict) -> Utilisateur:
        # La creation passe par le service (hash du mot de passe) : non utilise ici.
        raise NotImplementedError("Utiliser AuthService pour creer un utilisateur.")

    def to_external(self, utilisateur: Utilisateur) -> dict:
        return {
            "id": utilisateur.id,
            "email": utilisateur.email,
            "nom": utilisateur.nom,
            "prenom": utilisateur.prenom,
            "role": utilisateur.role.value if utilisateur.role else None,
            "created_at": utilisateur.created_at.isoformat() if utilisateur.created_at else None,
            "updated_at": utilisateur.updated_at.isoformat() if utilisateur.updated_at else None,
        }