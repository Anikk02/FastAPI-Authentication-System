# 📊 Baseline Performance Results (SQLite)

## Test Setup

- Tool: Locust
- Backend: FastAPI (single instance)
- Database: SQLite
- Host: http://127.0.0.1:8000
- Workload Type: Auth-heavy (register, login, protected route)

### Test Configurations

| Test | Users | Spawn Rate |
|------|------|-----------|
| Moderate Load | 100 | 10 |

---

## 🔴 Moderate Load Results (100 Users, Spawn Rate 10 - Sustained Load)

- Total Requests: 677
- Failures: 263
- Failure Rate: ~38.8%
- Avg Latency: ~45.4 seconds
- Median Latency: ~45+ seconds (skewed due to queueing)
- Max Latency: ~91.3 seconds
- Throughput: ~1.92 req/sec

### Endpoint Breakdown

| Endpoint | Requests | Fails |
|----------|----------|-------|
| `/users/me` | 207 | 63 |
| `/auth/login` | 150 | 81 |
| `/auth/login (re-auth)` | 111 | 71 |
| `/auth/register` | 71 | 28 |

### Observations

- System enters severe saturation under sustained load
- Failure rate (~38.8%) indicates backend instability
- Latency increases drastically due to request queue buildup
- Tail latency extremely high (up to ~90 seconds)
- Throughput collapses despite ongoing traffic
- Write-heavy endpoints (`/auth/register`) degrade first
- Read endpoints (`/users/me`) also impacted due to system-wide contention

---

## 📌 Key Findings

- SQLite performs well under moderate load
- System degrades under increased concurrency
- Under sustained load, system collapses with:
  - high latency
  - high failure rate (~38.8%)
  - reduced throughput
- Bottleneck is primarily at the database layer

---

## ⚠️ Limitations

These results are based on:

- Single FastAPI instance
- SQLite database (file-based)
- Local machine testing environment

Results may vary with:
- distributed systems
- production-grade databases
- horizontal scaling

---

## 🚀 Conclusion

The system is functionally correct but not suitable for high-concurrency workloads using SQLite. Performance degradation is caused by database contention, request queue buildup, and CPU-intensive authentication logic. This motivates migration to PostgreSQL and further scalability improvements.