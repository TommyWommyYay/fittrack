import axios from 'axios'
import { getToken } from './auth'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const API = axios.create({
  baseURL: BASE_URL,
})

// Automatically attach the Bearer token to every request
API.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Extract a readable error message from Axios error responses
export function getErrorMessage(error) {
  if (error.response?.data?.detail) {
    const detail = error.response.data.detail
    // Pydantic validation errors return an array of objects
    if (Array.isArray(detail)) {
      return detail.map((e) => e.msg).join(' ')
    }
    return detail
  }
  return 'An unexpected error occurred. Please try again.'
}

export default API
