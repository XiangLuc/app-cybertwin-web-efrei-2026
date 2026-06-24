"""
Decorateur de notification d'action.

Pose sur une route d'ecriture, il cree une notification destinee a
l'utilisateur courant lorsque l'action reussit (reponse HTTP 2xx). A placer
SOUS @roles_required (pour disposer de l'identite JWT) et AU-DESSUS de
@expects_json (pour ne notifier qu'apres validation reussie).
"""
from functools import wraps

from flask_jwt_extended import get_jwt_identity

from domain.entities.notification import TypeNotification
from shared.modules.notification_module import notification_module

_service = notification_module["service"]


def notifier_action(titre, message=None, type=TypeNotification.INFO):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            resultat = fn(*args, **kwargs)
            statut = resultat[1] if isinstance(resultat, tuple) else getattr(resultat, "status_code", 200)
            if 200 <= statut < 300:
                try:
                    utilisateur_id = int(get_jwt_identity())
                    _service.notifier(utilisateur_id, titre, message or titre, type)
                except Exception:
                    pass  # une notification ne doit jamais faire echouer l'action
            return resultat
        return wrapper
    return decorator