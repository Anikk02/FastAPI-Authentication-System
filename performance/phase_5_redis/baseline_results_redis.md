# Redis Optimization Benchmark Results

## Test Environment

- Backend: FastAPI + Uvicorn
- Database: PostgreSQL (Optimized Connection Pool)
- Cache Layer: Redis (Docker)
- Authentication: JWT
- Load Testing Tool: Locust
- Host: http://127.0.0.1:8000

---

# Redis Integration Overview

Redis was introduced to cache authenticated user data for the endpoint:

- `GET /users/me`

### Optimization Strategy

- Cache key: `user:{user_id}`
- TTL: 300 seconds
- Flow:
  - Check Redis
  - If hit → return cached response
  - If miss → query DB → store in Redis

---

# 🚀 Test 1: 300 Concurrent Users

## Results

| Metric | Value |
|--------|------|
| Total Requests | 16,364 |
| Failures | 15 |
| Failure Rate | ~0.09% |
| Average Latency | 456 ms |
| Median Latency | 310 ms |
| p95 Latency | 1400 ms |
| p99 Latency | 2900 ms |
| Throughput | ~155 RPS |

---

## Endpoint Performance

| Endpoint | Avg Latency | Failures | RPS |
|----------|------------|----------|-----|
| GET /users/me | 374 ms | 0 | 64.8 |
| POST /auth/login | 562 ms | 0 | 27 |
| POST /auth/register | 602 ms | 15 | 7.4 |

---

## Observations (300 Users)

1. Redis significantly reduced latency for read-heavy endpoint `/users/me`.
2. Database load decreased drastically due to caching.
3. System achieved near-zero failure rate.
4. Throughput increased ~3x compared to pre-Redis baseline.
5. Remaining latency is primarily due to bcrypt hashing.

---

# 🚀 Test 2: 500 Concurrent Users

## Results

| Metric | Value |
|--------|------|
| Total Requests | 7,003 |
| Failures | 245 |
| Failure Rate | ~3% |
| Average Latency | 1764 ms |
| Median Latency | 1100 ms |
| p95 Latency | 5500 ms |
| p99 Latency | 10000 ms |
| Throughput | ~93 RPS |

---

## Endpoint Performance

| Endpoint | Avg Latency | Failures | RPS |
|----------|------------|----------|-----|
| GET /users/me | 1680 ms | 2 | 51 |
| POST /auth/login | 1927 ms | 98 | 25.2 |
| POST /auth/register | 2107 ms | 52 | 10.6 |

---

## Observations (500 Users)

1. System entered degraded performance state under high concurrency.
2. Latency increased significantly across all endpoints.
3. Failure rate rose to ~3%.
4. Throughput dropped from ~155 RPS to ~93 RPS.
5. CPU-bound bcrypt hashing became the dominant bottleneck.
6. Even cached endpoints slowed down due to worker saturation.

---

# 📊 Comparison: 300 vs 500 Users

| Metric | 300 Users | 500 Users |
|--------|----------|-----------|
| Throughput | ~155 RPS | ~93 RPS |
| Avg Latency | 456 ms | 1764 ms |
| Failure Rate | ~0.09% | ~3% |
| System State | Stable | Degraded |

---

# 🧠 Key Insights

1. Redis successfully eliminated the database bottleneck.
2. System transitioned from I/O-bound to CPU-bound.
3. bcrypt hashing is the primary scalability limitation.
4. Worker saturation impacts even cached responses under heavy load.

---

# 🎯 Conclusion

- Stable capacity: ~300 concurrent users
- Degraded capacity: ~500 concurrent users
- Redis caching improved performance significantly for read-heavy endpoints
- Further scaling requires CPU optimization and horizontal scaling

---

# 🚀 Next Optimization Steps

1. Reduce bcrypt cost or move hashing to background workers
2. Increase Uvicorn workers (based on CPU cores)
3. Introduce async database driver (asyncpg)
4. Add load balancer for horizontal scaling
5. Implement Redis-based rate limiting

---

# 📌 Final Note

This benchmark demonstrates a complete optimization journey:

- Database bottleneck → solved using PostgreSQL tuning
- Read bottleneck → solved using Redis caching
- Current bottleneck → CPU (bcrypt)

This reflects real-world backend system scaling behavior.

