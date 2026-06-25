/** Service des notifications (/notifications). */
import http from './http-client'

export const notificationService = {
  list() {
    return http.get('/notifications').then((r) => r.data)
  },
  unreadCount() {
    return http.get('/notifications/unread-count').then((r) => r.data.count)
  },
  markRead(id) {
    return http.patch(`/notifications/${id}/read`).then((r) => r.data)
  },
  markAllRead() {
    return http.post('/notifications/read-all').then((r) => r.data)
  },
  remove(id) {
    return http.delete(`/notifications/${id}`).then((r) => r.data)
  },
}

export default notificationService
