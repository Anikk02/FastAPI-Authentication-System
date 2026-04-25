import { Navigate } from "react-router-dom";
import { useAppSelector } from "../app/hooks";

const ProtectedRoute = ({ children }) => {
  const { user, isLoading } = useAppSelector((state) => state.auth);

  // 🔷 While checking auth state
  if (isLoading) {
    return <div>Loading...</div>;
  }

  // 🔷 If not authenticated
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // 🔷 If authenticated
  return children;
};

export default ProtectedRoute;