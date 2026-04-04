# 🧠 Benchmark Notes – PostgreSQL Load Testing

## 📌 Purpose

This document captures key learnings, reasoning, and technical insights from load testing a FastAPI authentication system using PostgreSQL with optimized connection pooling.

---

## ⚙️ What Was Tested

- Same optimized PostgreSQL configuration was used for both tests
- Only variable changed: **number of concurrent users (100 → 300)**
- Goal: Identify system breaking point and real bottlenecks

---

## 🔍 Key Observations

### 1. PostgreSQL Pooling Works Well
- With 100 users, system handled load efficiently
- No connection starvation observed
- Confirms that:
  - `pool_size + max_overflow` was sufficient
  - DB was not the bottleneck at moderate scale

---

### 2. System Breaks at 300 Users
- Failure rate increased drastically (~47%)
- Latency jumped from ~1 sec → ~80+ sec
- Throughput dropped from ~46 RPS → ~5.8 RPS

👉 Important Insight:
> Increasing users without scaling compute leads to system collapse

---

### 3. Bottleneck Shift (Very Important Concept)

Initially:
- Problem = Database (SQLite → PostgreSQL migration solved it)

After optimization:
- New bottlenecks:
  - CPU (bcrypt hashing)
  - Application server (single worker)
  - Blocking I/O

👉 This is a classic **"bottleneck shift"** in system design

---

### 4. Authentication Endpoints Are Expensive

Compared to `GET /users/me`:

- `POST /auth/login` and `POST /auth/register` are slower because:
  - Password hashing (bcrypt)
  - DB writes (register)
  - Validation & security checks

👉 Insight:
> Not all endpoints scale equally — write & auth endpoints are costlier

---

### 5. Throughput vs Latency Tradeoff

- At 100 users:
  - Good throughput (~46 RPS)
  - Acceptable latency (~1 sec)

- At 300 users:
  - Throughput collapses
  - Latency explodes

👉 Insight:
> System saturation leads to queueing → exponential latency growth

---

## 🧩 What This Proves

### ❓ Why PostgreSQL over SQLite?
- SQLite failed under concurrency
- PostgreSQL supports connection pooling and parallel queries

### ❓ Why do we need connection pooling?
- Prevents connection overhead
- Avoids DB exhaustion
- Improves throughput under load

### ❓ Why is DB not the bottleneck anymore?
- Because optimized pooling removed contention
- Now CPU and app layer dominate

---

## 🚀 Scaling Strategy (Based on Findings)

### Step 1: Vertical Scaling (Immediate)
- Increase Uvicorn workers:
  ```bash
  uvicorn main:app --workers 4
  ```

---

### Step 2: Async Optimization
- Replace sync DB calls with:
  - `asyncpg`
  - SQLAlchemy async engine

---

### Step 3: Reduce CPU Bottleneck
- Lower bcrypt cost factor (if acceptable)
- Or offload hashing to background workers

---

### Step 4: Introduce Caching
- Use Redis for:
  - Session/token validation
  - Frequently accessed user data

---

### Step 5: Horizontal Scaling
- Add multiple app instances
- Use load balancer (Nginx / cloud LB)

---

## ⚠️ Mistakes Avoided / Lessons Learned

- ❌ Assuming DB is always the bottleneck
- ❌ Ignoring CPU-bound operations (bcrypt)
- ❌ Testing only small-scale load

- ✅ Learned to test progressively (100 → 300 users)
- ✅ Identified real bottlenecks using data
- ✅ Understood system behavior under stress

---

## 🧠 Final Takeaway

> Performance optimization is iterative.
> Fixing one bottleneck exposes the next.

This benchmark demonstrated a real-world backend scaling journey:

**SQLite → PostgreSQL → Connection Pooling → CPU Bottleneck → Scaling Strategy**

---

## 🎯 How to Explain This in Interview

You can say:

> “I performed load testing using Locust on a FastAPI authentication system. After optimizing PostgreSQL connection pooling, the system handled 100 concurrent users efficiently with ~46 RPS and negligible failures. However, at 300 users, performance degraded significantly due to CPU-bound bcrypt hashing and single-worker limitations. This helped me understand bottleneck shifting and guided me toward scaling strategies like async DB calls, caching, and horizontal scaling.”

---

**End of Notes** 🚀

