import { useEffect } from "react";
import { useAppDispatch } from "./app/hooks";
import { loadUser } from "./features/auth/authslice";
import AppRoutes from "./routes/AppRoutes";

function App() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    // 🔷 Load user if token exists (auto-login)
    dispatch(loadUser());
  }, [dispatch]);

  return <AppRoutes />;
}

export default App;