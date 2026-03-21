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

GL has 13 optimization strategies. The script demonstrates 11 of them directly:

| # | Strategy | What GL does | Demoed? |
|---|----------|-------------|---------|
| 1 | **Materialized views** | Repeated join queries get a transparent matview — precomputed results, fast reads | Yes |
| 2 | **Incremental matviews (IMMV)** | With pg_ivm installed, matviews update instantly on writes instead of periodic refresh | Automatic |
| 3 | **Matview consolidation** | Multiple similar matviews get merged into one wider view that serves both patterns | Automatic |
| 4 | **Query rewriting** | Queries that match a matview get transparently rewritten to SELECT from it | Yes |
| 5 | **B-tree indexes** | Equality/range filters (`WHERE region = 'us-east'`) get a B-tree index | Yes |
| 6 | **Trigram indexes** | `LIKE`/`ILIKE` patterns get a GIN trigram index (via pg_trgm) | Yes |
| 7 | **Expression indexes** | Function calls in WHERE (`LOWER(email) = ...`) get an expression index | Yes |
| 8 | **Partial indexes** | Constant filters (`WHERE status = 'pending'`) get a partial index | Yes |
| 9 | **Deep pagination detection** | Large OFFSETs are flagged — GL warns and can rewrite to keyset pagination | Yes |
| 10 | **Result cache** | Identical read-only queries served from an in-memory cache | Yes |
| 11 | **Prepared statement cache** | Repeated extended-protocol queries skip re-parsing | Automatic |
| 12 | **N+1 detection + batch prefetch** | Rapid-fire identical queries detected, then all rows prefetched into a batch cache | Yes |
| 13 | **Query coalescing** | Identical concurrent in-flight queries deduplicated — one executes, all get the result | Yes |

Strategies marked "Automatic" happen transparently — they don't need specific query patterns to trigger, but you can see their counters in the dashboard.

At the end, the script pulls strategy counters from the dashboard API and prints a summary.

Check the dashboard at http://localhost:7933 for matview details, index recommendations, and audit timeline.
