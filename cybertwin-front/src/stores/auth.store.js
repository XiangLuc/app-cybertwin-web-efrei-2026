/**
 * Store d'authentification (Pinia).
 *
 * Gere le jeton JWT, l'utilisateur courant et son role. Persiste le token et
 * l'utilisateur dans le localStorage pour conserver la session au rechargement.
 */
import { defineStore } from 'pinia'
import { authService } from '@/services/auth-service'
import { ROLES, ROLES_ECRITURE } from '@/constants/enums'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('cybertwin_token') || null,
    user: JSON.parse(localStorage.getItem('cybertwin_user') || 'null'),
  }),

  getters: {
    estConnecte: (state) => !!state.token,
    role: (state) => state.user?.role || null,
    estAdmin: (state) => state.user?.role === ROLES.ADMIN,
    peutEcrire: (state) => ROLES_ECRITURE.includes(state.user?.role),
    nomAffiche: (state) => {
      if (!state.user) return ''
      const { prenom, nom, email } = state.user
      return [prenom, nom].filter(Boolean).join(' ') || email
    },
  },

  actions: {
    async login(email, motDePasse) {
      const data = await authService.login(email, motDePasse)
      this._enregistrerSession(data.access_token, data.utilisateur)
      return data
    },

    async register(payload) {
      return authService.register(payload)
    },

    async rafraichirProfil() {
      const user = await authService.me()
      this.user = user
      localStorage.setItem('cybertwin_user', JSON.stringify(user))
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('cybertwin_token')
      localStorage.removeItem('cybertwin_user')
    },

    _enregistrerSession(token, user) {
      this.token = token
      this.user = user
      localStorage.setItem('cybertwin_token', token)
      localStorage.setItem('cybertwin_user', JSON.stringify(user))
    },
  },
})
