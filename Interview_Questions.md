# 🎯 PulseNotify — Interview Questions & Answers

> **Project:** Airtribe EventHub Project 4 — Flight Price Monitor & Alert System  
> A curated list of expected interview questions with detailed answers covering the system design and technical decisions behind PulseNotify.

---

## 1. Why PostgreSQL over SQLite?

**SQLite** is file-based and ideal for development or small applications.  
**PostgreSQL** is a client-server database that supports:

- Concurrent users
- Advanced indexing
- Transactions
- Scalability
- Production workloads

---

## 2. Why Redis?

Redis is used as:

- **Cache** for flight prices — reducing repetitive API calls to airline providers
- **Rate limiter** — to prevent API abuse and control request throughput

---

## 3. How does the scheduler work?

It uses **Celery Beat** (or Django Cron) to periodically wake up and trigger flight price checks for all tracked routes on a configured interval.

---

## 4. How do you handle rate limiting from airlines?

- Implement **exponential backoff** — retry with progressively longer delays
- Use a **token bucket algorithm** to control the rate of outgoing requests
- Queue requests and process them with controlled concurrency

---

## 5. What happens if the server crashes?

| Layer | Recovery Mechanism |
|---|---|
| Database schema | Django migrations ensure consistency on restart |
| Data integrity | Database transactions prevent partial writes |
| Scheduled tasks | Celery Beat's retry logic re-queues missed tasks |
| Cache | Redis snapshots (RDB/AOF) can restore state if persistence is enabled |

---

## 6. How do you scale this to thousands of users?

- **Horizontal scaling** — multiple Celery worker instances
- **Database read replicas** — offload read queries
- **Caching strategies** — Redis TTL-based caching to reduce DB load
- **Message queues** — RabbitMQ or Kafka for decoupling heavy operations

---

## 7. How do you handle timezone conversions?

> Always store timestamps in **UTC** in the database.  
> Convert to the user's local timezone **only in the frontend or API response layer**.

This avoids ambiguity during daylight saving changes and ensures consistent data storage.

---

## 8. How do you detect price drops?

Compare the **current price** fetched from the airline API with the **historical minimum price** stored in the database for that same route. If `current_price < historical_min`, trigger an alert.

---

## 9. Should Redis be persistent?

It depends on the use case:

| Mode | When to Use |
|---|---|
| **Persistent** (RDB snapshots / AOF logging) | Cache must survive restarts; critical cached data |
| **Non-persistent** | Cache misses are acceptable; saves memory & resources |

---

## 10. How do you prevent duplicate API calls to airlines?

1. Use a **Redis caching layer** with a short TTL (e.g., 5–10 minutes)
2. Before making an API call, **check if a recent response is cached** for that route
3. Apply **rate limiting** to cap the number of outgoing requests per time window

---

*Last updated: June 2026*
