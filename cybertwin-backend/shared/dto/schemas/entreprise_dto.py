"""
Schemas JSON de validation (utilises avec flask_expects_json).

  - entreprise_dto       : creation (POST) et remplacement complet (PUT)
  - entreprise_patch_dto : modification partielle (PATCH)
"""

entreprise_dto = {
    "type": "object",
    "properties": {
        "nom": {"type": "string", "minLength": 1},
        "secteur_activite": {"type": "string", "minLength": 1},
        "nombre_employes": {"type": "integer", "minimum": 0},
        "nombre_serveurs": {"type": "integer", "minimum": 0},
        "nombre_postes_clients": {"type": "integer", "minimum": 0},
        "services_exposes": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "nom",
        "secteur_activite",
        "nombre_employes",
        "nombre_serveurs",
        "nombre_postes_clients",
    ],
    "additionalProperties": False,
}

entreprise_patch_dto = {
    "type": "object",
    "properties": {
        "nom": {"type": "string", "minLength": 1},
        "secteur_activite": {"type": "string", "minLength": 1},
        "nombre_employes": {"type": "integer", "minimum": 0},
        "nombre_serveurs": {"type": "integer", "minimum": 0},
        "nombre_postes_clients": {"type": "integer", "minimum": 0},
        "services_exposes": {"type": "array", "items": {"type": "string"}},
    },
    "additionalProperties": False,
    "minProperties": 1,
}