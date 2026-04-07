## Severe Load Analysis(SQLite Database)

Under the SQLite-based setup, the system became unstable at 100 concurrent users with a spawn rate of 10 users/sec.

### Measured Outcome
- Total Requests: 677
- Failures: 263
- Failure Rate: ~38.8%
- Average Latency: ~45.4 seconds
- Maximum Latency: ~91.3 seconds
- Throughput: ~1.92 requests/sec

### What this indicates
This is not a minor slowdown. It is a collapse pattern caused by:
- SQLite write contention and locking
- queue buildup under concurrent load
- CPU overhead from bcrypt hashing and verification
- single backend instance limitations

### Key Insight
The system initially handled traffic, but once request arrival rate exceeded processing capacity, queued requests accumulated rapidly. This caused extreme latency growth, reduced throughput, and a high failure rate.