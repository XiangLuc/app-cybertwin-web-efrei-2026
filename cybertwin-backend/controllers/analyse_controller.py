"""Controller d'analyse (moteur de risque, tableau de bord, rapport, historique).
Endpoints :
  - POST /risk/calculate         
  - GET  /dashboard/<entreprise_id> 
  - GET  /report/<entreprise_id>   
  - GET  /history/<entreprise_id> 
"""

from flask import Blueprint, jsonify, request
from flask_expects_json import expects_json
from flask_jwt_extended import get_jwt, get_jwt_identity

from domain.entities.notification import TypeNotification
from domain.repositories.utilisateur_repository import UtilisateurRepository
from utils.exceptions import NotFoundError
from shared.modules.analyse_module import analyse_module
from shared.modules.historique_module import historique_module
from shared.modules.notification_module import notification_module
from utils.security import roles_required

service = analyse_module["service"]
risk_schema = analyse_module["risk_schema"]
historique_service = historique_module["service"]
historique_mapper = historique_module["dto_mapper"]
notification_service = notification_module["service"]

_utilisateur_repository = UtilisateurRepository()

analyse_bp = Blueprint("analyse_bp", __name__)

@analyse_bp.route("/risk/calculate", methods=["POST"])
@roles_required()
@expects_json(risk_schema)
def calculer_risque():
    """
    Calculer le risque cyber d'une entreprise
    ---
    tags: [Analyse]
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [entreprise_id]
          properties:
            entreprise_id: {type: integer, example: 1}
    responses:
      200: {description: Score et niveau de risque, schema: {$ref: '#/definitions/Risque'}}
      404: {description: Entreprise introuvable, schema: {$ref: '#/definitions/Erreur'}}
    """
    dto = request.json
    try:
        resultat = service.calculer_risque(dto["entreprise_id"])
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

    utilisateur_id = int(get_jwt_identity())

    utilisateur = _utilisateur_repository.find_by_id(utilisateur_id)
    utilisateur_email = utilisateur.email if utilisateur else get_jwt().get("email")
    historique_service.enregistrer(resultat, utilisateur_id, utilisateur_email)

    _config_notif = {
        "ELEVE": ("Risque cyber eleve", TypeNotification.ALERTE),
        "MOYEN": ("Risque cyber modere", TypeNotification.INFO),
        "FAIBLE": ("Risque cyber faible", TypeNotification.SUCCES),
    }
    titre, type_notif = _config_notif.get(
        resultat["niveau_risque"], ("Analyse de risque effectuee", TypeNotification.INFO)
    )
    notification_service.notifier(
        utilisateur_id,
        titre=titre,
        message=(
            f"Analyse terminee : niveau {resultat['niveau_risque']} "
            f"(score {resultat['score']}, {resultat['nombre_vulnerabilites']} vulnerabilite(s))."
        ),
        type=type_notif,
    )

    return jsonify(resultat), 200


@analyse_bp.route("/dashboard/<int:entreprise_id>", methods=["GET"])
@roles_required()
def dashboard(entreprise_id):
    """
    Donnees du tableau de bord d'une entreprise
    ---
    tags: [Analyse]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: entreprise_id
        type: integer
        required: true
    responses:
      200: {description: Statistiques du tableau de bord}
      404: {description: Entreprise introuvable, schema: {$ref: '#/definitions/Erreur'}}
    """
    try:
        return jsonify(service.dashboard(entreprise_id)), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

@analyse_bp.route("/report/<int:entreprise_id>", methods=["GET"])
@roles_required()
def rapport(entreprise_id):
    """
    Rapport final d'une entreprise
    ---
    tags: [Analyse]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: entreprise_id
        type: integer
        required: true
    responses:
      200: {description: Rapport complet}
      404: {description: Entreprise introuvable, schema: {$ref: '#/definitions/Erreur'}}
    """
    try:
        return jsonify(service.rapport(entreprise_id)), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

@analyse_bp.route("/history/<int:entreprise_id>", methods=["GET"])
@roles_required()
def historique(entreprise_id):
    """
    Historique des analyses d'une entreprise
    ---
    tags: [Analyse]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: entreprise_id
        type: integer
        required: true
    responses:
      200: {description: Liste des analyses passees (plus recentes d'abord)}
    """
    entrees = historique_service.lister(entreprise_id)
    return jsonify(historique_mapper.to_external_list(entrees)), 200