import {
  loginUser,
  registerUser,
  getProfile,
  logoutUser,
} from "../../api/authApi";

// 🔷 Auth Service Layer
// Keeps Redux slice clean and abstracts API calls

export const authService = {
  // 🔑 LOGIN
  async login(credentials) {
    const data = await loginUser(credentials);
    return data; // { access_token, token_type }
  },

  // 📝 REGISTER
  async register(userData) {
    const data = await registerUser(userData);
    return data;
  },

  // 👤 GET CURRENT USER
  async getProfile() {
    const data = await getProfile();
    return data;
  },

  // 🚪 LOGOUT
  async logout() {
    try {
      await logoutUser(); // optional backend endpoint
    } catch {
      // ignore if backend logout not implemented
    }

    // Always clear token on frontend
    localStorage.removeItem("access_token");
  },
};