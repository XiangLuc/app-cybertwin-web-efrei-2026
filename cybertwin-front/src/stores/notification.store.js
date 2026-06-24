/**
 * Store des notifications (Pinia).
 * Gere le compteur de non-lues et la liste, avec un rafraichissement leger.
 */
import { defineStore } from 'pinia'
import { notificationService } from '@/services/notification-service'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    items: [],
    count: 0,
    chargement: false,
    _timer: null,
  }),
  actions: {
    async rafraichirCompteur() {
      try { this.count = await notificationService.unreadCount() } catch { /* silencieux */ }
    },
    async charger() {
      this.chargement = true
      try {
        this.items = await notificationService.list()
        this.count = this.items.filter((n) => !n.lu).length
      } finally { this.chargement = false }
    },
    async marquerLue(id) {
      await notificationService.markRead(id)
      const n = this.items.find((i) => i.id === id)
      if (n && !n.lu) { n.lu = true; this.count = Math.max(0, this.count - 1) }
    },
    async marquerToutesLues() {
      await notificationService.markAllRead()
      this.items.forEach((n) => (n.lu = true))
      this.count = 0
    },
    async supprimer(id) {
      await notificationService.remove(id)
      const n = this.items.find((i) => i.id === id)
      if (n && !n.lu) this.count = Math.max(0, this.count - 1)
      this.items = this.items.filter((i) => i.id !== id)
    },
    demarrerPolling(intervalMs = 60000) {
      this.rafraichirCompteur()
      this.arreterPolling()
      this._timer = setInterval(() => this.rafraichirCompteur(), intervalMs)
    },
    arreterPolling() {
      if (this._timer) { clearInterval(this._timer); this._timer = null }
    },
  },
})
