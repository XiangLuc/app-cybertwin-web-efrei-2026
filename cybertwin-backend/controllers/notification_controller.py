"""Controller des notifications (/notifications)."""

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity

from utils.exceptions import NotFoundError
from shared.modules.notification_module import notification_module
from utils.security import roles_required

service = notification_module["service"]
mapper = notification_module["dto_mapper"]
notification_bp = Blueprint("notification_bp", __name__)

def _moi():
    return int(get_jwt_identity())

@notification_bp.route("", methods=["GET"])
@roles_required()
def lister():
    """
    Lister mes notifications
    ---
    tags: [Notification]
    security:
      - Bearer: []
    responses:
      200:
        description: Liste des notifications de l'utilisateur connecte
    """
    return jsonify(mapper.to_external_list(service.lister(_moi()))), 200

@notification_bp.route("/unread-count", methods=["GET"])
@roles_required()
def compter():
    """
    Nombre de notifications non lues
    ---
    tags: [Notification]
    security:
      - Bearer: []
    responses:
      200:
        description: Compteur
    """
    return jsonify({"count": service.compter_non_lues(_moi())}), 200

@notification_bp.route("/<int:notification_id>/read", methods=["PATCH"])
@roles_required()
def marquer_lue(notification_id):
    """
    Marquer une notification comme lue
    ---
    tags: [Notification]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: notification_id
        type: integer
        required: true
    responses:
      200: {description: Notification marquee comme lue}
      404: {description: Introuvable, schema: {$ref: '#/definitions/Erreur'}}
    """
    try:
        return jsonify(mapper.to_external(service.marquer_lue(notification_id, _moi()))), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404

@notification_bp.route("/read-all", methods=["POST"])
@roles_required()
def marquer_toutes_lues():
    """
    Marquer toutes mes notifications comme lues
    ---
    tags: [Notification]
    security:
      - Bearer: []
    responses:
      200: {description: Nombre de notifications marquees}
    """
    nb = service.marquer_toutes_lues(_moi())
    return jsonify({"message": f"{nb} notification(s) marquee(s) comme lue(s).", "count": nb}), 200

@notification_bp.route("/<int:notification_id>", methods=["DELETE"])
@roles_required()
def supprimer(notification_id):
    """
    Supprimer une notification
    ---
    tags: [Notification]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: notification_id
        type: integer
        required: true
    responses:
      200: {description: Supprimee}
      404: {description: Introuvable, schema: {$ref: '#/definitions/Erreur'}}
    """
    try:
        service.supprimer(notification_id, _moi())
        return jsonify({"message": "Notification supprimee."}), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404