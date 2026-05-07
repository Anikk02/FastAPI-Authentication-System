import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../../../app/hooks";
import { login, loadUser } from "../authSlice";
import Input from "../../../components/common/Input";
import Button from "../../../components/common/Button";
import { validateLogin } from "../../../utils/validators";
import "./LoginForm.css";

const LoginForm = () => {
  const [form, setForm] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});

  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const { isLoading, error } = useAppSelector(
    (state) => state.auth
  );

  const handleSubmit = async (e) => {
    e.preventDefault();

    // 🔷 Validate before API call
    const validationErrors = validateLogin(form);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({}); // clear old errors

    const res = await dispatch(login(form));

    if (res.meta.requestStatus === "fulfilled") {
      await dispatch(loadUser());
      navigate("/dashboard");
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <div>
        <Input
          type="email"
          placeholder="Email"
          onChange={(e) =>
            setForm({ ...form, email: e.target.value })
          }
        />
        {errors.email && <p className="error">{errors.email}</p>}
      </div>

      <div>
        <Input
          type="password"
          placeholder="Password"
          onChange={(e) =>
            setForm({ ...form, password: e.target.value })
          }
        />
        {errors.password && (
          <p className="error">{errors.password}</p>
        )}
      </div>

      <Button
        text={isLoading ? "Logging in..." : "Login"}
        type="submit"
        disabled={isLoading}
      />

      {/* Backend error */}
      {error && <p className="error">{error}</p>}
    </form>
  );
};

export default LoginForm;