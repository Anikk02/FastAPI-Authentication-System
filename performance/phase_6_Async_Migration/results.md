# Phase 6: Async Migration & Load Testing Results

## Objective
Evaluate backend performance after migrating to async architecture:
- FastAPI (async)
- SQLAlchemy Async Engine
- asyncpg
- Redis caching

---

## Test Configuration

- Host: http://127.0.0.1:8000
- Tool: Locust
- DB Semaphore: 50
- Pool Size: 20
- Max Overflow: 30

---

## Test Scenarios

---

### 🔹 Scenario 1: 400 Users (Spawn Rate: 5)

| Metric              | Value        |
|--------------------|-------------|
| Total Requests     | ~20K        |
| Failures           | ~6          |
| Failure Rate       | ~0.02%      |
| Avg Response Time  | ~1555 ms    |
| Median             | ~850 ms     |
| 95th Percentile    | ~5700 ms    |
| RPS                | ~100        |

✅ **Status: Stable**

---

### 🔹 Scenario 2: 800 Users (Spawn Rate: 5)

| Metric              | Value        |
|--------------------|-------------|
| Total Requests     | ~25K        |
| Failures           | ~17         |
| Failure Rate       | ~0.06%      |
| Avg Response Time  | ~3726 ms    |
| Median             | ~1400 ms    |
| 95th Percentile    | ~14000 ms   |
| RPS                | ~116        |

⚠️ **Status: Stable but high latency**

---

### 🔹 Scenario 3: 400 Users (Spawn Rate: 10)

| Metric              | Value        |
|--------------------|-------------|
| Total Requests     | ~1900       |
| Failures           | 269         |
| Failure Rate       | **~14%**    |
| Avg Response Time  | ~6493 ms    |
| Median             | ~5400 ms    |
| 95th Percentile    | ~16000 ms   |
| RPS                | ~40         |

❌ **Status: System breakdown under burst load**

---

## Endpoint-Level Observations

### 🔹 GET /users/me
- Previously stable
- Under burst: **failures + latency spike (~3.3s avg)**
- Indicates DB/connection saturation despite Redis

---

### 🔹 POST /auth/login
- Avg latency ~9–10 seconds
- High failure rate
- CPU (bcrypt) + DB bottleneck

---

### 🔹 POST /auth/register
- Worst performing endpoint
- Avg latency ~12–13 seconds
- Highest failure probability

---

## Key Findings

### 1. Async Migration Success (Controlled Load)
- System scaled to **800 users successfully**
- No crashes under gradual load (spawn rate 5)

---

### 2. Burst Traffic Causes System Failure (Critical Insight)

Same concurrency, different spawn rate:

| Scenario | Result |
|----------|--------|
| 400 @ spawn 5 | ✅ Stable |
| 400 @ spawn 10 | ❌ 14% failures |

👉 **Root Cause:**  
System cannot absorb **sudden spikes in concurrent requests**

---

### 3. Throughput Collapse Under Stress

- RPS dropped from ~100 → ~40
- Latency increased drastically (up to 20s)
- Failure rate exploded (14%)

👉 Classic **queue buildup + resource exhaustion**

---

### 4. Bottleneck Sources

- DB connection pool saturation
- CPU-bound bcrypt hashing
- Write-heavy endpoints
- Lack of backpressure / rate limiting

---

## Final Conclusion

- Async architecture = ✅ **Scales well under steady load**
- System = ❌ **Fails under burst traffic**
- Current system is **NOT production-safe for traffic spikes**

---

## Next Steps

- Implement rate limiting (critical)
- Add request queue/backpressure
- Optimize bcrypt cost
- Increase pool capacity carefully
- Introduce background workers