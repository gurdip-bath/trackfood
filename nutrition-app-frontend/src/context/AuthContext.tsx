import { createContext, useContext, useState, useEffect } from 'react'
import { supabase } from '../supabase'
import type { ReactNode } from 'react'

type AuthContextType = {
  token: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  signUp: (email: string, password: string) => Promise<void>
}

const AuthContext = createContext<AuthContextType | null>(null)

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null)

  // Initialize token from existing session on app load
  useEffect(() => {
    const initializeAuth = async () => {
      const { data: { session } } = await supabase.auth.getSession()
      if (session?.access_token) {
        setToken(session.access_token)
      }
    }
    initializeAuth()

    // Listen for auth state changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        setToken(session?.access_token || null)
      }
    )

    return () => subscription.unsubscribe()
  }, [])

  const login = async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    console.log("Token:", data.session?.access_token)

    if (error) throw new Error(error.message)
    setToken(data.session?.access_token || null)
  }

  const logout = async () => {
    await supabase.auth.signOut()
    setToken(null)
  }

  const signUp = async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signUp({ email, password })
    console.log("SignUp Response:", data)

    if (error) throw new Error(error.message)
    // Don't set token here if email confirmation is required
  }

  return (
    <AuthContext.Provider value={{ token, login, logout, signUp }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}