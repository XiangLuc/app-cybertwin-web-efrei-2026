/**
 * Client HTTP centralise (axios).
 *
 */
import axios from 'axios'
import { environment } from '@/environment'

const http = axios.create({
  baseURL: environment.apiBaseUrl,
  headers: { 'Content-Type': 'application/json' },
  timeout: 15000,
})

export const httpEvents = new EventTarget()
function notifier(type, detail) {
  httpEvents.dispatchEvent(new CustomEvent(type, { detail }))
}

function deconnecter(redirige = true) {
  localStorage.removeItem('cybertwin_token')
  localStorage.removeItem('cybertwin_user')
  if (redirige && window.location.pathname !== '/login') {
    window.location.href = '/login'
  }
}

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('cybertwin_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

http.interceptors.response.use(
  (response) => {
    const methode = (response.config.method || 'get').toLowerCase()
    const estNotif = (response.config.url || '').includes('/notifications')
    if (methode !== 'get' && !estNotif) notifier('mutation', {})
    return response
  },
  (error) => {
    // Pas de reponse = backend injoignable (service ou BDD HS, timeout, CORS).
    if (!error.response) {
      notifier('reseau', { message: "Le serveur est injoignable. Verifiez que le backend est demarre." })
      // Si l'utilisateur est connecte, on le deconnecte
      if (localStorage.getItem('cybertwin_token')) deconnecter(true)
      return Promise.reject(error)
    }
    const status = error.response.status
    if (status === 401) {
      notifier('session', { message: 'Session expiree, reconnectez-vous.' })
      deconnecter(true)
    } else if (status >= 500) {
      notifier('serveur', { message: "Erreur cote serveur (base de donnees indisponible ?)." })
    }
    return Promise.reject(error)
  },
)

export function messageErreur(error, defaut = 'Une erreur est survenue.') {
  if (!error.response) return 'Serveur injoignable.'
  const data = error.response.data
  if (!data) return defaut
  if (Array.isArray(data.details)) return `${data.error} (${data.details.join(', ')})`
  return data.error || defaut
}

export default http
