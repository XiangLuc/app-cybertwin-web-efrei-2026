"""
Service de la vulnerabilite (logique metier).

Verifie l'existence de l'actif lie (integrite de la cle etrangere) avant toute
creation / mise a jour.
"""
from domain.entities.vulnerabilite import Criticite
from utils.exceptions import NotFoundError
from domain.repositories.actif_repository import ActifRepository
from domain.repositories.vulnerabilite_repository import VulnerabiliteRepository
from shared.dto.mappers.vulnerabilite_dto_mapper import VulnerabiliteDTOMapper


class VulnerabiliteService:
    def __init__(self, repository: VulnerabiliteRepository,
                 actif_repository: ActifRepository,
                 mapper: VulnerabiliteDTOMapper):
        self.repository = repository
        self.actif_repository = actif_repository
        self.mapper = mapper

    def get_all(self, actif_id: int = None, entreprise_id: int = None):
        if entreprise_id is not None:
            return self.repository.find_by_entreprise(entreprise_id)
        if actif_id is not None:
            self._require_actif(actif_id)
        return self.repository.find_all(actif_id)

    def get_by_id(self, vulnerabilite_id: int):
        vulnerabilite = self.repository.find_by_id(vulnerabilite_id)
        if vulnerabilite is None:
            raise NotFoundError(
                f"Aucune vulnerabilite trouvee avec l'identifiant '{vulnerabilite_id}'."
            )
        return vulnerabilite

    def create_vulnerabilite(self, dto: dict):
        self._require_actif(dto["actif_id"])
        vulnerabilite = self.mapper.to_domain(dto)
        return self.repository.create_vulnerabilite(vulnerabilite)

    def update_vulnerabilite(self, vulnerabilite_id: int, dto: dict):
        """Remplacement complet (PUT)."""
        vulnerabilite = self.get_by_id(vulnerabilite_id)
        self._require_actif(dto["actif_id"])
        vulnerabilite.actif_id = dto["actif_id"]
        vulnerabilite.libelle = dto["libelle"]
        vulnerabilite.criticite = Criticite(dto["criticite"])
        vulnerabilite.description = dto.get("description")
        return self.repository.update_vulnerabilite(vulnerabilite)

    def patch_vulnerabilite(self, vulnerabilite_id: int, dto: dict):
        """Modification partielle (PATCH)."""
        vulnerabilite = self.get_by_id(vulnerabilite_id)
        if "actif_id" in dto:
            self._require_actif(dto["actif_id"])
        for champ in ["actif_id", "libelle", "criticite", "description"]:
            if champ in dto:
                if champ == "criticite":
                    vulnerabilite.criticite = Criticite(dto[champ])
                else:
                    setattr(vulnerabilite, champ, dto[champ])
        return self.repository.update_vulnerabilite(vulnerabilite)

    def delete_vulnerabilite(self, vulnerabilite_id: int):
        vulnerabilite = self.get_by_id(vulnerabilite_id)
        self.repository.delete_vulnerabilite(vulnerabilite)

    def _require_actif(self, actif_id: int):
        if self.actif_repository.find_by_id(actif_id) is None:
            raise NotFoundError(
                f"Aucun actif trouve avec l'identifiant '{actif_id}'."
            )