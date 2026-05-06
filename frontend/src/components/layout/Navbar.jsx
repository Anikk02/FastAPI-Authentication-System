import { useNavigate } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { logout } from "../../features/auth/authslice";
import "./Navbar.css";

const Navbar = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const { user } = useAppSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
    navigate("/login"); // ✅ SPA navigation
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <h3 className="logo">AuthSystem</h3>
      </div>

      <div className="navbar-right">
        {user && <span className="user-email">{user.email}</span>}
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;