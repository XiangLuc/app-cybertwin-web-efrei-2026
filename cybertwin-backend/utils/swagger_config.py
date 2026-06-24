"""Configuration de la documentation Swagger (flasgger)."""

from domain.entities.actif import TYPES_ACTIF
from domain.entities.vulnerabilite import NIVEAUX_CRITICITE
from domain.entities.utilisateur import ROLES
from domain.entities.notification import TYPES_NOTIFICATION

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "ui_params": {"persistAuthorization": True},
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "CyberTwin API",
        "description": "Simulateur de risque cyber pour PME.",
        "version": "1.0.0",
    },
    "basePath": "/",
    "tags": [
        {"name": "Entreprise", "description": "Gestion de l'entreprise"},
        {"name": "Actif", "description": "Gestion des actifs informatiques"},
        {"name": "Vulnerabilite", "description": "Gestion des vulnerabilites"},
        {"name": "Analyse", "description": "Risque, tableau de bord et rapport"},
        {"name": "Auth", "description": "Authentification et utilisateurs"},
        {"name": "Notification", "description": "Gestion des alertes et notifications"},
    ],
    "definitions": {
        "EntrepriseCreate": {
            "type": "object",
            "required": [
                "nom",
                "secteur_activite",
                "nombre_employes",
                "nombre_serveurs",
                "nombre_postes_clients",
            ],
            "properties": {
                "nom": {"type": "string", "example": "TechNova Solutions"},
                "secteur_activite": {"type": "string", "example": "Edition de logiciels"},
                "nombre_employes": {"type": "integer", "example": 45},
                "nombre_serveurs": {"type": "integer", "example": 6},
                "nombre_postes_clients": {"type": "integer", "example": 40},
                "services_exposes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "example": ["HTTPS", "VPN", "SMTP"],
                },
            },
        },
        "EntrepriseUpdate": {
            "type": "object",
            "properties": {
                "nom": {"type": "string", "example": "TechNova Solutions"},
                "secteur_activite": {"type": "string", "example": "Cybersecurite"},
                "nombre_employes": {"type": "integer", "example": 52},
                "nombre_serveurs": {"type": "integer", "example": 8},
                "nombre_postes_clients": {"type": "integer", "example": 47},
                "services_exposes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "example": ["HTTPS", "VPN"],
                },
            },
        },
        "Entreprise": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "nom": {"type": "string"},
                "secteur_activite": {"type": "string"},
                "nombre_employes": {"type": "integer"},
                "nombre_serveurs": {"type": "integer"},
                "nombre_postes_clients": {"type": "integer"},
                "services_exposes": {"type": "array", "items": {"type": "string"}},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
            },
        },
        "ActifCreate": {
            "type": "object",
            "required": ["entreprise_id", "nom", "type_actif"],
            "properties": {
                "entreprise_id": {"type": "integer", "example": 1},
                "nom": {"type": "string", "example": "Serveur de production"},
                "type_actif": {"type": "string", "enum": TYPES_ACTIF, "example": "SERVEUR_WEB"},
                "description": {"type": "string", "example": "Heberge le site vitrine"},
            },
        },
        "ActifUpdate": {
            "type": "object",
            "properties": {
                "entreprise_id": {"type": "integer", "example": 1},
                "nom": {"type": "string", "example": "Serveur de production"},
                "type_actif": {"type": "string", "enum": TYPES_ACTIF, "example": "BASE_DE_DONNEES"},
                "description": {"type": "string"},
            },
        },
        "Actif": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "entreprise_id": {"type": "integer"},
                "nom": {"type": "string"},
                "type_actif": {"type": "string", "enum": TYPES_ACTIF},
                "description": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
            },
        },
        "VulnerabiliteCreate": {
            "type": "object",
            "required": ["actif_id", "libelle", "criticite"],
            "properties": {
                "actif_id": {"type": "integer", "example": 1},
                "libelle": {"type": "string", "example": "Logiciel obsolete"},
                "criticite": {"type": "string", "enum": NIVEAUX_CRITICITE, "example": "ELEVEE"},
                "description": {"type": "string", "example": "Version non maintenue"},
            },
        },
        "VulnerabiliteUpdate": {
            "type": "object",
            "properties": {
                "actif_id": {"type": "integer", "example": 1},
                "libelle": {"type": "string", "example": "Mot de passe faible"},
                "criticite": {"type": "string", "enum": NIVEAUX_CRITICITE, "example": "CRITIQUE"},
                "description": {"type": "string"},
            },
        },
        "Vulnerabilite": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "actif_id": {"type": "integer"},
                "libelle": {"type": "string"},
                "criticite": {"type": "string", "enum": NIVEAUX_CRITICITE},
                "description": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
            },
        },
        "Risque": {
            "type": "object",
            "properties": {
                "entreprise_id": {"type": "integer"},
                "nombre_actifs": {"type": "integer"},
                "nombre_vulnerabilites": {"type": "integer"},
                "score": {"type": "integer"},
                "niveau_risque": {"type": "string", "enum": ["FAIBLE", "MOYEN", "ELEVE"]},
                "details": {"type": "object"},
                "recommandations": {"type": "array", "items": {"type": "string"}},
            },
        },
        "Register": {
            "type": "object",
            "required": ["email", "mot_de_passe"],
            "properties": {
                "email": {"type": "string", "example": "admin@cybertwin.fr"},
                "mot_de_passe": {"type": "string", "example": "CyberTwin2024!secure"},
                "nom": {"type": "string", "example": "Dupont"},
                "prenom": {"type": "string", "example": "Marie"},
                "role": {"type": "string", "enum": ROLES, "example": "ANALYSTE"},
            },
        },
        "Login": {
            "type": "object",
            "required": ["email", "mot_de_passe"],
            "properties": {
                "email": {"type": "string", "example": "admin@cybertwin.fr"},
                "mot_de_passe": {"type": "string", "example": "CyberTwin2024!secure"},
            },
        },
        "Utilisateur": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "email": {"type": "string"},
                "nom": {"type": "string"},
                "prenom": {"type": "string"},
                "role": {"type": "string", "enum": ROLES},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"},
            },
        },
        "Notification": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "titre": {"type": "string"},
                "message": {"type": "string"},
                "type": {"type": "string", "enum": TYPES_NOTIFICATION},
                "lu": {"type": "boolean"},
                "created_at": {"type": "string", "format": "date-time"}
            }
        },
        "Erreur": {
            "type": "object",
            "properties": {"error": {"type": "string"}},
        },
    },
}