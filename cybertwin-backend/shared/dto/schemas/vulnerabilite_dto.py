"""
Schemas JSON de validation de la vulnerabilite (flask_expects_json).

  - vulnerabilite_dto       : creation (POST) et remplacement complet (PUT)
  - vulnerabilite_patch_dto : modification partielle (PATCH)
"""
from domain.entities.vulnerabilite import NIVEAUX_CRITICITE

vulnerabilite_dto = {
    "type": "object",
    "properties": {
        "actif_id": {"type": "integer", "minimum": 1},
        "libelle": {"type": "string", "minLength": 1},
        "criticite": {"type": "string", "enum": NIVEAUX_CRITICITE},
        "description": {"type": ["string", "null"]},
    },
    "required": ["actif_id", "libelle", "criticite"],
    "additionalProperties": False,
}

vulnerabilite_patch_dto = {
    "type": "object",
    "properties": {
        "actif_id": {"type": "integer", "minimum": 1},
        "libelle": {"type": "string", "minLength": 1},
        "criticite": {"type": "string", "enum": NIVEAUX_CRITICITE},
        "description": {"type": ["string", "null"]},
    },
    "additionalProperties": False,
    "minProperties": 1,
}