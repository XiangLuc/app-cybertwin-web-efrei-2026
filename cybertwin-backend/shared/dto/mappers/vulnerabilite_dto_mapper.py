"""Mapper DTO <-> entite Vulnerabilite (herite de BaseMapper)."""
from domain.entities.vulnerabilite import Vulnerabilite
from domain.kernel.mapper import BaseMapper


class VulnerabiliteDTOMapper(BaseMapper[Vulnerabilite, dict]):
    def to_domain(self, dto: dict) -> Vulnerabilite:
        return Vulnerabilite.create(
            libelle=dto["libelle"],
            criticite=dto["criticite"],
            actif_id=dto["actif_id"],
            description=dto.get("description"),
        )

    def to_external(self, vulnerabilite: Vulnerabilite) -> dict:
        return {
            "id": vulnerabilite.id,
            "actif_id": vulnerabilite.actif_id,
            "libelle": vulnerabilite.libelle,
            "criticite": vulnerabilite.criticite.value if vulnerabilite.criticite else None,
            "description": vulnerabilite.description,
            "created_at": vulnerabilite.created_at.isoformat() if vulnerabilite.created_at else None,
            "updated_at": vulnerabilite.updated_at.isoformat() if vulnerabilite.updated_at else None,
        }