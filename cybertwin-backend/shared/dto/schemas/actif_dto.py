"""
Schemas JSON de validation de l'actif (utilises avec flask_expects_json).

  - actif_dto       : creation (POST) et remplacement complet (PUT)
  - actif_patch_dto : modification partielle (PATCH)

`type_actif` est valide contre la liste figee TYPES_ACTIF (enum).
"""
from domain.entities.actif import TYPES_ACTIF

actif_dto = {
    "type": "object",
    "properties": {
        "entreprise_id": {"type": "integer", "minimum": 1},
        "nom": {"type": "string", "minLength": 1},
        "type_actif": {"type": "string", "enum": TYPES_ACTIF},
        "description": {"type": ["string", "null"]},
    },
    "required": ["entreprise_id", "nom", "type_actif"],
    "additionalProperties": False,
}

actif_patch_dto = {
    "type": "object",
    "properties": {
        "entreprise_id": {"type": "integer", "minimum": 1},
        "nom": {"type": "string", "minLength": 1},
        "type_actif": {"type": "string", "enum": TYPES_ACTIF},
        "description": {"type": ["string", "null"]},
    },
    "additionalProperties": False,
    "minProperties": 1,
}