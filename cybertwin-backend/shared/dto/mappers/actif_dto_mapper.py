"""Mapper DTO <-> entite Actif (herite de BaseMapper)."""
from domain.entities.actif import Actif
from domain.kernel.mapper import BaseMapper


class ActifDTOMapper(BaseMapper[Actif, dict]):
    def to_domain(self, dto: dict) -> Actif:
        return Actif.create(
            nom=dto["nom"],
            type_actif=dto["type_actif"],
            entreprise_id=dto["entreprise_id"],
            description=dto.get("description"),
        )

    def to_external(self, actif: Actif) -> dict:
        return {
            "id": actif.id,
            "entreprise_id": actif.entreprise_id,
            "nom": actif.nom,
            "type_actif": actif.type_actif.value if actif.type_actif else None,
            "description": actif.description,
            "created_at": actif.created_at.isoformat() if actif.created_at else None,
            "updated_at": actif.updated_at.isoformat() if actif.updated_at else None,
        }