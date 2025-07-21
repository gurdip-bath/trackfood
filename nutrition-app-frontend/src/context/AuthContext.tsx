import { createContext, useContext, useState } from 'react'
import { supabase } from '../supabase'
import type { ReactNode } from 'react'

//BREAK DOWN CODE BELOW FOR DEEPR UNDERSTANDING

type AuthContextType = {
  token: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  signUp: (email: string, password: string) => Promise<void>
}

const AuthContext = createContext<AuthContextType | null>(null)

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null)

  const login = async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    console.log("Token:", data.session?.access_token);

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

    // Optional: set token *only* if email confirmation is disabled
    // setToken(data.session?.access_token || null)
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
// 