# 🧠 Benchmark Notes (PostgreSQL - Default Configuration)

## 🔍 Objective

Evaluate system performance after migrating from SQLite to PostgreSQL under concurrent load.

---

## 🚨 Key Finding

Migration to PostgreSQL did NOT eliminate failures.

Instead, the bottleneck shifted from:

- SQLite → DB locking issues

to:

- PostgreSQL → connection pool exhaustion

---

## ⚙️ What Happened Internally

### 1. SQLAlchemy Connection Pool Behavior

Default config:
- pool_size = 5
- max_overflow = 10
- max total connections ≈ 15

Under load:
- Each request requires DB connection
- Concurrent requests > 15
- New requests wait for free connection

---

### 2. Queueing Effect

When connections are exhausted:

1. Requests enter queue
2. Wait for connection
3. Queue grows
4. Latency increases exponentially

---

### 3. Timeout Failure

If wait > 30 seconds:

→ SQLAlchemy raises:
QueuePool limit reached --> TimeoutError

-> FastAPI return: 500 Internal Server Error

---

## 📉 Why Latency Became Huge (30–90s)

Because:

- Requests are NOT failing immediately
- They are WAITING in queue
- Then either:
  - get connection (very late)
  - OR timeout

👉 This inflates p95 and p99 dramatically

---

## 🔥 Why Failure Rate is High (~39%)

Because:

- Many requests exceed pool capacity
- Many hit timeout limit
- Setup endpoints (register/login) increase DB load early

---

## 🧠 Important Insight

PostgreSQL is NOT the bottleneck.

The bottleneck is:

👉 Application-level connection management

---

## ⚖️ SQLite vs PostgreSQL

| Aspect | SQLite | PostgreSQL |
|------|--------|------------|
| Concurrency | Poor | Good |
| Failure cause | DB locking | Pool exhaustion |
| Writes | Blocking | Parallel |
| Scalability | Limited | High |
| Bottleneck | DB engine | App configuration |

---

## 📌 System Behavior Pattern

1. Low load → works fine
2. Moderate load → queue forms
3. High load → pool exhaustion
4. Extreme load → timeouts + failures

---

## 🚀 What This Teaches

Real-world systems fail not only due to:
- database choice

but also due to:
- connection management
- resource limits
- request concurrency

---

## 🔧 Next Step (Optimization Plan)

To fix:

1. Increase connection pool size
2. Reduce DB dependency (caching)
3. Optimize auth flow (reduce DB hits)
4. Add async processing if needed

---

## 🎯 Key Takeaway

> Migrating to PostgreSQL solves database-level concurrency issues, but without proper connection pool tuning, the application still fails under load due to connection starvation.

---