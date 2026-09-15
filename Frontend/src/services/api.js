import axios from 'axios'

// Ajusta esta IP/puerto según cómo estés probando (localhost, IP local, etc.)
const api = axios.create({
  baseURL: 'http://localhost:8000',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api