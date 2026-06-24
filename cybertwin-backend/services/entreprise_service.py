"""
Service de l'entreprise (logique metier).

"""
from utils.exceptions import ConflictError, NotFoundError
from domain.repositories.entreprise_repository import EntrepriseRepository
from shared.dto.mappers.entreprise_dto_mapper import EntrepriseDTOMapper

CHAMPS = [
    "nom",
    "secteur_activite",
    "nombre_employes",
    "nombre_serveurs",
    "nombre_postes_clients",
    "services_exposes",
]


class EntrepriseService:
    def __init__(self, repository: EntrepriseRepository, mapper: EntrepriseDTOMapper):
        self.repository = repository
        self.mapper = mapper

    def get_all(self):
        return self.repository.find_all()

    def get_by_id(self, entreprise_id: str):
        entreprise = self.repository.find_by_id(entreprise_id)
        if entreprise is None:
            raise NotFoundError(
                f"Aucune entreprise trouvee avec l'identifiant '{entreprise_id}'."
            )
        return entreprise

    def create_entreprise(self, dto: dict):
        if self.repository.exists_by_nom(dto["nom"]):
            raise ConflictError(f"Une entreprise nommee '{dto['nom']}' existe deja.")
        entreprise = self.mapper.to_domain(dto)
        return self.repository.create_entreprise(entreprise)

    def update_entreprise(self, entreprise_id: str, dto: dict):
        """Remplacement complet (PUT) : tous les champs requis (valides en amont)."""
        entreprise = self.get_by_id(entreprise_id)
        self._check_nom_unique(dto, entreprise)
        for champ in CHAMPS:
            if champ == "services_exposes":
                setattr(entreprise, champ, dto.get("services_exposes", []))
            else:
                setattr(entreprise, champ, dto[champ])
        return self.repository.update_entreprise(entreprise)

    def patch_entreprise(self, entreprise_id: str, dto: dict):
        """Modification partielle (PATCH) : seuls les champs fournis sont modifies."""
        entreprise = self.get_by_id(entreprise_id)
        self._check_nom_unique(dto, entreprise)
        for champ in CHAMPS:
            if champ in dto:
                setattr(entreprise, champ, dto[champ])
        return self.repository.update_entreprise(entreprise)

    def delete_entreprise(self, entreprise_id: str):
        entreprise = self.get_by_id(entreprise_id)
        self.repository.delete_entreprise(entreprise)

    def _check_nom_unique(self, dto: dict, entreprise):
        nouveau_nom = dto.get("nom")
        if nouveau_nom and nouveau_nom != entreprise.nom:
            if self.repository.exists_by_nom(nouveau_nom, exclude_id=entreprise.id):
                raise ConflictError(
                    f"Une entreprise nommee '{nouveau_nom}' existe deja."
                )