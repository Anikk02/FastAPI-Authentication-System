// 🔷 EMAIL VALIDATION
export const validateEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

// 🔷 PASSWORD VALIDATION
export const validatePassword = (password) => {
  return password && password.length >= 6;
};

// 🔷 NAME VALIDATION
export const validateName = (name) => {
  return name && name.trim().length >= 2;
};

// 🔷 LOGIN FORM VALIDATION
export const validateLogin = ({ email, password }) => {
  const errors = {};

  if (!email) {
    errors.email = "Email is required";
  } else if (!validateEmail(email)) {
    errors.email = "Invalid email format";
  }

  if (!password) {
    errors.password = "Password is required";
  }
  else if (!validatePassword(password)) {
    errors.password = "Password must be at least 6 characters"
  }

  return errors;
};

// 🔷 REGISTER FORM VALIDATION (UPDATED)
export const validateRegister = ({ name, email, password }) => {
  const errors = {};

  // 🔷 Name validation
  if (!name) {
    errors.name = "Name is required";
  } else if (!validateName(name)) {
    errors.name = "Name must be at least 2 characters";
  }

  // 🔷 Email validation
  if (!email) {
    errors.email = "Email is required";
  } else if (!validateEmail(email)) {
    errors.email = "Invalid email";
  }

  // 🔷 Password validation
  if (!password) {
    errors.password = "Password is required";
  } else if (!validatePassword(password)) {
    errors.password = "Password must be at least 6 characters";
  }

  return errors;
};