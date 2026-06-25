"""
Service de l'actif (logique metier).

"""
from domain.entities.actif import TypeActif
from utils.exceptions import NotFoundError
from domain.repositories.actif_repository import ActifRepository
from domain.repositories.entreprise_repository import EntrepriseRepository
from shared.dto.mappers.actif_dto_mapper import ActifDTOMapper


class ActifService:
    def __init__(self, repository: ActifRepository,
                 entreprise_repository: EntrepriseRepository,
                 mapper: ActifDTOMapper):
        self.repository = repository
        self.entreprise_repository = entreprise_repository
        self.mapper = mapper

    def get_all(self, entreprise_id: int = None):
        if entreprise_id is not None:
            self._require_entreprise(entreprise_id)
        return self.repository.find_all(entreprise_id)

    def get_by_id(self, actif_id: int):
        actif = self.repository.find_by_id(actif_id)
        if actif is None:
            raise NotFoundError(
                f"Aucun actif trouve avec l'identifiant '{actif_id}'."
            )
        return actif

    def create_actif(self, dto: dict):
        self._require_entreprise(dto["entreprise_id"])
        actif = self.mapper.to_domain(dto)
        return self.repository.create_actif(actif)

    def update_actif(self, actif_id: int, dto: dict):
        """Remplacement complet (PUT)."""
        actif = self.get_by_id(actif_id)
        self._require_entreprise(dto["entreprise_id"])
        actif.entreprise_id = dto["entreprise_id"]
        actif.nom = dto["nom"]
        actif.type_actif = TypeActif(dto["type_actif"])
        actif.description = dto.get("description")
        return self.repository.update_actif(actif)

    def patch_actif(self, actif_id: int, dto: dict):
        """Modification partielle (PATCH)."""
        actif = self.get_by_id(actif_id)
        if "entreprise_id" in dto:
            self._require_entreprise(dto["entreprise_id"])
        for champ in ["entreprise_id", "nom", "type_actif", "description"]:
            if champ in dto:
                if champ == "type_actif":
                    actif.type_actif = TypeActif(dto[champ])
                else:
                    setattr(actif, champ, dto[champ])
        return self.repository.update_actif(actif)

    def delete_actif(self, actif_id: int):
        actif = self.get_by_id(actif_id)
        self.repository.delete_actif(actif)

    def _require_entreprise(self, entreprise_id: int):
        if self.entreprise_repository.find_by_id(entreprise_id) is None:
            raise NotFoundError(
                f"Aucune entreprise trouvee avec l'identifiant '{entreprise_id}'."
            )