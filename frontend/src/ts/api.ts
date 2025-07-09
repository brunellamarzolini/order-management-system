import axios from 'axios'

// This const are here for assignment purposes reason, they should be moved in an .env file
const API_BASE_URL = 'http://localhost:8000/api'
const DEFAULT_LANGUAGE = 'en'

const api = axios.create({
  baseURL: API_BASE_URL,
})

// Add access token and default language to every request
api.interceptors.request.use((config) => {
  const access = localStorage.getItem('access_token')
  config.headers = config.headers || {}
  if (access) {
    config.headers['Authorization'] = `Bearer ${access}`
  }
  config.headers['Accept-Language'] = DEFAULT_LANGUAGE
  return config
})

// Auto-refresh logic
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Token expired
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      localStorage.getItem('refresh_token')
    ) {
      originalRequest._retry = true
      try {
        const response = await api.post('/auth/refresh/', {
          refresh: localStorage.getItem('refresh_token'),
        })

        const newAccess = response.data.access
        localStorage.setItem('access_token', newAccess)

        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${newAccess}`

        return api(originalRequest)
      } catch (refreshError) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  },
)

const request = async (
  method: string,
  url: string,
  data: Record<string, unknown> | null = null,
  config = {},
) => {
  const response = await api({ method, url, data, ...config })
  return response.data
}

function createResource(resource: string) {
  return {
    list: (params: Record<string, unknown> = {}) =>
      request('get', resource + '/', null, { params }),

    retrieve: (id: string) => request('get', `${resource}/${id}/`),

    create: (data?: Record<string, unknown>) => request('post', resource + '/', data),

    update: (id: string, data?: Record<string, unknown>) =>
      request('patch', `${resource}/${id}/`, data),

    delete: (id: string) => request('delete', `${resource}/${id}/`),
  }
}

export const ordersApi = createResource('orders')
export const productsApi = createResource('products')

export default api
