import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { loginUser, getProfile, registerUser } from "../../api/authApi"; // ✅ added

// 🔷 REGISTER
export const register = createAsyncThunk(
  "auth/register",
  async (userData, thunkAPI) => {
    try {
      const data = await registerUser(userData);
      return data;
    } catch (err) {
      return thunkAPI.rejectWithValue(
        err.response?.data?.detail || "Registration failed"
      );
    }
  }
);

// 🔷 LOGIN
export const login = createAsyncThunk(
  "auth/login",
  async (credentials, thunkAPI) => {
    try {
      const data = await loginUser(credentials);

      localStorage.setItem("access_token", data.access_token);

      return data;
    } catch (err) {
      return thunkAPI.rejectWithValue(
        err.response?.data?.detail || "Login failed"
      );
    }
  }
);

// 🔷 LOAD USER
export const loadUser = createAsyncThunk(
  "auth/loadUser",
  async (_, thunkAPI) => {
    try {
      const data = await getProfile();
      return data;
    } catch {
      return thunkAPI.rejectWithValue("Not authenticated");
    }
  }
);

const authSlice = createSlice({
  name: "auth",
  initialState: {
    user: null,
    isLoading: false,
    error: null,
  },
  reducers: {
    logout: (state) => {
      state.user = null;
      localStorage.removeItem("access_token");
    },
  },
  extraReducers: (builder) => {
    builder
      // 🔷 REGISTER
      .addCase(register.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(register.fulfilled, (state) => {
        state.isLoading = false;
      })
      .addCase(register.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })

      // 🔷 LOGIN
      .addCase(login.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload.user || {}; //fallback if API doesn't return user
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })

      // 🔷 LOAD USER
      .addCase(loadUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(loadUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
      })
      .addCase(loadUser.rejected, (state) => {
        state.isLoading = false;
        state.user = null;
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;