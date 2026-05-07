import { Link } from "react-router-dom";
import RegisterForm from "../components/RegisterForm";
import FormContainer from "../../../components/common/FormContainer";
import "./Register.css";

const Register = () => {
  return (
    <div className="auth-page">
      <FormContainer title="Register">
        <RegisterForm />

        <p style={{ marginTop: "10px" }}>
          Already have an account?{" "}
          <Link to="/login">Login</Link>
        </p>

      </FormContainer>
    </div>
  );
};

export default Register;