"""Mapper DTO <-> entite Entreprise (herite de BaseMapper)."""
from domain.entities.entreprise import Entreprise
from domain.kernel.mapper import BaseMapper


class EntrepriseDTOMapper(BaseMapper[Entreprise, dict]):
    def to_domain(self, dto: dict) -> Entreprise:
        return Entreprise.create(
            nom=dto["nom"],
            secteur_activite=dto["secteur_activite"],
            nombre_employes=dto["nombre_employes"],
            nombre_serveurs=dto["nombre_serveurs"],
            nombre_postes_clients=dto["nombre_postes_clients"],
            services_exposes=dto.get("services_exposes", []),
        )

    def to_external(self, entreprise: Entreprise) -> dict:
        return {
            "id": entreprise.id,
            "nom": entreprise.nom,
            "secteur_activite": entreprise.secteur_activite,
            "nombre_employes": entreprise.nombre_employes,
            "nombre_serveurs": entreprise.nombre_serveurs,
            "nombre_postes_clients": entreprise.nombre_postes_clients,
            "services_exposes": entreprise.services_exposes or [],
            "created_at": entreprise.created_at.isoformat() if entreprise.created_at else None,
            "updated_at": entreprise.updated_at.isoformat() if entreprise.updated_at else None,
        }