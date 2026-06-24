/** Service CRUD des vulnerabilites (/vulnerabilities). */
import http from './http-client'

export const vulnerabiliteService = {
  list({ actifId, entrepriseId } = {}) {
    const params = {}
    if (actifId) params.actif_id = actifId
    if (entrepriseId) params.entreprise_id = entrepriseId
    return http.get('/vulnerabilities', { params }).then((r) => r.data)
  },
  get(id) {
    return http.get(`/vulnerabilities/${id}`).then((r) => r.data)
  },
  create(payload) {
    return http.post('/vulnerabilities', payload).then((r) => r.data)
  },
  update(id, payload) {
    return http.put(`/vulnerabilities/${id}`, payload).then((r) => r.data)
  },
  remove(id) {
    return http.delete(`/vulnerabilities/${id}`).then((r) => r.data)
  },
}

export default vulnerabiliteService
