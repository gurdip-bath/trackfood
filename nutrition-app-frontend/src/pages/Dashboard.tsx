import { useEffect } from "react"
import { useAuth } from "../context/AuthContext"
import api, { setAuthToken } from "../api"

const Dashboard = () => {
  const { logout, token } = useAuth()

  useEffect(() => {
    
    // Set the auth token when component mounts
    if (token) {
      setAuthToken(token)
    } else {
      return
    }

    const checkPing = async () => {
      try {
        const res = await api.get("/api/ping")
      } catch (err: any) {
        console.error("❌ Ping error:", err.message)
        console.error("Error response:", err.response?.data)
        console.error("Error status:", err.response?.status)
        
        // If unauthorized, might need to re-login
        if (err.response?.status === 401) {
        }
      }
    }

    checkPing()
  }, [token])

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <p>You're logged in. 🎉</p>
      <p>Token present: {token ? "Yes" : "No"}</p>
      <button
        onClick={logout}
        className="mt-4 px-4 py-2 bg-red-500 text-white rounded"
      >
        Log out
      </button>
    </div>
  )
}

export default Dashboard