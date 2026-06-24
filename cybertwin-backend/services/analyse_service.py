"""
Service d'analyse

"""
from domain.entities.vulnerabilite import Criticite, POIDS_CRITICITE
from utils.exceptions import NotFoundError

# Constantes du moteur d'analyse
POIDS_EXPOSITION = 2   # par service expose sur Internet
POIDS_ACTIF = 1        # par actif 
SEUIL_FAIBLE = 10      # score <= 10 = FAIBLE
SEUIL_MOYEN = 25       # 11 <= score <= 25 -> MOYEN ; au-dela -> ELEVE


class AnalyseService:
    def __init__(self, entreprise_repository, actif_repository,
                 vulnerabilite_repository, entreprise_mapper, actif_mapper,
                 vulnerabilite_mapper):
        self.entreprise_repository = entreprise_repository
        self.actif_repository = actif_repository
        self.vulnerabilite_repository = vulnerabilite_repository
        self.entreprise_mapper = entreprise_mapper
        self.actif_mapper = actif_mapper
        self.vulnerabilite_mapper = vulnerabilite_mapper

    def calculer_risque(self, entreprise_id: int) -> dict:
        entreprise = self._require_entreprise(entreprise_id)
        actifs = self.actif_repository.find_all(entreprise_id)
        vulnerabilites = self.vulnerabilite_repository.find_by_entreprise(entreprise_id)
        return self._analyser(entreprise, actifs, vulnerabilites)

    def dashboard(self, entreprise_id: int) -> dict:
        entreprise = self._require_entreprise(entreprise_id)
        actifs = self.actif_repository.find_all(entreprise_id)
        vulnerabilites = self.vulnerabilite_repository.find_by_entreprise(entreprise_id)
        analyse = self._analyser(entreprise, actifs, vulnerabilites)

        repartition_actifs = {}
        for actif in actifs:
            cle = actif.type_actif.value
            repartition_actifs[cle] = repartition_actifs.get(cle, 0) + 1

        repartition_criticites = {}
        for vuln in vulnerabilites:
            cle = vuln.criticite.value
            repartition_criticites[cle] = repartition_criticites.get(cle, 0) + 1

        return {
            "entreprise_id": entreprise.id,
            "nombre_total_actifs": len(actifs),
            "nombre_total_vulnerabilites": len(vulnerabilites),
            "repartition_actifs": repartition_actifs,
            "repartition_criticites": repartition_criticites,
            "score_risque_global": analyse["score"],
            "niveau_risque": analyse["niveau_risque"],
        }

    def rapport(self, entreprise_id: int) -> dict:
        entreprise = self._require_entreprise(entreprise_id)
        actifs = self.actif_repository.find_all(entreprise_id)
        vulnerabilites = self.vulnerabilite_repository.find_by_entreprise(entreprise_id)
        analyse = self._analyser(entreprise, actifs, vulnerabilites)

        return {
            "entreprise": self.entreprise_mapper.to_external(entreprise),
            "inventaire_actifs": self.actif_mapper.to_external_list(actifs),
            "vulnerabilites_detectees": self.vulnerabilite_mapper.to_external_list(vulnerabilites),
            "analyse_risque": {
                "score": analyse["score"],
                "niveau_risque": analyse["niveau_risque"],
                "details": analyse["details"],
            },
            "recommandations": analyse["recommandations"],
        }

    def _analyser(self, entreprise, actifs, vulnerabilites) -> dict:
        score_vulnerabilites = sum(POIDS_CRITICITE[v.criticite] for v in vulnerabilites)
        score_exposition = len(entreprise.services_exposes or []) * POIDS_EXPOSITION
        score_actifs = len(actifs) * POIDS_ACTIF
        score_total = score_vulnerabilites + score_exposition + score_actifs
        niveau = self._niveau_risque(score_total)

        return {
            "entreprise_id": entreprise.id,
            "nombre_actifs": len(actifs),
            "nombre_vulnerabilites": len(vulnerabilites),
            "score": score_total,
            "niveau_risque": niveau,
            "details": {
                "score_vulnerabilites": score_vulnerabilites,
                "score_exposition": score_exposition,
                "score_actifs": score_actifs,
            },
            "recommandations": self._recommandations(entreprise, actifs, vulnerabilites, niveau),
        }

    @staticmethod
    def _niveau_risque(score: int) -> str:
        if score <= SEUIL_FAIBLE:
            return "FAIBLE"
        if score <= SEUIL_MOYEN:
            return "MOYEN"
        return "ELEVE"

    @staticmethod
    def _recommandations(entreprise, actifs, vulnerabilites, niveau) -> list:
        reco = []
        nb_critique = sum(1 for v in vulnerabilites if v.criticite == Criticite.CRITIQUE)
        nb_elevee = sum(1 for v in vulnerabilites if v.criticite == Criticite.ELEVEE)
        nb_services = len(entreprise.services_exposes or [])

        if not actifs:
            reco.append(
                "Commencez par recenser votre parc informatique : aucun actif n'est "
                "inventorie, l'analyse ne peut donc pas etre representative."
            )

        if nb_critique:
            reco.append(
                f"Priorite absolue : corriger sans delai les {nb_critique} vulnerabilite(s) "
                "critique(s) (correctifs de securite, changement des mots de passe par defaut)."
            )
        if nb_elevee:
            reco.append(
                f"Planifier sous 30 jours la correction des {nb_elevee} vulnerabilite(s) "
                "de criticite elevee (mises a jour, durcissement des configurations)."
            )

        if nb_services >= 5:
            reco.append(
                "Surface d'exposition tres elevee : fermez les services non indispensables, "
                "placez-les derriere un VPN et renforcez les regles du pare-feu."
            )
        elif nb_services >= 3:
            reco.append(
                "Reduire l'exposition Internet : limitez les services accessibles publiquement "
                "et verifiez la configuration du pare-feu."
            )

        if actifs and len(vulnerabilites) > 2 * len(actifs):
            reco.append(
                "Le nombre de vulnerabilites est eleve au regard du parc : mettez en place "
                "un processus regulier de detection et de correction (scan + suivi)."
            )

        reco.append(
            "Activez des sauvegardes automatiques et testees regulierement (regle 3-2-1) "
            "et l'authentification a deux facteurs sur les acces sensibles."
        )

        if niveau == "ELEVE":
            reco.append(
                "Niveau de risque ELEVE : etablissez un plan de remediation formalise avec "
                "un suivi mensuel des indicateurs de securite."
            )
        elif niveau == "MOYEN":
            reco.append(
                "Niveau de risque MOYEN : corrigez les points ouverts et instaurez une "
                "revue de securite trimestrielle."
            )
        else:
            reco.append(
                "Niveau de risque MAITRISE : maintenez les bonnes pratiques et poursuivez "
                "la veille sur les nouvelles menaces."
            )

        if not vulnerabilites and actifs:
            reco.insert(
                0,
                "Aucune vulnerabilite enregistree : excellent point. Maintenez une veille "
                "de securite reguliere pour que cela perdure.",
            )

        return reco

    def _require_entreprise(self, entreprise_id: int):
        entreprise = self.entreprise_repository.find_by_id(entreprise_id)
        if entreprise is None:
            raise NotFoundError(
                f"Aucune entreprise trouvee avec l'identifiant '{entreprise_id}'."
            )
        return entreprise