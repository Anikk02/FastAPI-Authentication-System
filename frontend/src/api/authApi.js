import API from "./axios";

// 🔷 REGISTER
export const registerUser = async (data) => {
  // data = { email, password }
  const response = await API.post("/auth/register", data);
  return response.data;
};

// 🔷 LOGIN
export const loginUser = async (data) => {
  // data = { email, password }
  const response = await API.post("/auth/login", data);

  // Expected: { access_token, token_type }
  return response.data;
};

// 🔷 GET CURRENT USER (Protected)
export const getProfile = async () => {
  const response = await API.get("/auth/me");
  return response.data;
};

// 🔷 LOGOUT (optional backend endpoint)
export const logoutUser = async () => {
  try {
    await API.post("/auth/logout"); // only if you implemented it
  } catch (err) {
    // ignore if not implemented
  }

  // Always clear frontend token
  localStorage.removeItem("access_token");
};