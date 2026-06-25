/** Service CRUD des entreprises (/company). */
import http from './http-client'

export const entrepriseService = {
  list() {
    return http.get('/company').then((r) => r.data)
  },
  get(id) {
    return http.get(`/company/${id}`).then((r) => r.data)
  },
  create(payload) {
    return http.post('/company', payload).then((r) => r.data)
  },
  update(id, payload) {
    return http.put(`/company/${id}`, payload).then((r) => r.data)
  },
  remove(id) {
    return http.delete(`/company/${id}`).then((r) => r.data)
  },
}

export default entrepriseService
