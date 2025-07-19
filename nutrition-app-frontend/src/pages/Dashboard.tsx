// src/pages/Dashboard.tsx
import { useAuth } from "../context/AuthContext";

const Dashboard = () => {
  const { logout } = useAuth();

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <p>You're logged in. 🎉</p>
      <button
        onClick={logout}
        className="mt-4 px-4 py-2 bg-red-500 text-white rounded"
      >
        Log out
      </button>
    </div>
  );
};

export default Dashboard;
