"""Chargement d'un jeu de donnees de demonstration pour CyberTwin."""
import bcrypt
from sqlalchemy import text

from app import app
from infra.db.database import db
from domain.entities.utilisateur import Utilisateur, Role
from domain.entities.entreprise import Entreprise
from domain.entities.actif import Actif, TypeActif
from domain.entities.vulnerabilite import Vulnerabilite, Criticite

MOT_DE_PASSE = "CyberTwin2024!"

def hacher(mot_de_passe: str) -> str:
    return bcrypt.hashpw(mot_de_passe.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

COMPTES = [
    {"email": "admin@cybertwin.fr",    "nom": "Dupont",  "prenom": "Marie",  "role": Role.ADMIN},
    {"email": "analyste@cybertwin.fr", "nom": "Martin",  "prenom": "Lucas",  "role": Role.ANALYSTE},
    {"email": "lecteur@cybertwin.fr",  "nom": "Bernard", "prenom": "Sophie", "role": Role.LECTEUR},
]


def vul(libelle, criticite, description):
    return {"libelle": libelle, "criticite": criticite, "description": description}


def act(nom, type_actif, description, vulns=()):
    return {"nom": nom, "type_actif": type_actif, "description": description, "vulns": list(vulns)}


def ent(nom, secteur, emp, srv, postes, services, actifs):
    return {
        "nom": nom, "secteur_activite": secteur, "nombre_employes": emp,
        "nombre_serveurs": srv, "nombre_postes_clients": postes,
        "services_exposes": services, "actifs": actifs,
    }



# -Jeu de données
ENTREPRISES = [
    ent("Atelier Boulanger & Fils", "Menuiserie et agencement", 32, 3, 28, ["HTTPS", "RDP"], [
        act("Serveur de devis", TypeActif.SERVEUR_WEB, "Generation des devis clients", [
            vul("Logiciel obsolete", Criticite.ELEVEE, "Serveur non mis a jour depuis 8 mois"),
            vul("Certificat SSL expire", Criticite.MOYENNE, "Certificat HTTPS a renouveler"),
        ]),
        act("Base clients", TypeActif.BASE_DE_DONNEES, "Fichier clients et commandes", [
            vul("Mot de passe faible", Criticite.CRITIQUE, "Compte admin avec mot de passe par defaut"),
        ]),
        act("Poste atelier", TypeActif.POSTE_UTILISATEUR, "Poste partage de l'atelier"),
    ]),
    ent("Cabinet Lefevre Expertise", "Expertise comptable", 21, 2, 19, ["HTTPS", "RDP"], [
        act("Serveur de fichiers", TypeActif.SERVEUR_WEB, "Partage des dossiers comptables", [
            vul("Port SMB expose", Criticite.ELEVEE, "Partage accessible depuis l'exterieur"),
        ]),
        act("Logiciel de paie", TypeActif.BASE_DE_DONNEES, "Donnees de paie et fiscales", [
            vul("Injection SQL potentielle", Criticite.CRITIQUE, "Application non parametree"),
        ]),
        act("Routeur agence", TypeActif.ROUTEUR, "Acces Internet du cabinet"),
    ]),
    ent("Maison Dorval Traiteur", "Restauration et traiteur", 38, 2, 12, ["HTTPS", "SSH", "SMTP"], [
        act("Site de commande", TypeActif.SERVEUR_WEB, "Commandes en ligne et reservations", [
            vul("Faille XSS", Criticite.ELEVEE, "Champ de recherche non assaini"),
        ]),
        act("Base commandes", TypeActif.BASE_DE_DONNEES, "Commandes et paiements", [
            vul("Donnees de paiement non chiffrees", Criticite.CRITIQUE, "Numeros de carte en clair"),
        ]),
        act("Pare-feu boutique", TypeActif.PARE_FEU, "Protection du reseau", [
            vul("Pare-feu mal configure", Criticite.ELEVEE, "Regles trop permissives"),
        ]),
    ]),
    ent("Pharmacie du Centre", "Sante - officine", 14, 2, 10, ["HTTPS", "VPN"], [
        act("Dossier patients", TypeActif.BASE_DE_DONNEES, "Donnees de sante sensibles", [
            vul("Acces non restreint", Criticite.CRITIQUE, "Dossiers accessibles a tout le personnel"),
            vul("Absence de chiffrement", Criticite.ELEVEE, "Donnees non chiffrees au repos"),
        ]),
        act("Logiciel officine", TypeActif.APPLICATION_METIER, "Gestion des ordonnances", [
            vul("Logiciel obsolete", Criticite.MOYENNE, "Application a mettre a jour"),
        ]),
        act("Pare-feu officine", TypeActif.PARE_FEU, "Segmentation du reseau"),
    ]),
    ent("Studio Pixel & Plume", "Agence de communication", 11, 1, 11, ["HTTPS"], [
        act("Site portfolio", TypeActif.SERVEUR_WEB, "Vitrine de l'agence", [
            vul("Plugin vulnerable", Criticite.FAIBLE, "Extension du CMS a mettre a jour"),
        ]),
        act("Poste designer", TypeActif.POSTE_UTILISATEUR, "Station creative"),
    ]),
    ent("SCP Moreau & Associes", "Cabinet d'avocats", 26, 3, 23, ["HTTPS", "VPN", "IMAP"], [
        act("Coffre documentaire", TypeActif.BASE_DE_DONNEES, "Dossiers juridiques confidentiels", [
            vul("Absence de double authentification", Criticite.ELEVEE, "Acces au coffre sans 2FA"),
        ]),
        act("Messagerie securisee", TypeActif.APPLICATION_METIER, "Echanges avocat-client", [
            vul("Chiffrement faible", Criticite.MOYENNE, "Algorithme obsolete"),
        ]),
        act("Pare-feu cabinet", TypeActif.PARE_FEU, "Protection des donnees sensibles", [
            vul("Journalisation absente", Criticite.FAIBLE, "Pas de logs sur le pare-feu"),
        ]),
    ]),
    ent("Transports Vidal Logistique", "Transport et logistique", 78, 5, 45, ["HTTPS", "RDP", "FTP"], [
        act("Suivi des flottes", TypeActif.APPLICATION_METIER, "Geolocalisation des camions", [
            vul("Acces RDP non restreint", Criticite.ELEVEE, "Bureau a distance ouvert sur Internet"),
        ]),
        act("Serveur EDI", TypeActif.SERVEUR_WEB, "Echanges de donnees logistiques", [
            vul("Mot de passe faible", Criticite.MOYENNE, "Compte EDI partage"),
        ]),
        act("Poste exploitation", TypeActif.POSTE_UTILISATEUR, "Planning des livraisons"),
    ]),
    ent("Menuiserie Alpine Bois", "Industrie du bois", 54, 4, 30, ["HTTPS", "VPN", "SSH"], [
        act("Supervision atelier", TypeActif.APPLICATION_METIER, "Pilotage des machines", [
            vul("Reseau non segmente", Criticite.ELEVEE, "IT et machines sur le meme reseau"),
        ]),
        act("Base RH", TypeActif.BASE_DE_DONNEES, "Donnees des employes", [
            vul("Sauvegarde non testee", Criticite.MOYENNE, "Restauration jamais verifiee"),
        ]),
        act("Routeur site", TypeActif.ROUTEUR, "Interconnexion des ateliers"),
    ]),
]


TABLES = ["vulnerabilite", "actif", "analyse_historique", "notification", "entreprise", "utilisateur"]


def vider_tables():
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    for table in TABLES:
        db.session.execute(text(f"TRUNCATE TABLE {table}"))
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    db.session.commit()


def inserer():
    for c in COMPTES:
        db.session.add(Utilisateur(
            email=c["email"], mot_de_passe=hacher(MOT_DE_PASSE),
            nom=c["nom"], prenom=c["prenom"], role=c["role"],
        ))

    nb_actifs = nb_vulns = 0
    for e in ENTREPRISES:
        entreprise = Entreprise(
            nom=e["nom"], secteur_activite=e["secteur_activite"],
            nombre_employes=e["nombre_employes"], nombre_serveurs=e["nombre_serveurs"],
            nombre_postes_clients=e["nombre_postes_clients"],
            services_exposes=e["services_exposes"],
        )
        db.session.add(entreprise)
        db.session.flush()

        for a in e["actifs"]:
            actif = Actif(
                entreprise_id=entreprise.id, nom=a["nom"],
                type_actif=a["type_actif"], description=a["description"],
            )
            db.session.add(actif)
            db.session.flush()
            nb_actifs += 1

            for v in a["vulns"]:
                db.session.add(Vulnerabilite(
                    actif_id=actif.id, libelle=v["libelle"],
                    criticite=v["criticite"], description=v["description"],
                ))
                nb_vulns += 1

    db.session.commit()
    return nb_actifs, nb_vulns


def main():
    with app.app_context():
        db.create_all()
        vider_tables()
        nb_actifs, nb_vulns = inserer()

    print("Jeu de donnees charge avec succes :")
    print(f"  - {len(COMPTES)} compte(s) (mot de passe : {MOT_DE_PASSE})")
    print(f"  - {len(ENTREPRISES)} entreprise(s), {nb_actifs} actif(s), {nb_vulns} vulnerabilite(s)")


if __name__ == "__main__":
    main()