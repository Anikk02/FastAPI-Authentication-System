import { Navigate } from "react-router-dom";
import { useAppSelector } from "../app/hooks";

const PublicRoute = ({ children }) => {
  const { user, isLoading } = useAppSelector((state) => state.auth);

  // While checking auth state
  if (isLoading) {
    return <div>Loading...</div>;
  }

  // If already logged in → redirect to dashboard
  if (user) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

export default PublicRoute;