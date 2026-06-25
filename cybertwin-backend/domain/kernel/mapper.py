from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

TDomain = TypeVar('TDomain')
TExternal = TypeVar('TExternal')

'''
Classe abstraite de base pour les mappers, chaque mapper doit heriter de cette classe.
Permet de passer d'un objet externe (DTO / base de donnees) a un objet domaine et vice versa.
Par defaut, les methodes to_domain_list et to_external_list sont implementees pour
transformer des listes d'objets. Chaque mapper devra en revanche reimplementer les
methodes to_domain et to_external pour s'adapter a ses besoins.
'''

class BaseMapper(ABC, Generic[TDomain, TExternal]):
    @abstractmethod
    def to_domain(self, external: TExternal) -> TDomain:
        """Transforme un objet externe (DTO / base de donnees) en un objet domaine"""
        pass

    @abstractmethod
    def to_external(self, domain: TDomain) -> TExternal:
        """Transforme un objet domaine en un objet externe (dict)"""
        pass

    def to_domain_list(self, externals: List[TExternal]) -> List[TDomain]:
        return [self.to_domain(external) for external in externals]

    def to_external_list(self, domains: List[TDomain]) -> List[TExternal]:
        return [self.to_external(domain) for domain in domains]