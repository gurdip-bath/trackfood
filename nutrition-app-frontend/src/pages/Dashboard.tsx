import { useEffect } from "react"
import { useAuth } from "../context/AuthContext"
import api, { setAuthToken } from "../api"

const Dashboard = () => {
  const { logout, token } = useAuth()

  useEffect(() => {
    console.log("Dashboard token:", token?.substring(0, 50) + "...")
    
    // Set the auth token when component mounts
    if (token) {
      setAuthToken(token)
      console.log("Auth token set in axios")
    } else {
      console.log("No token available")
      return
    }

    const checkPing = async () => {
      try {
        console.log("Making ping request...")
        const res = await api.get("/api/ping")
        console.log("✅ Ping response:", res.data)
      } catch (err: any) {
        console.error("❌ Ping error:", err.message)
        console.error("Error response:", err.response?.data)
        console.error("Error status:", err.response?.status)
        
        // If unauthorized, might need to re-login
        if (err.response?.status === 401) {
          console.log("Token expired or invalid, consider logging out")
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