import { Link } from "react-router-dom";
import LoginForm from "../components/LoginForm";
import FormContainer from "../../../components/common/FormContainer";
import "./Login.css";

const Login = () => {
  return (
    <div className="auth-page">
      <FormContainer title="Login">
        <LoginForm />

        <p style={{ marginTop: "10px" }}>
          Don't have an account?{" "}
          <Link to="/register">Register</Link>
        </p>

      </FormContainer>
    </div>
  );
};

export default Login;