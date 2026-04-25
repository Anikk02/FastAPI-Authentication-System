import "./Sidebar.css";
import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <h3 className="sidebar-title">Menu</h3>

      <nav>
        <Link to="/dashboard" className="sidebar-link">
          Dashboard
        </Link>

        {/* Future routes */}
        {/* <Link to="/profile" className="sidebar-link">Profile</Link> */}
      </nav>
    </div>
  );
};

export default Sidebar;