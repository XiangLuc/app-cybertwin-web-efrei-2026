/** Service CRUD des actifs (/assets). */
import http from './http-client'

export const actifService = {
  list(entrepriseId) {
    const params = entrepriseId ? { entreprise_id: entrepriseId } : {}
    return http.get('/assets', { params }).then((r) => r.data)
  },
  get(id) {
    return http.get(`/assets/${id}`).then((r) => r.data)
  },
  create(payload) {
    return http.post('/assets', payload).then((r) => r.data)
  },
  update(id, payload) {
    return http.put(`/assets/${id}`, payload).then((r) => r.data)
  },
  remove(id) {
    return http.delete(`/assets/${id}`).then((r) => r.data)
  },
}

export default actifService
