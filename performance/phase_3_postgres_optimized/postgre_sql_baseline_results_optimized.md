# 🚀 PostgreSQL Performance Benchmark Report

## 📌 Test Environment

- **Backend**: FastAPI + Uvicorn  
- **Database**: PostgreSQL  
- **ORM**: SQLAlchemy  
- **Load Testing Tool**: Locust  
- **Host**: `http://127.0.0.1:8000`  
- **Test Duration**: ~3–5 minutes  

---

# 🧪 Test 1: Optimized PostgreSQL Configuration (100 Users)

## ⚙️ Configuration

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_timeout=30,
    pool_recycle=1800,
)
```

- Concurrent Users: **100**
- Spawn Rate: **10 users/sec**

---

## 📊 Results (100 Users)

| Endpoint | Requests | Fails | Median | Avg | p95 | p99 | Max |
|----------|----------|-------|--------|-----|-----|-----|-----|
| GET /users/me | 5682 | 0 | 620 ms | 859 ms | 2400 ms | 3100 ms | 4293 ms |
| POST /auth/login | 2049 | 0 | 1400 ms | 1524 ms | 2800 ms | 4000 ms | 4789 ms |
| POST /auth/login (re-auth) | 1428 | 0 | 1400 ms | 1510 ms | 2800 ms | 3800 ms | 5074 ms |
| POST /auth/register | 762 | 2 | 1400 ms | 1504 ms | 2800 ms | 4100 ms | 4473 ms |

---

## 📈 Aggregated Metrics

| Metric | Value |
|--------|--------|
| Total Requests | 10,070 |
| Total Failures | 2 |
| Failure Rate | **0.02%** |
| Average Latency | **1148 ms** |
| Median Latency | 1000 ms |
| p95 Latency | 2600 ms |
| p99 Latency | 3600 ms |
| Maximum Latency | 5074 ms |
| Throughput | **46.3 RPS** |

---

## ✅ Observations (100 Users)

- System is **stable under 100 concurrent users**
- Near-zero failure rate
- Good throughput (~46 RPS)
- Read endpoint performs best
- Bottleneck mainly due to **bcrypt hashing (CPU-bound)**

---

# 🧪 Test 2: Optimized PostgreSQL Configuration (300 Users)

## ⚙️ Configuration

(Same optimized SQLAlchemy pooling configuration as above)

- Concurrent Users: **300**
- Spawn Rate: **10 users/sec**

---

## 📊 Results (300 Users)

| Endpoint | Requests | Fails | Median | Avg | p95 | p99 | Max |
|----------|----------|-------|--------|-----|-----|-----|-----|
| GET /users/me | 55 | 22 | 120000 ms | 117089 ms | 219000 ms | 220000 ms | 219637 ms |
| POST /auth/login | 134 | 89 | 96000 ms | 83125 ms | 156000 ms | 217000 ms | 218159 ms |
| POST /auth/login (re-auth) | 91 | 79 | 124000 ms | 110394 ms | 156000 ms | 218000 ms | 217545 ms |
| POST /auth/register | 77 | 39 | 121000 ms | 97944 ms | 155000 ms | 216000 ms | 216390 ms |

---

## 📉 Aggregated Metrics

| Metric | Value |
|--------|--------|
| Total Requests | 716 |
| Total Failures | 334 |
| Failure Rate | **47%** |
| Average Latency | **83,899 ms (~84 sec)** |
| Median Latency | 92,000 ms |
| p95 Latency | 187,000 ms |
| p99 Latency | 219,000 ms |
| Maximum Latency | 219,637 ms |
| Throughput | **5.8 RPS** |

---

## ❌ Observations (300 Users)

- System becomes **unstable at 300 concurrent users**
- High failure rate (~47%)
- Extreme latency (seconds → minutes)
- Throughput drops significantly
- Indicates **CPU and application-level bottlenecks**, not database pooling

---

# 🔍 Final Comparison

| Metric | 100 Users | 300 Users |
|--------|----------|----------|
| Failure Rate | 0.02% | 47% |
| Avg Latency | ~1.1 sec | ~84 sec |
| Throughput | 46.3 RPS | 5.8 RPS |
| Stability | Stable | Unstable |

---

# 🧠 Key Insights

1. Optimized PostgreSQL pooling works efficiently up to **100 concurrent users**
2. Increasing users to 300 exposes **system bottlenecks beyond DB**
3. Major bottlenecks:
   - CPU-intensive bcrypt hashing
   - Single Uvicorn worker
   - Blocking request handling
4. Database is **no longer the primary bottleneck**

---

# 🚀 Next Steps (Scaling Plan)

- Increase **Uvicorn workers** (`--workers 4` or more)
- Use **async PostgreSQL driver (`asyncpg`)**
- Implement **Redis caching** for frequent reads
- Offload password hashing (background tasks or reduce cost factor)
- Add **load balancer (Nginx)**
- Horizontal scaling (multiple instances)

---

# ✅ Conclusion

The optimized PostgreSQL configuration provides a **solid and stable baseline at 100 users**. However, at higher concurrency (300 users), system performance degrades significantly due to **CPU and application-layer limitations**, indicating the need for **multi-layer scaling (compute + async + caching)**.

