/** Service du moteur d'analyse : risque, tableau de bord, rapport, historique. */
import http from './http-client'

export const analyseService = {
  calculerRisque(entrepriseId) {
    return http.post('/risk/calculate', { entreprise_id: entrepriseId }).then((r) => r.data)
  },
  dashboard(entrepriseId) {
    return http.get(`/dashboard/${entrepriseId}`).then((r) => r.data)
  },
  rapport(entrepriseId) {
    return http.get(`/report/${entrepriseId}`).then((r) => r.data)
  },
  history(entrepriseId) {
    return http.get(`/history/${entrepriseId}`).then((r) => r.data)
  },
}

export default analyseService
