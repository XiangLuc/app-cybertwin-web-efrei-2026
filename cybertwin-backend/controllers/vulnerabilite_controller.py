"""Controller de la vulnerabilite."""
from flask import Blueprint, jsonify, request
from flask_expects_json import expects_json

from utils.exceptions import NotFoundError
from shared.modules.vulnerabilite_module import vulnerabilite_module

service = vulnerabilite_module["service"]
mapper = vulnerabilite_module["dto_mapper"]
vulnerabilite_schema = vulnerabilite_module["dto_schema"]
vulnerabilite_patch_schema = vulnerabilite_module["dto_patch_schema"]

vulnerabilite_bp = Blueprint("vulnerabilite_bp", __name__)


@vulnerabilite_bp.route("", methods=["GET"])
def get_vulnerabilites():
    """
    Lister les vulnerabilites (filtre par actif ou par entreprise)
    ---
    tags: [Vulnerabilite]
    parameters:
      - in: query
        name: actif_id
        type: integer
        required: false
      - in: query
        name: entreprise_id
        type: integer
        required: false
        description: Toutes les vulnerabilites des actifs de cette entreprise
    responses:
      200:
        description: Liste des vulnerabilites
        schema:
          type: array
          items: {$ref: '#/definitions/Vulnerabilite'}
      404:
        description: Actif filtre introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    actif_id = request.args.get("actif_id", type=int)
    entreprise_id = request.args.get("entreprise_id", type=int)
    try:
        vulnerabilites = service.get_all(actif_id=actif_id, entreprise_id=entreprise_id)
        return jsonify(mapper.to_external_list(vulnerabilites)), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@vulnerabilite_bp.route("/<int:vulnerabilite_id>", methods=["GET"])
def get_vulnerabilite(vulnerabilite_id):
    """
    Consulter une vulnerabilite
    ---
    tags: [Vulnerabilite]
    parameters:
      - in: path
        name: vulnerabilite_id
        type: integer
        required: true
    responses:
      200:
        description: Fiche de la vulnerabilite
        schema: {$ref: '#/definitions/Vulnerabilite'}
      404:
        description: Vulnerabilite introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    try:
        vulnerabilite = service.get_by_id(vulnerabilite_id)
        return jsonify(mapper.to_external(vulnerabilite)), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@vulnerabilite_bp.route("", methods=["POST"])
@expects_json(vulnerabilite_schema)
def create_vulnerabilite():
    """
    Associer une vulnerabilite a un actif
    ---
    tags: [Vulnerabilite]
    parameters:
      - in: body
        name: body
        required: true
        schema: {$ref: '#/definitions/VulnerabiliteCreate'}
    responses:
      201:
        description: Vulnerabilite creee
      404:
        description: Actif lie introuvable
        schema: {$ref: '#/definitions/Erreur'}
      400:
        description: Donnees invalides
        schema: {$ref: '#/definitions/Erreur'}
    """
    dto = request.json
    try:
        created = service.create_vulnerabilite(dto)
        return jsonify({
            "message": "Vulnerabilite creee avec succes.",
            "vulnerabilite": mapper.to_external(created),
        }), 201
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@vulnerabilite_bp.route("/<int:vulnerabilite_id>", methods=["PUT"])
@expects_json(vulnerabilite_schema)
def update_vulnerabilite(vulnerabilite_id):
    """
    Remplacer une vulnerabilite (mise a jour complete)
    ---
    tags: [Vulnerabilite]
    parameters:
      - in: path
        name: vulnerabilite_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema: {$ref: '#/definitions/VulnerabiliteCreate'}
    responses:
      200:
        description: Vulnerabilite mise a jour
      404:
        description: Vulnerabilite ou actif introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    dto = request.json
    try:
        updated = service.update_vulnerabilite(vulnerabilite_id, dto)
        return jsonify({
            "message": "Vulnerabilite mise a jour.",
            "vulnerabilite": mapper.to_external(updated),
        }), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@vulnerabilite_bp.route("/<int:vulnerabilite_id>", methods=["PATCH"])
@expects_json(vulnerabilite_patch_schema)
def patch_vulnerabilite(vulnerabilite_id):
    """
    Modifier partiellement une vulnerabilite
    ---
    tags: [Vulnerabilite]
    parameters:
      - in: path
        name: vulnerabilite_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema: {$ref: '#/definitions/VulnerabiliteUpdate'}
    responses:
      200:
        description: Vulnerabilite modifiee
      404:
        description: Vulnerabilite ou actif introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    dto = request.json
    try:
        updated = service.patch_vulnerabilite(vulnerabilite_id, dto)
        return jsonify({
            "message": "Vulnerabilite partiellement mise a jour.",
            "vulnerabilite": mapper.to_external(updated),
        }), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@vulnerabilite_bp.route("/<int:vulnerabilite_id>", methods=["DELETE"])
def delete_vulnerabilite(vulnerabilite_id):
    """
    Supprimer une vulnerabilite
    ---
    tags: [Vulnerabilite]
    parameters:
      - in: path
        name: vulnerabilite_id
        type: integer
        required: true
    responses:
      200:
        description: Vulnerabilite supprimee
      404:
        description: Vulnerabilite introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    try:
        service.delete_vulnerabilite(vulnerabilite_id)
        return jsonify({"message": "Vulnerabilite supprimee avec succes."}), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404