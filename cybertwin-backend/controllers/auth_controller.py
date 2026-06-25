"""
Controller d'authentification (/auth).

  - POST /auth/register        inscription publique
  - POST /auth/login           connexion jwt
  - GET  /auth/me              profil de l'utilisateur connecte
  - GET  /auth/users           liste des utilisateurs        (ADMIN)
  - POST /auth/users           creer un utilisateur          (ADMIN)
  - DELETE /auth/users/<id>    supprimer un utilisateur      (ADMIN)
"""
from flask import Blueprint, jsonify, request
from flask_expects_json import expects_json
from flask_jwt_extended import get_jwt_identity

from utils.exceptions import (
    ConflictError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)
from shared.modules.auth_module import auth_module
from utils.security import roles_required

service = auth_module["service"]
mapper = auth_module["dto_mapper"]
register_schema = auth_module["register_schema"]
login_schema = auth_module["login_schema"]
change_password_schema = auth_module["change_password_schema"]
change_role_schema = auth_module["change_role_schema"]


auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/register", methods=["POST"])
@expects_json(register_schema)
def register():
    """
    Inscription d'un utilisateur
    ---
    tags: [Auth]
    parameters:
      - in: body
        name: body
        required: true
        schema: {$ref: '#/definitions/Register'}
    responses:
      201:
        description: Utilisateur cree
      400:
        description: Mot de passe non conforme ou role invalide
        schema: {$ref: '#/definitions/Erreur'}
      409:
        description: Email deja utilise
        schema: {$ref: '#/definitions/Erreur'}
    """
    dto = request.json
    try:
        created = service.inscrire(dto)
        return jsonify({
            "message": "Utilisateur cree avec succes.",
            "utilisateur": mapper.to_external(created),
        }), 201
    except ValidationError as e:
        return jsonify({"error": e.message, "details": e.details}), 400
    except ConflictError as e:
        return jsonify({"error": str(e)}), 409


@auth_bp.route("/login", methods=["POST"])
@expects_json(login_schema)
def login():
    """
    Connexion (renvoie un jeton JWT)
    ---
    tags: [Auth]
    parameters:
      - in: body
        name: body
        required: true
        schema: {$ref: '#/definitions/Login'}
    responses:
      200:
        description: Jeton JWT + role
      401:
        description: Identifiants incorrects
        schema: {$ref: '#/definitions/Erreur'}
    """
    data = request.json
    try:
        resultat = service.connecter(data["email"], data["mot_de_passe"])
        return jsonify(resultat), 200
    except UnauthorizedError as e:
        return jsonify({"error": str(e)}), 401


@auth_bp.route("/me", methods=["GET"])
@roles_required()
def me():
    """
    Profil de l'utilisateur connecte
    ---
    tags: [Auth]
    security:
      - Bearer: []
    responses:
      200:
        description: Profil
        schema: {$ref: '#/definitions/Utilisateur'}
      401:
        description: Non authentifie
    """
    utilisateur = service.get_by_id(int(get_jwt_identity()))
    return jsonify(mapper.to_external(utilisateur)), 200


@auth_bp.route("/users", methods=["GET"])
@roles_required("ADMIN")
def list_users():
    """
    Lister les utilisateurs (ADMIN)
    ---
    tags: [Auth]
    security:
      - Bearer: []
    responses:
      200:
        description: Liste des utilisateurs
      403:
        description: Role insuffisant
        schema: {$ref: '#/definitions/Erreur'}
    """
    return jsonify(mapper.to_external_list(service.lister())), 200


@auth_bp.route("/users", methods=["POST"])
@roles_required("ADMIN")
@expects_json(register_schema)
def create_user():
    """
    Creer un utilisateur, tous roles (ADMIN)
    ---
    tags: [Auth]
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema: {$ref: '#/definitions/Register'}
    responses:
      201:
        description: Utilisateur cree
      400:
        description: Donnees invalides
        schema: {$ref: '#/definitions/Erreur'}
      409:
        description: Email deja utilise
        schema: {$ref: '#/definitions/Erreur'}
    """
    dto = request.json
    try:
        created = service.creer_par_admin(dto)
        return jsonify({
            "message": "Utilisateur cree avec succes.",
            "utilisateur": mapper.to_external(created),
        }), 201
    except ValidationError as e:
        return jsonify({"error": e.message, "details": e.details}), 400
    except ConflictError as e:
        return jsonify({"error": str(e)}), 409


@auth_bp.route("/users/<int:utilisateur_id>", methods=["DELETE"])
@roles_required("ADMIN")
def delete_user(utilisateur_id):
    """
    Supprimer un utilisateur (ADMIN)
    ---
    tags: [Auth]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: utilisateur_id
        type: integer
        required: true
    responses:
      200:
        description: Utilisateur supprime
      404:
        description: Utilisateur introuvable
        schema: {$ref: '#/definitions/Erreur'}
    """
    try:
        service.supprimer(utilisateur_id)
        return jsonify({"message": "Utilisateur supprime avec succes."}), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
    

@auth_bp.route("/me/password", methods=["PATCH"])
@roles_required()
@expects_json(change_password_schema)
def changer_mon_mot_de_passe():
    """
    Changer son propre mot de passe
    ---
    tags: [Auth]
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [ancien_mot_de_passe, nouveau_mot_de_passe]
          properties:
            ancien_mot_de_passe: {type: string}
            nouveau_mot_de_passe: {type: string}
    responses:
      200: {description: Mot de passe modifie}
      400: {description: Nouveau mot de passe non conforme, schema: {$ref: '#/definitions/Erreur'}}
      401: {description: Ancien mot de passe incorrect, schema: {$ref: '#/definitions/Erreur'}}
    """
    dto = request.json
    try:
        service.changer_mot_de_passe(
            int(get_jwt_identity()), 
            dto["ancien_mot_de_passe"], 
            dto["nouveau_mot_de_passe"]
        )
        return jsonify({"message": "Mot de passe modifie avec succes."}), 200
    except UnauthorizedError as e:
        return jsonify({"error": str(e)}), 401
    except ValidationError as e:
        return jsonify({"error": str(e), "details": getattr(e, 'details', None)}), 400


@auth_bp.route("/users/<int:utilisateur_id>/role", methods=["PATCH"])
@roles_required("ADMIN")
@expects_json(change_role_schema)
def changer_role_utilisateur(utilisateur_id):
    """
    Changer le role d'un utilisateur (ADMIN)
    ---
    tags: [Auth]
    security:
      - Bearer: []
    parameters:
      - in: path
        name: utilisateur_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [role]
          properties:
            role: {type: string, enum: [ADMIN, ANALYSTE, LECTEUR]}
    responses:
      200: {description: Role modifie}
      400: {description: Operation invalide, schema: {$ref: '#/definitions/Erreur'}}
      404: {description: Utilisateur introuvable, schema: {$ref: '#/definitions/Erreur'}}
    """
    dto = request.json
    try:
        updated = service.changer_role(utilisateur_id, dto["role"], int(get_jwt_identity()))
        return jsonify({
            "message": "Role mis a jour.", 
            "utilisateur": mapper.to_external(updated)
        }), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404