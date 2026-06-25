const API_BASE_URL = 'http://localhost:5000'

export const environment = {
  apiBaseUrl: API_BASE_URL,
  endpoints: {
    auth: `${API_BASE_URL}/auth`,
    company: `${API_BASE_URL}/company`,
    assets: `${API_BASE_URL}/assets`,
    vulnerabilities: `${API_BASE_URL}/vulnerabilities`,
    risk: `${API_BASE_URL}/risk/calculate`,
    dashboard: `${API_BASE_URL}/dashboard`,
    report: `${API_BASE_URL}/report`,
  },
}

export default environment
