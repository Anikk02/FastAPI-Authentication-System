# Benchmark Notes – Phase 6

## 🚨 Most Important Insight

👉 System failure is driven by **burst traffic**, not total concurrency.

---

## What Worked

### ✅ Async Migration
- Eliminated blocking I/O
- Enabled scaling up to 800 users (steady load)

---

### ✅ Redis Caching
- Helped read-heavy endpoints
- Reduced DB pressure under normal conditions

---

### ✅ Connection Pool
- Handled steady traffic well

---

## What Failed

### ❌ Burst Handling (Critical Failure)

| Users | Spawn Rate | Result |
|------|-----------|--------|
| 400  | 5         | ✅ Stable |
| 400  | 10        | ❌ 14% failure |

👉 This is a **real-world production failure scenario**

---

## Why It Failed

### 1. DB Pool Saturation
- Too many concurrent queries instantly
- Pool exhausted → requests queued → timeouts

---

### 2. CPU Bottleneck (bcrypt)

- Login/Register became extremely slow (~10–12s)
- Async cannot optimize CPU-bound tasks

---

### 3. No Backpressure Mechanism

System accepts all requests → leads to:
- Queue explosion
- Latency amplification
- Failure cascade

---

## Failure Chain
Traffic Spike
↓
Too many concurrent requests
↓
DB pool exhausted
↓
Requests queued
↓
Latency ↑↑↑
↓
Timeouts + Failures

### 🔹 Async ≠ Scalable by default
- DB + CPU still limit performance

---

### 🔹 Burst handling is a separate problem
- Requires:
  - Rate limiting
  - Load shedding
  - Queueing

---

### 🔹 Reads vs Writes

| Type  | Behavior |
|------|---------|
| Reads | Stable |
| Writes | Collapse under load |

---
