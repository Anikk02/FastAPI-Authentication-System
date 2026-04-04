# 📊 Baseline Performance Results (PostgreSQL - Default Pool)

## Test Setup

- Tool: Locust
- Backend: FastAPI (single instance)
- Database: PostgreSQL
- ORM: SQLAlchemy (default pool config)
- Host: http://127.0.0.1:8000
- Workload Type: Auth-heavy (register, login, protected route)

### SQLAlchemy Default Pool Config

- pool_size = 5
- max_overflow = 10
- max connections ≈ 15

---

## 🔴 Test Configuration

| Users | Spawn Rate |
|------|-----------|
| 100 | 10 |

---

## 📉 Results

- Total Requests: 333
- Failures: 130
- Failure Rate: **~39% ❌**

- Avg Latency: ~36,871 ms
- Median Latency: ~31,000 ms
- p95 Latency: ~89,000 ms
- p99 Latency: ~89,000 ms

- Throughput: ~2.1 req/sec

---

## 📊 Endpoint Breakdown

| Endpoint | Median | Avg | Max |
|----------|--------|-----|-----|
| `/users/me` | 58,000 ms | 45,949 ms | 89,546 ms |
| `/auth/login` | 56,000 ms | 42,286 ms | 89,372 ms |
| `/auth/register` | 57,000 ms | 46,039 ms | 86,190 ms |

---

## ⚠️ Errors Observed
sqlalchemy.exc.TimeoutError:
QueuePool limit of size 5 overflow 10 reached, connection time out, timeout 30

---

## 📌 Key Observations

- High failure rate (~39%) under moderate concurrency
- Extremely high latency (30–90 seconds)
- System becomes unresponsive under load
- Requests queue up waiting for DB connections

---

## ❗ Root Cause

The failure is NOT due to PostgreSQL itself.

The bottleneck is:

👉 SQLAlchemy connection pool exhaustion

- Only ~15 concurrent DB connections available
- 100 users generate more concurrent DB requests
- Requests wait for connections
- Timeout occurs → failures (500 errors)

---

## 🔍 Conclusion

- PostgreSQL removes SQLite locking limitations
- But default SQLAlchemy pool is insufficient for concurrent workloads
- System fails due to connection starvation, not DB capability

---

## ⚠️ Limitation

- Single FastAPI instance
- No connection pool tuning
- No caching layer (Redis)
- CPU-bound bcrypt hashing still present

---

