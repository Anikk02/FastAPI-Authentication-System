const TOKEN_KEY = "access_token";

// 🔷 SET TOKEN
export const setToken = (token) => {
  localStorage.setItem(TOKEN_KEY, token);
};

// 🔷 GET TOKEN
export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

// 🔷 REMOVE TOKEN
export const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY);
};

// 🔷 CHECK AUTH
export const isAuthenticated = () => {
  return !!getToken();
};