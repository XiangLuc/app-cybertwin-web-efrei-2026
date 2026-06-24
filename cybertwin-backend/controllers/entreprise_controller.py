"""
Controller de l'entreprise.

"""
from flask import Blueprint, jsonify, request
from flask_expects_json import expects_json

from utils.exceptions import ConflictError, NotFoundError
from shared.modules.entreprise_module import entreprise_module
from utils.security import roles_required
from utils.notification import notifier_action
from domain.entities.notification import TypeNotification

service = entreprise_module["service"]
mapper = entreprise_module["dto_mapper"]
entreprise_schema = entreprise_module["dto_schema"]
entreprise_patch_schema = entreprise_module["dto_patch_schema"]

entreprise_bp = Blueprint("entreprise_bp", __name__)


@entreprise_bp.route("", methods=["GET"])
def get_entreprises():
    """
    Lister les entreprises
    ---
    tags: [Entreprise]
    responses:
      200:
        description: Liste des entreprises
        schema:
          type: array
          items: {$ref: '#/definitions/Entreprise'}
    """
    entreprises = service.get_all()
    return jsonify(mapper.to_external_list(entreprises)), 200


@entreprise_bp.route("<int:entreprise_id>", methods=["GET"])
def get_entreprise(entreprise_id):
    """
    Consulter une entreprise
    ---
    tags: [Entreprise]
    parameters:
      - in: path
        name: entreprise_id
        type: string
        required: true
    responses:
      200:
        description: Fiche de l'entreprise
        schema: {$ref: '#/definitions/Entreprise'}
      404:
        description: Entreprise introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    try:
        entreprise = service.get_by_id(entreprise_id)
        return jsonify(mapper.to_external(entreprise)), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@entreprise_bp.route("", methods=["POST"])
@notifier_action("Entreprise creee", "Une entreprise a ete creee.", TypeNotification.SUCCES)
@expects_json(entreprise_schema)
def create_entreprise():
    """
    Creer une entreprise
    ---
    tags: [Entreprise]
    parameters:
      - in: body
        name: body
        required: true
        schema: {$ref: '#/definitions/EntrepriseCreate'}
    responses:
      201:
        description: Entreprise creee
      409:
        description: Nom deja utilise
        schema: {$ref: '#/definitions/Erreur'}
      400:
        description: Donnees invalides
        schema: {$ref: '#/definitions/Erreur'}
    """
    dto = request.json
    try:
        created = service.create_entreprise(dto)
        return jsonify({
            "message": "Entreprise creee avec succes.",
            "entreprise": mapper.to_external(created),
        }), 201
    except ConflictError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@entreprise_bp.route("<int:entreprise_id>", methods=["PUT"])
@expects_json(entreprise_schema)
def update_entreprise(entreprise_id):
    """
    Remplacer une entreprise (mise a jour complete)
    ---
    tags: [Entreprise]
    parameters:
      - in: path
        name: entreprise_id
        type: string
        required: true
      - in: body
        name: body
        required: true
        schema: {$ref: '#/definitions/EntrepriseCreate'}
    responses:
      200:
        description: Entreprise mise a jour
      404:
        description: Entreprise introuvable
        schema: {$ref: '#/definitions/Erreur'}
      409:
        description: Nom deja utilise
        schema: {$ref: '#/definitions/Erreur'}
    """
    dto = request.json
    try:
        updated = service.update_entreprise(entreprise_id, dto)
        return jsonify({
            "message": "Entreprise mise a jour.",
            "entreprise": mapper.to_external(updated),
        }), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except ConflictError as e:
        return jsonify({"error": str(e)}), 409


@entreprise_bp.route("<int:entreprise_id>", methods=["PATCH"])
@expects_json(entreprise_patch_schema)
def patch_entreprise(entreprise_id):
    """
    Modifier partiellement une entreprise
    ---
    tags: [Entreprise]
    parameters:
      - in: path
        name: entreprise_id
        type: string
        required: true
      - in: body
        name: body
        required: true
        schema: {$ref: '#/definitions/EntrepriseUpdate'}
    responses:
      200:
        description: Entreprise modifiee
      404:
        description: Entreprise introuvable
        schema: {$ref: '#/definitions/Erreur'}
      409:
        description: Nom deja utilise
        schema: {$ref: '#/definitions/Erreur'}
    """
    dto = request.json
    try:
        updated = service.patch_entreprise(entreprise_id, dto)
        return jsonify({
            "message": "Entreprise partiellement mise a jour.",
            "entreprise": mapper.to_external(updated),
        }), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except ConflictError as e:
        return jsonify({"error": str(e)}), 409


@entreprise_bp.route("<int:entreprise_id>", methods=["DELETE"])
@roles_required("ADMIN", "ANALYSTE") 
@notifier_action("Entreprise supprimee", "Une entreprise a ete supprimee.", TypeNotification.ALERTE)
def delete_entreprise(entreprise_id):
    """
    Supprimer une entreprise
    ---
    tags: [Entreprise]
    parameters:
      - in: path
        name: entreprise_id
        type: string
        required: true
    responses:
      200:
        description: Entreprise supprimee
      404:
        description: Entreprise introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    try:
        service.delete_entreprise(entreprise_id)
        return jsonify({"message": "Entreprise supprimee avec succes."}), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404