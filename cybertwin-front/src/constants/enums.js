export const ROLES = {
  ADMIN: 'ADMIN',
  ANALYSTE: 'ANALYSTE',
  LECTEUR: 'LECTEUR',
}

// Roles autorises a ecrire (creer / modifier / supprimer).
export const ROLES_ECRITURE = [ROLES.ADMIN, ROLES.ANALYSTE]

export const TYPES_ACTIF = [
  { label: 'Serveur Web', value: 'SERVEUR_WEB' },
  { label: 'Base de donnees', value: 'BASE_DE_DONNEES' },
  { label: 'Poste utilisateur', value: 'POSTE_UTILISATEUR' },
  { label: 'Routeur', value: 'ROUTEUR' },
  { label: 'Pare-feu', value: 'PARE_FEU' },
  { label: 'Application metier', value: 'APPLICATION_METIER' },
]

export const NIVEAUX_CRITICITE = [
  { label: 'Faible', value: 'FAIBLE' },
  { label: 'Moyenne', value: 'MOYENNE' },
  { label: 'Elevee', value: 'ELEVEE' },
  { label: 'Critique', value: 'CRITIQUE' },
]

export const ROLES_OPTIONS = [
  { label: 'Analyste', value: 'ANALYSTE' },
  { label: 'Lecteur', value: 'LECTEUR' },
]

// Suggestions de services exposes sur Internet (champ multi-select).
export const SERVICES_EXPOSES = [
  'HTTPS', 'HTTP', 'VPN', 'SSH', 'FTP', 'SMTP', 'IMAP', 'RDP', 'DNS', 'SIP',
]

// Couleurs par niveau (badges, graphiques).
export const COULEUR_CRITICITE = {
  FAIBLE: '#22c55e',
  MOYENNE: '#eab308',
  ELEVEE: '#f97316',
  CRITIQUE: '#ef4444',
}

export const COULEUR_RISQUE = {
  FAIBLE: '#22c55e',
  MOYEN: '#eab308',
  ELEVE: '#ef4444',
}

export function labelTypeActif(value) {
  return TYPES_ACTIF.find((t) => t.value === value)?.label || value
}
export function labelCriticite(value) {
  return NIVEAUX_CRITICITE.find((c) => c.value === value)?.label || value
}

// Tous les roles (pour l'admin qui peut changer le role d'un utilisateur).
export const ROLES_OPTIONS_ADMIN = [
  { label: 'Administrateur', value: 'ADMIN' },
  { label: 'Analyste', value: 'ANALYSTE' },
  { label: 'Lecteur', value: 'LECTEUR' },
]
