import { Link } from "react-router-dom";
import "./Home.css";

const Home = () => {
  return (
    <div className="home">
      <h1>Welcome to Auth System</h1>
      <p>Secure authentication built with FastAPI + React</p>

      <div className="home-actions">
        <Link to="/login" className="home-btn">
          Login
        </Link>
        <Link to="/register" className="home-btn secondary">
          Register
        </Link>
      </div>
    </div>
  );
};

export default Home;