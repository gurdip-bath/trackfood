// src/api/index.ts
import axios from 'axios'
import { supabase } from '../supabase'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
})

// Attach Supabase token to every request
api.interceptors.request.use(async (config) => {
  const {
    data: { session },
  } = await supabase.auth.getSession()

  const token = session?.access_token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
