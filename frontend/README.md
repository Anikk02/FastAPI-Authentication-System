# 🔐 FastAPI Authentication System (Frontend)

A scalable and production-ready authentication frontend built with React, Redux Toolkit, and Axios, designed to integrate seamlessly with a FastAPI backend.

---

## 🚀 Features

- 🔑 User Registration & Login
- 🔐 JWT-based Authentication
- 🔄 Persistent Login (Auto-load user on refresh)
- 🛡️ Protected Routes (Dashboard access control)
- 🚫 Public Route Guard (Prevent logged-in users from accessing auth pages)
- ⚡ Axios Interceptors (Token injection + global error handling)
- ✅ Form Validation (Custom validators)
- 🧠 Centralized State Management (Redux Toolkit)
- 🎯 Clean and scalable folder architecture

---

## 🏗️ Tech Stack

- **Frontend:** React (CRA)
- **State Management:** Redux Toolkit
- **Routing:** React Router DOM
- **HTTP Client:** Axios
- **Styling:** CSS (Modular structure)

---

## 📂 Project Structure

```
frontend/
│
├── public/
│
├── src/
│   ├── api/               # Axios + API calls
│   ├── app/               # Redux store + hooks
│   ├── components/        # Reusable UI components
│   ├── features/
│   │   └── auth/          # Auth module (slice, forms, pages)
│   ├── pages/             # App-level pages
│   ├── routes/            # Routing (protected + public)
│   ├── utils/             # Helpers (validators, token)
│   ├── styles/            # Global styles
│   ├── App.jsx
│   └── index.js
│
├── .env
├── package.json
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root:

```
REACT_APP_API_BASE_URL=http://127.0.0.1:8000
```

---

## 📦 Installation & Setup

```bash
# 1. Clone repository
git clone <your-repo-url>

# 2. Navigate to frontend
cd frontend

# 3. Install dependencies
npm install

# 4. Start development server
npm start
```

---

## 🔗 Backend Integration

This frontend is designed to work with a FastAPI backend providing:

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

Make sure your backend is running on: `http://127.0.0.1:8000`

---

## 🔐 Authentication Flow

```
Login/Register → Store JWT → Attach via Axios → Access Protected Routes
                         ↓
                  Auto-load user on refresh
```

---

## 🛡️ Route Protection

**Public Routes:**
- `/login`
- `/register`

**Protected Routes:**
- `/dashboard`

---

## 🔄 Axios Interceptors

- Automatically attaches JWT to every request
- Handles 401 Unauthorized globally
- Prepares system for refresh token implementation

---

## ✅ Validation

- Email format validation
- Password length validation
- Prevents invalid API calls

---

## 📈 Future Improvements

- 🔁 Refresh Token Flow (Auto-login without logout)
- 🎨 UI Upgrade (Tailwind / Modern Design)
- 🔔 Toast Notifications
- 👤 User Profile & Settings
- 🔐 Role-Based Authorization (Admin/User)
- 🌐 Deployment (Vercel + Backend Hosting)

---

## 📸 Screenshots


---

## 🧠 Key Learnings

- Scalable frontend architecture
- Redux async flows (createAsyncThunk)
- Secure authentication handling
- API integration with interceptors
- Clean separation of concerns

---

## 👨‍💻 Author

**Aniket Paswan**

Aspiring AI/ML Engineer | Backend Engineer

---

## ⭐ Contribute / Feedback

Feel free to fork, improve, and suggest enhancements!