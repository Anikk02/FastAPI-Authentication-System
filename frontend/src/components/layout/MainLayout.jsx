import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import "./MainLayout.css";

const MainLayout = ({ children }) => {
  return (
    <div>
      <Navbar />

      <div className="layout">
        <Sidebar />

        <main className="content">
          {children}
        </main>
      </div>
    </div>
  );
};

export default MainLayout;