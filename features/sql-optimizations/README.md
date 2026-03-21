# Gold Lapel — SQL Optimizations

A single script that walks through all of GL's automatic SQL optimization strategies. Run it, watch GL analyze your queries, and see the results in the dashboard.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the demo:
   ```bash
   python app.py
   ```

## What it covers

The script creates a realistic schema (customers, products, orders, order_items) and sends query patterns that trigger each optimization strategy:

| Strategy | What GL does |
|----------|-------------|
| **Materialized views** | Repeated join queries get a transparent matview — same results, faster reads |
| **Query rewriting** | Once a matview exists, GL rewrites queries to read from it automatically |
| **B-tree indexes** | Equality filters (`WHERE region = 'us-east'`) get a B-tree index |
| **Trigram indexes** | `LIKE`/`ILIKE` patterns get a GIN trigram index (via pg_trgm) |
| **Expression indexes** | Function calls in WHERE (`LOWER(email) = ...`) get an expression index |
| **Partial indexes** | Constant filters (`WHERE status = 'pending'`) get a partial index |
| **Deep pagination** | Large OFFSETs are flagged — GL suggests keyset pagination |
| **Result cache** | Identical read-only queries are served from an in-memory cache |
| **N+1 detection** | Rapid-fire identical queries (the N+1 loop) are flagged with a warning |
| **Batch prefetch** | After N+1 detection, GL prefetches all rows to serve future lookups from cache |

At the end, the script pulls strategy counters from the dashboard API and prints a summary.

Check the dashboard at http://localhost:7933 for matview details, index recommendations, and audit timeline.
