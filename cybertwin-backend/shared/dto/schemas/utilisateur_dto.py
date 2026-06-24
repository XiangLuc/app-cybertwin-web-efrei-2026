"""
Schemas JSON de validation pour l'authentification (flask_expects_json).

"""
from domain.entities.utilisateur import ROLES

# Email valide via un pattern simple (evite la dependance "format": "email").
EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

register_dto = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "pattern": EMAIL_PATTERN},
        "mot_de_passe": {"type": "string"},
        "nom": {"type": ["string", "null"]},
        "prenom": {"type": ["string", "null"]},
        "role": {"type": "string", "enum": ROLES},
    },
    "required": ["email", "mot_de_passe"],
    "additionalProperties": False,
}

login_dto = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "pattern": EMAIL_PATTERN},
        "mot_de_passe": {"type": "string"},
    },
    "required": ["email", "mot_de_passe"],
    "additionalProperties": False,
}

change_password_dto = {
    "type": "object",
    "properties": {
        "ancien_mot_de_passe": {"type": "string"},
        "nouveau_mot_de_passe": {"type": "string"},
    },
    "required": ["ancien_mot_de_passe", "nouveau_mot_de_passe"],
    "additionalProperties": False,
}

change_role_dto = {
    "type": "object",
    "properties": {
        "role": {"type": "string", "enum": ROLES},
    },
    "required": ["role"],
    "additionalProperties": False,
}