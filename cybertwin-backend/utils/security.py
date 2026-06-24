"""
Decorateur de securite pour proteger les routes par role (JWT).

Usage :
    @bp.route("...")
    @roles_required("ADMIN", "ANALYSTE")   # roles autorises
    def vue(): ...

    @roles_required()   # sans argument : n'importe quel utilisateur connecte

Il faut mettre @roles_required au-dessus de @expects_json.
"""
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required


def roles_required(*roles_autorises):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            role = get_jwt().get("role")
            if roles_autorises and role not in roles_autorises:
                return jsonify({"error": "Acces refuse : role insuffisant."}), 403
            return fn(*args, **kwargs)
        return jwt_required()(wrapper)
    return decorator