"""
Service d'authentification.

"""
import bcrypt
from flask_jwt_extended import create_access_token

from domain.entities.utilisateur import Role, Utilisateur
from utils.exceptions import (
    ConflictError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)
from domain.repositories.utilisateur_repository import UtilisateurRepository
from shared.dto.mappers.utilisateur_dto_mapper import UtilisateurDTOMapper
from utils.password_validator import valider_mot_de_passe


class AuthService:
    def __init__(self, repository: UtilisateurRepository, mapper: UtilisateurDTOMapper):
        self.repository = repository
        self.mapper = mapper

    def inscrire(self, dto: dict):
        email = self._email_normalise(dto["email"])
        self._verifier_mot_de_passe(dto.get("mot_de_passe", ""))
        self._verifier_email_libre(email)

        demande = dto.get("role", Role.LECTEUR.value)
        if demande == Role.ADMIN.value:
            raise ValidationError(
                "Le role ADMIN ne peut pas etre choisi a l'inscription."
            )
        role = Role(demande)

        return self._creer(email, dto["mot_de_passe"], role,
                        dto.get("nom"), dto.get("prenom"))


    def creer_par_admin(self, dto: dict):
        email = self._email_normalise(dto["email"])
        self._verifier_mot_de_passe(dto.get("mot_de_passe", ""))
        self._verifier_email_libre(email)
        role = Role(dto.get("role", Role.LECTEUR.value))
        return self._creer(email, dto["mot_de_passe"], role, dto.get("nom"), dto.get("prenom"))

    def connecter(self, email: str, mot_de_passe: str) -> dict:
        utilisateur = self.repository.find_by_email(self._email_normalise(email))
        if utilisateur is None or not self._mot_de_passe_correct(mot_de_passe, utilisateur):
            raise UnauthorizedError("Email ou mot de passe incorrect.")
        token = create_access_token(
            identity=str(utilisateur.id),
            additional_claims={"role": utilisateur.role.value, "email": utilisateur.email},
        )
        return {
            "access_token": token,
            "role": utilisateur.role.value,
            "utilisateur": self.mapper.to_external(utilisateur),
        }
    
    def changer_mot_de_passe(self, utilisateur_id, ancien, nouveau):
        utilisateur = self.get_by_id(utilisateur_id)
        
        if not self._mot_de_passe_correct(ancien, utilisateur):
            raise UnauthorizedError("L'ancien mot de passe est incorrect.")
            
        self._verifier_mot_de_passe(nouveau)
        
        utilisateur.mot_de_passe = bcrypt.hashpw(
            nouveau.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        
        return self.repository.create_utilisateur(utilisateur)

    def changer_role(self, utilisateur_id, role, demandeur_id):
        from domain.entities.utilisateur import Role
        
        if utilisateur_id == demandeur_id and role != Role.ADMIN.value:
            raise ValidationError("Un administrateur ne peut pas retirer son propre role ADMIN.")
            
        utilisateur = self.get_by_id(utilisateur_id)
        utilisateur.role = Role(role)
        
        return self.repository.create_utilisateur(utilisateur)

    # --- Gestion (ADMIN) -----------------------------------------------------
    def lister(self):
        return self.repository.find_all()

    def get_by_id(self, utilisateur_id: int):
        utilisateur = self.repository.find_by_id(utilisateur_id)
        if utilisateur is None:
            raise NotFoundError(
                f"Aucun utilisateur trouve avec l'identifiant '{utilisateur_id}'."
            )
        return utilisateur

    def supprimer(self, utilisateur_id: int):
        utilisateur = self.get_by_id(utilisateur_id)
        self.repository.delete_utilisateur(utilisateur)

    # --- Helpers prives ------------------------------------------------------
    def _creer(self, email, mot_de_passe_clair, role, nom, prenom):
        hash_ = bcrypt.hashpw(mot_de_passe_clair.encode("utf-8"), bcrypt.gensalt())
        utilisateur = Utilisateur.create(
            email=email,
            mot_de_passe_hash=hash_.decode("utf-8"),
            role=role,
            nom=nom,
            prenom=prenom,
        )
        return self.repository.create_utilisateur(utilisateur)

    @staticmethod
    def _mot_de_passe_correct(mot_de_passe_clair, utilisateur) -> bool:
        return bcrypt.checkpw(
            mot_de_passe_clair.encode("utf-8"),
            utilisateur.mot_de_passe.encode("utf-8"),
        )

    @staticmethod
    def _verifier_mot_de_passe(mot_de_passe):
        erreurs = valider_mot_de_passe(mot_de_passe)
        if erreurs:
            raise ValidationError(
                "Mot de passe non conforme aux recommandations de securite.",
                details=erreurs,
            )

    def _verifier_email_libre(self, email):
        if self.repository.exists_by_email(email):
            raise ConflictError(f"L'email '{email}' est deja utilise.")

    @staticmethod
    def _email_normalise(email):
        return (email or "").strip().lower()