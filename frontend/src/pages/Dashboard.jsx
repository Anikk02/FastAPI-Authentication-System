import { useAppSelector } from "../app/hooks";
import MainLayout from "../components/layout/MainLayout";
import "./Dashboard.css";

const Dashboard = () => {
  const { user } = useAppSelector((state) => state.auth);

  return (
    <MainLayout>
      <div className="dashboard">
        <h1>Dashboard</h1>

        <div className="card">
          <h3>User Info</h3>
          <p><strong>Email:</strong> {user?.email}</p>
        </div>
      </div>
    </MainLayout>
  );
};

export default Dashboard;