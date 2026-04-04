# Benchmark Notes – Redis Integration

## Objective

Evaluate the impact of Redis caching on the FastAPI Authentication System under concurrent load and identify system bottlenecks after optimization.

---

## Context Before Redis

- Database (PostgreSQL) was the primary bottleneck
- High latency due to repeated DB lookups for authenticated endpoints
- High failure rate under load
- Limited throughput (~50 RPS)

---

## Redis Integration Strategy

Redis was introduced to optimize the read-heavy endpoint:

### Target Endpoint
- `GET /users/me`

### Caching Design

- Cache Key: `user:{user_id}`
- TTL: 300 seconds
- Storage Format: JSON (Pydantic serialized)

### Flow

1. Decode JWT → extract `user_id`
2. Check Redis:
   - HIT → return cached user
   - MISS → query DB → cache result → return

---

## Observed Impact

### 1. Latency Reduction

- `/users/me` latency significantly reduced due to cache hits
- Avoided repeated DB queries

### 2. Throughput Increase

- System throughput increased from ~50 RPS to ~150 RPS (3x improvement)

### 3. Failure Reduction

- Failure rate dropped to near zero under moderate load (300 users)

### 4. Database Load Reduction

- DB queries reduced drastically for authenticated requests

---

## Behavior at Higher Load (500 Users)

Despite Redis optimization, system showed degradation:

### Observations

- Increased latency across all endpoints
- Failure rate increased (~3%)
- Throughput dropped (~93 RPS)

### Root Cause

- CPU saturation due to bcrypt hashing
- Worker processes became overloaded
- Request queue buildup increased response times

---

## Bottleneck Shift

### Before Redis
- I/O-bound system (Database bottleneck)

### After Redis
- CPU-bound system (bcrypt hashing bottleneck)

---

## Key Learnings

1. Caching is highly effective for read-heavy endpoints
2. Removing one bottleneck exposes the next
3. System scalability depends on both I/O and CPU efficiency
4. Redis improves performance but does not solve CPU-bound operations
5. Load testing is essential to identify real bottlenecks

---

## Limitations

- bcrypt hashing remains expensive
- Synchronous request handling limits concurrency
- No horizontal scaling (single instance)

---

## Future Improvements

### High Priority

- Reduce bcrypt cost factor
- Offload hashing to background workers

### Medium Priority

- Introduce async database driver (asyncpg)
- Increase Uvicorn worker count (based on CPU cores)

### Advanced Scaling

- Add load balancer (Nginx)
- Deploy multiple FastAPI instances
- Implement Redis-based rate limiting

---

## Final Insight

This benchmark demonstrates a real-world scaling pattern:

1. Initial bottleneck: Database
2. Optimization: Redis caching
3. New bottleneck: CPU (bcrypt)

This progression reflects practical backend system design and performance engineering principles.

