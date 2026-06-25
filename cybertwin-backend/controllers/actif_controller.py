"""
Controller de l'actif.

Endpoints conformes au cahier des charges : GET /assets, POST /assets,
PUT /assets/:id, DELETE /assets/:id (+ GET /assets/:id et PATCH en bonus).
Validation par flask_expects_json, doc Swagger par docstrings.
"""
from flask import Blueprint, jsonify, request
from flask_expects_json import expects_json

from utils.exceptions import NotFoundError
from shared.modules.actif_module import actif_module

service = actif_module["service"]
mapper = actif_module["dto_mapper"]
actif_schema = actif_module["dto_schema"]
actif_patch_schema = actif_module["dto_patch_schema"]

actif_bp = Blueprint("actif_bp", __name__)


@actif_bp.route("", methods=["GET"])
def get_actifs():
    """
    Lister les actifs (filtre optionnel par entreprise)
    ---
    tags: [Actif]
    parameters:
      - in: query
        name: entreprise_id
        type: integer
        required: false
        description: Filtrer les actifs d'une entreprise
    responses:
      200:
        description: Liste des actifs
        schema:
          type: array
          items: {$ref: '#/definitions/Actif'}
      404:
        description: Entreprise filtre introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    entreprise_id = request.args.get("entreprise_id", type=int)
    try:
        actifs = service.get_all(entreprise_id)
        return jsonify(mapper.to_external_list(actifs)), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@actif_bp.route("/<int:actif_id>", methods=["GET"])
def get_actif(actif_id):
    """
    Consulter un actif
    ---
    tags: [Actif]
    parameters:
      - in: path
        name: actif_id
        type: integer
        required: true
    responses:
      200:
        description: Fiche de l'actif
        schema: {$ref: '#/definitions/Actif'}
      404:
        description: Actif introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    try:
        actif = service.get_by_id(actif_id)
        return jsonify(mapper.to_external(actif)), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@actif_bp.route("", methods=["POST"])
@expects_json(actif_schema)
def create_actif():
    """
    Ajouter un actif
    ---
    tags: [Actif]
    parameters:
      - in: body
        name: body
        required: true
        schema: {$ref: '#/definitions/ActifCreate'}
    responses:
      201:
        description: Actif cree
      404:
        description: Entreprise liee introuvable
        schema: {$ref: '#/definitions/Erreur'}
      400:
        description: Donnees invalides
        schema: {$ref: '#/definitions/Erreur'}
    """
    dto = request.json
    try:
        created = service.create_actif(dto)
        return jsonify({
            "message": "Actif cree avec succes.",
            "actif": mapper.to_external(created),
        }), 201
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@actif_bp.route("/<int:actif_id>", methods=["PUT"])
@expects_json(actif_schema)
def update_actif(actif_id):
    """
    Remplacer un actif (mise a jour complete)
    ---
    tags: [Actif]
    parameters:
      - in: path
        name: actif_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema: {$ref: '#/definitions/ActifCreate'}
    responses:
      200:
        description: Actif mis a jour
      404:
        description: Actif ou entreprise introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    dto = request.json
    try:
        updated = service.update_actif(actif_id, dto)
        return jsonify({
            "message": "Actif mis a jour.",
            "actif": mapper.to_external(updated),
        }), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@actif_bp.route("/<int:actif_id>", methods=["PATCH"])
@expects_json(actif_patch_schema)
def patch_actif(actif_id):
    """
    Modifier partiellement un actif
    ---
    tags: [Actif]
    parameters:
      - in: path
        name: actif_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema: {$ref: '#/definitions/ActifUpdate'}
    responses:
      200:
        description: Actif modifie
      404:
        description: Actif ou entreprise introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    dto = request.json
    try:
        updated = service.patch_actif(actif_id, dto)
        return jsonify({
            "message": "Actif partiellement mis a jour.",
            "actif": mapper.to_external(updated),
        }), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@actif_bp.route("/<int:actif_id>", methods=["DELETE"])
def delete_actif(actif_id):
    """
    Supprimer un actif
    ---
    tags: [Actif]
    parameters:
      - in: path
        name: actif_id
        type: integer
        required: true
    responses:
      200:
        description: Actif supprime
      404:
        description: Actif introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    try:
        service.delete_actif(actif_id)
        return jsonify({"message": "Actif supprime avec succes."}), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404