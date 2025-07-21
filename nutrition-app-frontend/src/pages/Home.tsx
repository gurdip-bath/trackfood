import { Link } from "react-router-dom"

export default function Home() {
  return (
    <div>
      <h1>Welcome to the Nutrition App</h1>
      <Link to="/login">Login</Link> | <Link to="/register">Register</Link>
    </div>
  )
}
