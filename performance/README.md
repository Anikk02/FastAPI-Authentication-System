# ⚡ Performance Testing Guide (Locust)

## 📌 Overview

This document explains how to perform load testing on the FastAPI Authentication System using **Locust**.

The goal is to evaluate:

- System scalability
- Latency under load
- Throughput (RPS)
- Failure rates
- Bottlenecks (DB, CPU, Cache)

---

## 🧠 Why Load Testing?

Load testing helps simulate real-world traffic and answers:

- How many users can the system handle?
- When does performance degrade?
- What is the main bottleneck?

---

## 🛠️ Tool Used

- **Locust** (Python-based load testing tool)

---

## 📁 File Used

```
locustfile.py
```

This file defines user behavior and API request patterns.

---

## 🚀 How to Run Load Test

### 1. Start FastAPI Server

```
uvicorn app.main:app --workers 4
```

---

### 2. Run Locust

```
locust -f locustfile.py --host=http://127.0.0.1:8000
```

---

### 3. Open Web UI

```
http://localhost:8089
```

---

## ⚙️ Test Configuration

Typical parameters used:

- Users: 100 / 300 / 500
- Spawn Rate: 10 users/sec
- Duration: 3–5 minutes

---

## 📊 Key Metrics Explained

| Metric | Meaning |
|-------|--------|
| RPS | Requests per second |
| Avg Latency | Average response time |
| Median | 50th percentile |
| p95 | 95% of requests are below this value |
| p99 | Worst-case latency (almost) |
| Failures | % of failed requests |

---

## 🔥 Endpoints Tested

- `POST /auth/register`
- `POST /auth/login`
- `GET /users/me`

---

## 🧪 Testing Strategy

### Phase 1: Baseline

- PostgreSQL only
- Identify DB bottlenecks

### Phase 2: Optimization

- Connection pooling
- Reduced latency

### Phase 3: bcrypt Tuning

- Reduced hashing cost
- Improved CPU performance

### Phase 4: Redis Integration

- Cached `/users/me`
- Reduced DB load

---

## 📈 Observations Summary

### Without Redis

- High DB load
- Higher latency
- Lower throughput

### With Redis

- Faster read operations
- Increased throughput
- Reduced DB pressure

---

## ⚠️ Bottleneck Analysis

| Stage | Bottleneck |
|------|-----------|
| Initial | Database |
| After DB optimization | CPU (bcrypt) |
| After Redis | CPU saturation |

---

## 🎯 Key Learnings

1. Database is usually the first bottleneck
2. Caching improves read-heavy endpoints significantly
3. CPU-bound tasks (bcrypt) limit scalability
4. Increasing workers helps but has limits
5. Load testing reveals real system behavior

---

## 🚀 Tips for Accurate Testing

- Always warm up the system before testing
- Use realistic user flows (login → access endpoint)
- Monitor CPU usage during tests
- Run tests multiple times for consistency

---

## 🔮 Future Improvements

- Distributed load testing
- Grafana + Prometheus monitoring
- Auto-scaling with load balancer
- Async request handling

---

## 🎯 Conclusion

Locust helped simulate real-world traffic and identify critical performance bottlenecks.

This testing process guided:

- Database optimization
- Cache implementation
- CPU bottleneck identification

---

## 👨‍💻 Author

**Aniket Paswan**

Backend & AI Enthusiast focused on building scalable systems.

---

## ⭐ Final Note

Performance testing is not optional — it is essential for building reliable backend systems.

