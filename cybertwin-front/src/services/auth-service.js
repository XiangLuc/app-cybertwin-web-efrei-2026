/** Service d'authentification et de gestion des utilisateurs. */
import http from './http-client'

export const authService = {
  register(payload) {
    return http.post('/auth/register', payload).then((r) => r.data)
  },
  login(email, motDePasse) {
    return http.post('/auth/login', { email, mot_de_passe: motDePasse }).then((r) => r.data)
  },
  me() {
    return http.get('/auth/me').then((r) => r.data)
  },
  changePassword(ancien, nouveau) {
    return http
      .patch('/auth/me/password', { ancien_mot_de_passe: ancien, nouveau_mot_de_passe: nouveau })
      .then((r) => r.data)
  },
  listUsers() {
    return http.get('/auth/users').then((r) => r.data)
  },
  createUser(payload) {
    return http.post('/auth/users', payload).then((r) => r.data)
  },
  changeRole(id, role) {
    return http.patch(`/auth/users/${id}/role`, { role }).then((r) => r.data)
  },
  deleteUser(id) {
    return http.delete(`/auth/users/${id}`).then((r) => r.data)
  },
}

export default authService
