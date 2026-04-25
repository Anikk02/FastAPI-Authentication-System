import axios from "axios";

// 🔷 Create Axios instance
const API = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL, // ✅ FIXED
  withCredentials: true, // for cookies (refresh token)
});

// 🔷 REQUEST INTERCEPTOR
// Attach access token to every request
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// 🔷 RESPONSE INTERCEPTOR
API.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response) {
      // 🔴 Unauthorized (token expired or invalid)
      if (error.response.status === 401) {
        console.warn("Unauthorized - token may be expired");

        // Optional: auto logout
        localStorage.removeItem("access_token");

        // redirect to login (only if not already there)
        if (window.location.pathname !== "/login") {
          window.location.href = "/login";
        }
      }
    }

    return Promise.reject(error);
  }
);

export default API;