# 🧠 Benchmark Notes – bcrypt Optimization

## 📌 Context

During load testing with 300 concurrent users, the system showed:
- High latency (~8 seconds)
- High failure rate (~34%)
- Low throughput (~32 RPS)

After analysis, bcrypt hashing was identified as the primary CPU bottleneck.

---

## 🔍 Problem Identified

- bcrypt uses exponential cost factor
- Default rounds ≈ 12 → high CPU usage
- Each authentication request performs hashing

👉 Result:
- CPU saturation
- Request queue buildup
- Increased latency and failures

---

## 🔧 Optimization Applied

- Reduced bcrypt rounds from **12 → 10**

---

## 📊 Results After Optimization

| Metric | Value |
|--------|------|
| Total Requests | 11,155 |
| Total Failures | 1,359 |
| Failure Rate | ~12% |
| Average Latency | ~1787 ms |
| Median Latency | ~1100 ms |
| p95 Latency | ~5500 ms |
| p99 Latency | ~7500 ms |
| Throughput | ~54.4 RPS |

---

## 📈 Key Improvements

- Latency reduced by ~4x
- Throughput increased by ~70%
- Failure rate significantly decreased

---

## 🧠 Key Learnings

### 1. CPU-bound operations dominate at scale
- bcrypt hashing became bottleneck after DB optimization

### 2. Bottleneck shifting
- Initial bottleneck: Database
- After fix: CPU (bcrypt)

### 3. Small config change → huge impact
- Reducing rounds improved entire system performance

### 4. Concurrency alone is not enough
- Increasing workers did not solve issue initially
- Root cause was computational cost

---

## ⚠️ Remaining Issues

- Still ~12% failure rate
- CPU still partially saturated
- Blocking architecture limits concurrency

---

## 🚀 Next Optimization Steps

1. Increase Uvicorn workers (based on CPU cores)
2. Use async database driver (`asyncpg`)
3. Introduce Redis caching
4. Optimize or offload hashing
5. Horizontal scaling

---

## 🎯 Final Insight

> Performance optimization is iterative. Fixing one bottleneck reveals the next.

bcrypt optimization significantly improved performance but also highlighted deeper architectural limitations.

---

## 🧠 Interview Summary

> “During load testing, I identified bcrypt hashing as a CPU bottleneck. By reducing its cost factor, I improved latency by over 4x and increased throughput by ~70%. This demonstrated the impact of CPU-bound operations and the importance of iterative performance optimization.”

---

**End of Notes** 🚀

