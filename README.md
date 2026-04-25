# 🚀 FastAPI Authentication System (Backend Project)

## 📌 Overview

This project is a **production-style FastAPI authentication system** designed with scalability, performance, and real-world backend engineering practices in mind.

It demonstrates how to build and optimize a backend system using:

- FastAPI
- PostgreSQL
- Redis
- JWT Authentication
- Load Testing (Locust)

---

## 🧠 Key Features

- 🔐 JWT-based Authentication (Login/Register)
- 👤 User Management APIs
- ⚡ Redis Caching for performance optimization
- 🗄️ PostgreSQL with optimized connection pooling
- 🧪 Load testing with Locust
- 📊 Performance benchmarking & analysis
- 🔄 Multi-worker scaling using Uvicorn

---

## 🏗️ Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | FastAPI |
| Database | PostgreSQL |
| Cache | Redis |
| ORM | SQLAlchemy |
| Auth | JWT (python-jose) |
| Password Hashing | bcrypt (passlib) |
| Load Testing | Locust |

---

## ⚙️ System Architecture

```
Client → FastAPI → Redis (cache) → PostgreSQL
                ↓
             JWT Auth
```

---

## Architectural Design
Shows interactions between FastAPI, Redis, and PostgreSQL with JWT-based authentication.
![alt text](architectural_design.png)

## 🔥 Performance Journey

### Phase 1: Initial System
- High latency
- DB bottleneck
- Poor scalability

### Phase 2: PostgreSQL Optimization
- Connection pooling introduced
- Improved stability

### Phase 3: bcrypt Optimization
- Reduced hashing cost
- Improved response time

### Phase 4: Redis Integration
- Cached `/users/me`
- Eliminated repeated DB reads

---

## 📊 Benchmark Results

### ✅ With Redis (300 Users)

- Throughput: ~155 RPS
- Avg Latency: ~456 ms
- Failure Rate: ~0.09%

### ⚠️ With Redis (500 Users)

- Throughput: ~93 RPS
- Avg Latency: ~1.7 sec
- Failure Rate: ~3%

---

## 🧠 Key Insights

- Redis removed the database bottleneck
- System shifted from **I/O-bound → CPU-bound**
- bcrypt hashing became the main limitation
- Worker saturation affects performance under high load

---

## 📁 Project Structure

```
FastAPI-Authentication-System/
│
├── .github/
│ └── workflows/
│ └── ci.yml # CI/CD pipeline (GitHub Actions)
│
├── app/
│ ├── core/
│ │ └── redis.py # Redis client setup
│ │
│ ├── routes/
│ │ ├── auth_routes.py # Authentication endpoints (login/register)
│ │ ├── user_routes.py # User endpoints (/users/me)
│ │ ├── redis_routes.py # Redis test/debug endpoints
│ │ └── init.py
│ │
│ ├── init.py
│ ├── auth.py # JWT + password hashing (bcrypt)
│ ├── config.py # Environment configuration
│ ├── database.py # DB connection & session
│ ├── dependencies.py # Auth dependency (get_current_user)
│ ├── logger.py # Logging setup
│ ├── main.py # FastAPI entry point
│ ├── models.py # SQLAlchemy models
│ └── schemas.py # Pydantic schemas
│
├── diagrams/ # System design diagrams
│ ├── architectural_design.png
│ ├── component.png
│ ├── sequence_login.png
│ ├── sequence_users_me.png
│ ├── state_auth.png
│ ├── deployment.png
│ └── data_flow.png
│
├── performance/ # Load testing & benchmarking
│ ├── screenshots/ # Locust UI screenshots
│ ├── results/ # Metrics per phase
│ └── notes/ # Observations & insights
│
├── tests/ # Unit & integration tests
├── logs/ # Application logs
│
├── requirements.txt # Dependencies
├── README.md # Project documentation
├── LICENSE
├── .gitignore
├── test_auth.db # SQLite test DB (local/testing)
└── .test_auth.db # Temporary test DB (CI)
```

---

## 🚀 How to Run

### 1. Clone Repository

```
git clone <your-repo-url>
cd FastAPI-Authentication-System
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Start PostgreSQL

Make sure PostgreSQL is running and configured.

### 4. Start Redis (Docker)

```
docker run -d -p 6379:6379 redis
```

### 5. Run Server

```
uvicorn app.main:app --workers 4
```

---

## 🧪 Load Testing

Run Locust:

```
locust -f locustfile.py --host=http://127.0.0.1:8000
```

Open:

```
http://localhost:8089
```

---

## 🔮 Future Improvements

- Async DB (asyncpg)
- Background password hashing
- Load balancer (Nginx)
- Horizontal scaling (multiple instances)
- Rate limiting using Redis

---

## 🎯 What This Project Demonstrates

- Backend system design
- Performance optimization
- Load testing & benchmarking
- Bottleneck identification
- Real-world scalability challenges

---

## 👨‍💻 Author

**Aniket Paswan**

Aspiring AI/ML Engineer,Backend Engineer

---

## ⭐ Final Note

This project reflects a **real engineering journey**:

```
Database Bottleneck → Redis Optimization → CPU Bottleneck
```

Understanding this transition is key to designing scalable backend systems.

