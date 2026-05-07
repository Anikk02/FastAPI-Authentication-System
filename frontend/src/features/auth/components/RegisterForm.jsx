import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../../../app/hooks";
import { register } from "../authSlice";
import Input from "../../../components/common/Input";
import Button from "../../../components/common/Button";
import { validateRegister } from "../../../utils/validators";
import "./RegisterForm.css";

const RegisterForm = () => {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({});

  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const { isLoading, error } = useAppSelector(
    (state) => state.auth
  );

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationErrors = validateRegister(form);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});

    const res = await dispatch(register(form));

    if (res.meta.requestStatus === "fulfilled") {
      alert("Registration successful");
      navigate("/login");
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      {/* 🔷 Name */}
      <div>
        <Input
          type="text"
          placeholder="Name"
          onChange={(e) =>
            setForm({ ...form, name: e.target.value })
          }
        />
        {errors.name && <p className="error">{errors.name}</p>}
      </div>

      {/* 🔷 Email */}
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

      {/* 🔷 Password */}
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
        text={isLoading ? "Registering..." : "Register"}
        type="submit"
        disabled={isLoading}
      />

      {error && <p className="error">{error}</p>}
    </form>
  );
};

export default RegisterForm;