# 🚀 FastAPI Authentication System

## Full-Stack Authentication Platform

A **production-style full-stack authentication system** built with FastAPI (backend) and React (frontend), designed with scalability, performance, and real-world engineering practices in mind.

---

## 📌 Overview

This project demonstrates how to build and optimize a complete authentication system using modern web technologies, incorporating performance optimization, load testing, and clean frontend architecture.

---

## 🧠 Key Features

### Backend
- 🔐 JWT-based Authentication (Login/Register)
- 👤 User Management APIs
- ⚡ Redis Caching for performance optimization
- 🗄️ PostgreSQL with optimized connection pooling
- 🧪 Load testing with Locust
- 📊 Performance benchmarking & analysis
- 🔄 Multi-worker scaling using Uvicorn

### Frontend
- 🔑 User Registration & Login
- 🔐 JWT-based Authentication
- 🔄 Persistent Login (Auto-load user on refresh)
- 🛡️ Protected Routes (Dashboard access control)
- 🚫 Public Route Guard (Prevent logged-in users from accessing auth pages)
- ⚡ Axios Interceptors (Token injection + global error handling)
- ✅ Form Validation (Custom validators)
- 🧠 Centralized State Management (Redux Toolkit)

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI |
| **Database** | PostgreSQL |
| **Cache** | Redis |
| **ORM** | SQLAlchemy |
| **Auth** | JWT (python-jose) |
| **Password Hashing** | bcrypt (passlib) |
| **Load Testing** | Locust |
| **Frontend** | React (CRA) |
| **State Management** | Redux Toolkit |
| **Routing** | React Router DOM |
| **HTTP Client** | Axios |
| **Styling** | CSS |

---

## ⚙️ System Architecture

```
Client (React) → FastAPI → Redis (cache) → PostgreSQL
                      ↓
                   JWT Auth
```

---

## 🎨 Architectural Design

Shows interactions between FastAPI, Redis, and PostgreSQL with JWT-based authentication.

![Architectural Design](architectural_design.png)

---

## 🔥 Performance Journey

### Phase 1: SQLite Baseline
- Database: SQLite (default)
- Test: 100 users @ spawn rate 10
- Failure Rate: ~39%
- Avg Latency: ~45 sec
- Throughput: ~1.9 RPS
- **Bottleneck:** Database contention, request queue buildup

### Phase 2: PostgreSQL (Default Pool)
- Database: PostgreSQL + SQLAlchemy default pool (size=5, overflow=10)
- Test: 100 users @ spawn rate 10
- Failure Rate: ~39%
- Avg Latency: ~37 sec
- Throughput: ~2.1 RPS
- **Bottleneck:** SQLAlchemy connection pool exhaustion (not PostgreSQL)

### Phase 3: PostgreSQL Optimization
- Connection pooling: pool_size=20, max_overflow=30
- Test 1: 100 users → ✅ Stable
  - Failure Rate: ~0.02%
  - Avg Latency: ~1.1 sec
  - Throughput: ~46.3 RPS
- Test 2: 300 users → ❌ Unstable
  - Failure Rate: ~47%
  - Avg Latency: ~84 sec
  - Throughput: ~5.8 RPS
- **Bottleneck:** CPU-intensive bcrypt hashing, single Uvicorn worker

### Phase 4: bcrypt Optimization
- Reduced bcrypt rounds: 12 → 10 (4x reduction in CPU work)
- Performance Improvement:
  - Avg Latency: ~7900 ms → ~1787 ms (4.4x faster)
  - Throughput: ~32 RPS → ~54.4 RPS (+70%)
  - Failure Rate: ~34% → ~12%
- **Trade-off:** Slightly reduced security for significant performance gain

### Phase 5: Redis Integration
- Cached `/users/me` endpoint (TTL: 300 sec)
- Test 1: 300 users → ✅ Stable
  - Throughput: ~155 RPS
  - Avg Latency: ~456 ms
  - Failure Rate: ~0.09%
- Test 2: 500 users → ⚠️ Degraded
  - Throughput: ~93 RPS
  - Avg Latency: ~1.7 sec
  - Failure Rate: ~3%
- **Key Insight:** System shifted from I/O-bound → CPU-bound (bcrypt)

### Phase 6: Async Migration
- Async architecture: FastAPI + SQLAlchemy Async + asyncpg + Redis
- Test 1: 400 users @ spawn rate 5 → ✅ Stable
  - Throughput: ~100 RPS
  - Avg Latency: ~1555 ms
  - Failure Rate: ~0.02%
- Test 2: 800 users @ spawn rate 5 → ⚠️ High Latency
  - Throughput: ~116 RPS
  - Avg Latency: ~3726 ms
  - Failure Rate: ~0.06%
- Test 3: 400 users @ spawn rate 10 → ❌ Burst Failure
  - Throughput: ~40 RPS
  - Avg Latency: ~6493 ms
  - Failure Rate: ~14%
- **Critical Finding:** System scales well under steady load but fails under burst traffic

---

## 📊 Benchmark Results Summary

| Phase | Configuration | Users | Spawn Rate | Throughput | Avg Latency | Failure Rate | Status |
|-------|--------------|-------|------------|------------|-------------|--------------|--------|
| 1 | SQLite Baseline | 100 | 10 | ~1.9 RPS | ~45 sec | ~39% | ❌ Failed |
| 2 | PostgreSQL (Default Pool) | 100 | 10 | ~2.1 RPS | ~37 sec | ~39% | ❌ Failed |
| 3 | PostgreSQL (Optimized Pool) | 100 | 10 | ~46.3 RPS | ~1.1 sec | ~0.02% | ✅ Stable |
| 3 | PostgreSQL (Optimized Pool) | 300 | 10 | ~5.8 RPS | ~84 sec | ~47% | ❌ Failed |
| 4 | bcrypt (Rounds=10) | 300 | - | ~54.4 RPS | ~1787 ms | ~12% | ⚠️ Improved |
| 5 | Redis Cache | 300 | - | ~155 RPS | ~456 ms | ~0.09% | ✅ Stable |
| 5 | Redis Cache | 500 | - | ~93 RPS | ~1.7 sec | ~3% | ⚠️ Degraded |
| 6 | Async + Redis (Steady) | 400 | 5 | ~100 RPS | ~1555 ms | ~0.02% | ✅ Stable |
| 6 | Async + Redis (Steady) | 800 | 5 | ~116 RPS | ~3726 ms | ~0.06% | ⚠️ High Latency |
| 6 | Async + Redis (Burst) | 400 | 10 | ~40 RPS | ~6493 ms | ~14% | ❌ Burst Failure |

---

## 🧠 Key Insights

- Redis removed the database bottleneck
- System shifted from **I/O-bound → CPU-bound**
- bcrypt hashing became the main limitation
- Worker saturation affects performance under high load

---

## 📁 Backend Project Structure

```
FastAPI-Authentication-System/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── core/
│   │   └── redis.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── redis_routes.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── diagrams/
│   ├── architectural_design.png
│   ├── component.png
│   ├── sequence_login.png
│   ├── sequence_users_me.png
│   ├── state_auth.png
│   ├── deployment.png
│   └── data_flow.png
│
├── performance/
│   ├── screenshots/
│   ├── results/
│   └── notes/
│
├── tests/
├── logs/
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── test_auth.db
└── .test_auth.db
```

---

## 📁 Frontend Project Structure

```
frontend/
│
├── public/
│
├── src/
│   ├── api/
│   ├── app/
│   ├── components/
│   ├── features/
│   │   └── auth/
│   ├── pages/
│   ├── routes/
│   ├── utils/
│   ├── styles/
│   ├── App.jsx
│   └── index.js
│
├── .env
├── package.json
└── README.md
```

---

## 🚀 How to Run

### Backend Setup

```bash
# 1. Clone Repository
git clone <your-repo-url>
cd FastAPI-Authentication-System

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Start PostgreSQL (ensure it's running)

# 4. Start Redis (Docker)
docker run -d -p 6379:6379 redis

# 5. Run Server
uvicorn app.main:app --workers 4
```

### Frontend Setup

```bash
# 1. Navigate to Frontend
cd frontend

# 2. Install Dependencies
npm install

# 3. Configure Environment (create .env file)
echo "REACT_APP_API_BASE_URL=http://127.0.0.1:8000" > .env

# 4. Start Development Server
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

### Public Routes (Accessible without auth)
- `/login`
- `/register`

### Protected Routes (Require authentication)
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

## 🧪 Load Testing

Run Locust for backend performance testing:

```bash
locust -f locustfile.py --host=http://127.0.0.1:8000
```

Open Locust web interface: `http://localhost:8089`

---

## 🔮 Future Improvements

### Backend
- Async DB (asyncpg)
- Background password hashing
- Load balancer (Nginx)
- Horizontal scaling (multiple instances)
- Rate limiting using Redis

### Frontend
- 🔁 Refresh Token Flow
- 🎨 UI Upgrade (Tailwind / Modern Design)
- 🔔 Toast Notifications
- 👤 User Profile & Settings
- 🔐 Role-Based Authorization
- 🌐 Deployment (Vercel + Backend Hosting)

---

## 🎯 What This Project Demonstrates

- Full-stack system design
- Performance optimization & benchmarking
- Bottleneck identification
- Real-world scalability challenges
- Clean frontend architecture
- Secure authentication handling

---

## 🧠 Key Learnings

### Backend
```
Database Bottleneck → Redis Optimization → CPU Bottleneck
```

Understanding this transition is key to designing scalable backend systems.

### Frontend
- Scalable frontend architecture
- Redux async flows (createAsyncThunk)
- Secure authentication handling
- API integration with interceptors
- Clean separation of concerns

---

## 👨‍💻 Author

**Aniket Paswan**

Aspiring AI/ML Engineer | Backend Engineer

Focused on building scalable systems and real-world applications

---

## ⭐ Contribute / Feedback

Feel free to fork, improve, and suggest enhancements!

---

## 📄 License

This project is licensed under the terms of the LICENSE file.