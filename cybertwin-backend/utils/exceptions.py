"""Exceptions metier partagees, mappees vers des codes HTTP dans les controllers."""


class DomainError(Exception):
    """Exception metier de base."""


class NotFoundError(DomainError):
    """Ressource introuvable -> 404."""


class ConflictError(DomainError):
    """Conflit, ex : doublon -> 409."""


class ValidationError(DomainError):
    """Donnees metier invalides (ex : mot de passe non conforme) -> 400."""

    def __init__(self, message, details=None):
        super().__init__(message)
        self.message = message
        self.details = details


class UnauthorizedError(DomainError):
    """Echec d'authentification -> 401."""