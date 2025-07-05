import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
})

const request = async (method, url, data = null, config = {}) => {
  const response = await api({ method, url, data, ...config })
  return response.data
}

function createResource(resource) {
  return {
    list: (params) => request('get', resource + '/', null, { params }),
    retrieve: (id) => request('get', `${resource}/${id}/`),
    create: (data) => request('post', resource + '/', data),
    update: (id, data) => request('put', `${resource}/${id}/`, data),
    partialUpdate: (id, data) => request('patch', `${resource}/${id}/`, data),
    delete: (id) => request('delete', `${resource}/${id}/`),
  }
}

export const productsApi = createResource('products')
export const ordersApi = createResource('orders')

export default api
