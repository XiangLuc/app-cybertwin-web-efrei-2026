/**
 * Store de l'entreprise selectionnee (Pinia).
 *
 * L'entreprise active sert de contexte pour les actifs, vulnerabilites,
 * le tableau de bord et le rapport.
 */
import { defineStore } from 'pinia'
import { entrepriseService } from '@/services/entreprise-service'

export const useEntrepriseStore = defineStore('entreprise', {
  state: () => ({
    entreprises: [],
    selectionId: JSON.parse(localStorage.getItem('cybertwin_entreprise') || 'null'),
    chargement: false,
  }),

  getters: {
    selection: (state) =>
      state.entreprises.find((e) => e.id === state.selectionId) || null,
  },

  actions: {
    async charger() {
      this.chargement = true
      try {
        this.entreprises = await entrepriseService.list()
        // Selection par defaut : la premiere entreprise si rien n'est choisi.
        if (!this.selectionId && this.entreprises.length) {
          this.selectionner(this.entreprises[0].id)
        }
        // Si l'entreprise selectionnee n'existe plus, on reinitialise.
        if (this.selectionId && !this.selection) {
          this.selectionner(this.entreprises[0]?.id ?? null)
        }
      } finally {
        this.chargement = false
      }
    },

    selectionner(id) {
      this.selectionId = id
      localStorage.setItem('cybertwin_entreprise', JSON.stringify(id))
    },
  },
})
