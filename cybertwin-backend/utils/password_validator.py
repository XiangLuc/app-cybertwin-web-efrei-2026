"""
Validation de la robustesse d'un mot de passe (en se basant sur la recommandations du CNIL).

"""
import re

LONGUEUR_MIN = 12

# (pattern regex, message si non respecte)
REGLES = [
    (r"[A-Z]", "au moins une majuscule"),
    (r"[a-z]", "au moins une minuscule"),
    (r"[0-9]", "au moins un chiffre"),
    (r"[^A-Za-z0-9]", "au moins un caractere special (ponctuation, $, #, ...)"),
]


def valider_mot_de_passe(mot_de_passe: str) -> list:
    erreurs = []
    if not isinstance(mot_de_passe, str) or len(mot_de_passe) < LONGUEUR_MIN:
        erreurs.append(f"au moins {LONGUEUR_MIN} caracteres")
    for pattern, message in REGLES:
        if not re.search(pattern, mot_de_passe or ""):
            erreurs.append(message)
    return erreurs


def est_valide(mot_de_passe: str) -> bool:
    return len(valider_mot_de_passe(mot_de_passe)) == 0