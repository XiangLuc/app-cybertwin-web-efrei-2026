/**
 * Store de l'interface (Pinia) : theme clair/sombre et etat de la sidebar.
 * Persiste les preferences dans le localStorage.
 */
import { defineStore } from 'pinia'

export const useUiStore = defineStore('ui', {
  state: () => ({
    theme: localStorage.getItem('cybertwin_theme') || 'dark',
    sidebarReduite: JSON.parse(localStorage.getItem('cybertwin_sidebar') || 'false'),
    sidebarMobileOuverte: false,
  }),
  getters: {
    estSombre: (state) => state.theme === 'dark',
  },
  actions: {
    appliquerTheme() {
      const racine = document.documentElement
      racine.classList.toggle('app-dark', this.theme === 'dark')
      racine.classList.toggle('app-light', this.theme === 'light')
    },
    basculerTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark'
      localStorage.setItem('cybertwin_theme', this.theme)
      this.appliquerTheme()
    },
    basculerSidebar() {
      this.sidebarReduite = !this.sidebarReduite
      localStorage.setItem('cybertwin_sidebar', JSON.stringify(this.sidebarReduite))
    },
    basculerSidebarMobile() {
      this.sidebarMobileOuverte = !this.sidebarMobileOuverte
    },
    fermerSidebarMobile() {
      this.sidebarMobileOuverte = false
    },
  },
})
