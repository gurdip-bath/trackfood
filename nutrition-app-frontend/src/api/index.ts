import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
})

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('Making request to:', config.url)
    console.log('Request headers:', config.headers)
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// We'll set the token dynamically from components or context
// Instead of trying to get it in the interceptor
export const setAuthToken = (token: string | null) => {
  console.log('Setting auth token:', token ? `${token.substring(0, 20)}...` : 'null')
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    delete api.defaults.headers.common['Authorization']
  }
}

export default api