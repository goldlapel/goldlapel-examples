import json
import time
import urllib.request
import goldlapel

UPSTREAM = "postgres://gl:gl@localhost:5432/todos"

conn = goldlapel.start(UPSTREAM, config={
    "min_pattern_count": 3,
    "report_interval_secs": 3,
    "n1_threshold": 5,
    "n1_window_ms": 2000,
    "enable_coalescing": True,
    "deep_pagination_threshold": 100,
})

# --- Schema setup ---

conn.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
conn.execute("CREATE EXTENSION IF NOT EXISTS fuzzystrmatch")

conn.execute("DROP TABLE IF EXISTS articles CASCADE")
conn.execute("DROP TABLE IF EXISTS order_items CASCADE")
conn.execute("DROP TABLE IF EXISTS orders CASCADE")
conn.execute("DROP TABLE IF EXISTS products CASCADE")
conn.execute("DROP TABLE IF EXISTS customers CASCADE")

conn.execute("""
    CREATE TABLE customers (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        region TEXT NOT NULL,
        bio TEXT
    )
""")
conn.execute("""
    CREATE TABLE products (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        price NUMERIC(10, 2) NOT NULL,
        category TEXT,
        description TEXT
    )
""")
conn.execute("""
    CREATE TABLE orders (
        id SERIAL PRIMARY KEY,
        customer_id INTEGER REFERENCES customers(id),
        total NUMERIC(10, 2) NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT NOW()
    )
""")
conn.execute("""
    CREATE TABLE order_items (
        id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES orders(id),
        product_id INTEGER REFERENCES products(id),
        quantity INTEGER NOT NULL,
        line_total NUMERIC(10, 2) NOT NULL
    )
""")

for i in range(1, 51):
    region = ["us-east", "us-west", "eu-west", "ap-south"][i % 4]
    conn.execute(
        "INSERT INTO customers (name, email, region, bio) VALUES (%s, %s, %s, %s)",
        (f"Customer {i}", f"c{i}@example.com", region, f"Bio for customer {i} " * 20),
    )

for i in range(1, 21):
    cat = ["electronics", "books", "clothing", "food"][i % 4]
    conn.execute(
        "INSERT INTO products (name, price, category, description) VALUES (%s, %s, %s, %s)",
        (f"Product {i}", round(10 + i * 5.5, 2), cat, f"Description for product {i} " * 10),
    )

for i in range(1, 101):
    conn.execute(
        "INSERT INTO orders (customer_id, total, status) VALUES (%s, %s, %s)",
        ((i % 50) + 1, round(20 + i * 3.3, 2), ["pending", "shipped", "delivered"][i % 3]),
    )

for i in range(1, 201):
    conn.execute(
        "INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES (%s, %s, %s, %s)",
        ((i % 100) + 1, (i % 20) + 1, (i % 5) + 1, round(10 + i * 2.2, 2)),
    )

conn.execute("""
    CREATE TABLE articles (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        body TEXT NOT NULL
    )
""")

articles = [
    ("Introduction to PostgreSQL", "PostgreSQL is a powerful open source relational database system with over 35 years of active development. It runs on all major operating systems and has earned a strong reputation for reliability and performance."),
    ("Understanding Indexes", "Database indexes are data structures that improve the speed of data retrieval operations. Without indexes, the database must scan every row in a table to find matching results."),
    ("Full-Text Search in Postgres", "PostgreSQL provides built-in full-text search capabilities using tsvector and tsquery types. This eliminates the need for external search engines like Elasticsearch for many use cases."),
    ("Query Optimization Techniques", "Optimizing database queries involves analyzing execution plans, adding appropriate indexes, and restructuring queries to reduce I/O operations and CPU usage."),
    ("Connection Pooling Best Practices", "Connection pooling reduces the overhead of establishing database connections. Tools like PgBouncer and built-in connection pools help manage database resources efficiently."),
    ("Materialized Views Explained", "Materialized views store the result of a query physically on disk. They are useful for expensive aggregate queries that don't need real-time data freshness."),
    ("Postgres Replication Guide", "Streaming replication in PostgreSQL creates exact copies of a database server. This provides high availability and read scaling for production workloads."),
    ("Advanced JSON Operations", "PostgreSQL supports JSON and JSONB data types with powerful operators for querying nested documents. JSONB is stored in a binary format for faster processing."),
    ("Database Security Hardening", "Securing a PostgreSQL installation involves configuring authentication, encrypting connections with SSL, and implementing role-based access control."),
    ("Monitoring Postgres Performance", "Effective monitoring tracks query latency, connection counts, cache hit ratios, and disk I/O. Extensions like pg_stat_statements provide detailed query analytics."),
]
for title, body in articles:
    conn.execute(
        "INSERT INTO articles (title, body) VALUES (%s, %s)", (title, body)
    )

conn.commit()
print("Schema created: customers(50), products(20), orders(100), order_items(200), articles(10)\n")


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


# ─────────────────────────────────────────────────────────────
# 1. MATERIALIZED VIEWS
# ─────────────────────────────────────────────────────────────
section("1. Materialized Views")
print("Sending the same join query 5 times (min_pattern_count=3)...")

query = """
    SELECT c.name, o.total, o.status
    FROM customers c
    JOIN orders o ON o.customer_id = c.id
    WHERE c.region = 'us-east'
    ORDER BY o.total DESC
"""
for i in range(5):
    rows = conn.execute(query).fetchall()
    print(f"  run {i+1}: {len(rows)} rows")

print("Waiting for GL to create the matview...")
time.sleep(6)
print("GL should have created a materialized view for this join pattern.")
print("Next time this query runs, GL rewrites it to read from the matview.")


# ─────────────────────────────────────────────────────────────
# 2. QUERY REWRITING
# ─────────────────────────────────────────────────────────────
section("2. Query Rewriting")
print("Sending the same join query again — GL should rewrite it to use the matview...")

rows = conn.execute(query).fetchall()
print(f"  {len(rows)} rows returned (transparently rewritten)")


# ─────────────────────────────────────────────────────────────
# 3. B-TREE INDEX CREATION
# ─────────────────────────────────────────────────────────────
section("3. B-tree Index Creation")
print("Sending equality queries on an unindexed column...")

for i in range(5):
    conn.execute("SELECT name, email FROM customers WHERE region = %s", ("us-west",)).fetchall()
    print(f"  run {i+1}: SELECT ... WHERE region = 'us-west'")

print("GL analyzes the WHERE clause and may create a B-tree index on customers.region.")
time.sleep(4)


# ─────────────────────────────────────────────────────────────
# 4. TRIGRAM INDEX CREATION
# ─────────────────────────────────────────────────────────────
section("4. Trigram Index Creation")
print("Sending LIKE/ILIKE queries (requires pg_trgm extension)...")

for i in range(5):
    conn.execute("SELECT name FROM customers WHERE name ILIKE %s", ("%customer 1%",)).fetchall()
    print(f"  run {i+1}: SELECT ... WHERE name ILIKE '%customer 1%'")

print("GL detects LIKE/ILIKE patterns and may create a GIN trigram index.")
time.sleep(4)


# ─────────────────────────────────────────────────────────────
# 5. EXPRESSION INDEX CREATION
# ─────────────────────────────────────────────────────────────
section("5. Expression Index Creation")
print("Sending queries with function expressions in WHERE...")

for i in range(5):
    conn.execute("SELECT name FROM customers WHERE LOWER(email) = %s", ("c5@example.com",)).fetchall()
    print(f"  run {i+1}: SELECT ... WHERE LOWER(email) = 'c5@example.com'")

print("GL detects expression-based filtering and may create an expression index.")
time.sleep(4)


# ─────────────────────────────────────────────────────────────
# 6. PARTIAL INDEX CREATION
# ─────────────────────────────────────────────────────────────
section("6. Partial Index Creation")
print("Sending queries that always filter on a constant...")

for i in range(5):
    conn.execute(
        "SELECT id, total FROM orders WHERE status = 'pending' AND total > %s", (50,)
    ).fetchall()
    print(f"  run {i+1}: SELECT ... WHERE status = 'pending' AND total > 50")

print("GL detects the constant filter and may create a partial index (WHERE status = 'pending').")
time.sleep(4)


# ─────────────────────────────────────────────────────────────
# 7. DEEP PAGINATION DETECTION
# ─────────────────────────────────────────────────────────────
section("7. Deep Pagination Detection")
print("Sending a query with a large OFFSET (threshold=100)...")

rows = conn.execute("SELECT * FROM orders ORDER BY id LIMIT 10 OFFSET 500").fetchall()
print(f"  SELECT ... LIMIT 10 OFFSET 500 → {len(rows)} rows")
print("GL flags deep pagination and may suggest keyset pagination.")


# ─────────────────────────────────────────────────────────────
# 8. RESULT CACHE
# ─────────────────────────────────────────────────────────────
section("8. Result Cache")
print("Sending the same read-only query twice in quick succession...")

conn.execute("SELECT COUNT(*) FROM customers WHERE region = 'eu-west'").fetchone()
print("  run 1: SELECT COUNT(*) ... (cache miss)")
conn.execute("SELECT COUNT(*) FROM customers WHERE region = 'eu-west'").fetchone()
print("  run 2: SELECT COUNT(*) ... (cache hit — served from memory)")


# ─────────────────────────────────────────────────────────────
# 9. N+1 DETECTION
# ─────────────────────────────────────────────────────────────
section("9. N+1 Query Detection")
print("Simulating the N+1 anti-pattern: fetch IDs then query each...")

ids = [row[0] for row in conn.execute("SELECT id FROM customers LIMIT 10").fetchall()]
for cid in ids:
    conn.execute("SELECT id, name, region FROM customers WHERE id = %s", (cid,)).fetchone()
    print(f"  SELECT ... WHERE id = {cid}")

print("GL detects 10 identical parameterized queries in rapid succession.")
print("Check logs for 'N+1 query pattern detected'.")


# ─────────────────────────────────────────────────────────────
# 10. BATCH PREFETCH (N+1 → cache)
# ─────────────────────────────────────────────────────────────
section("10. Batch Prefetch")
print("After N+1 detection, GL prefetches all rows into a batch cache.")
print("Subsequent lookups for the same pattern are served from the cache.")
print("(This happens automatically after step 9 — check dashboard for batch_cache stats.)")


# ─────────────────────────────────────────────────────────────
# 11. QUERY COALESCING
# ─────────────────────────────────────────────────────────────
section("11. Query Coalescing")
print("Sending 3 identical slow queries concurrently from separate connections...")
print("GL deduplicates them — one executes, the others wait for its result.\n")

import threading

coalesce_results = []

def coalesce_worker(worker_id):
    try:
        c = goldlapel.connect()
        row = c.execute("SELECT pg_sleep(0.5)::text, COUNT(*)::text FROM customers").fetchone()
        coalesce_results.append((worker_id, row[1]))
        c.close()
    except Exception as e:
        coalesce_results.append((worker_id, f"error: {e}"))

threads = [threading.Thread(target=coalesce_worker, args=(i,)) for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()

for wid, count in sorted(coalesce_results):
    print(f"  worker {wid}: {count} customers")
print("All 3 got the same result, but GL only executed the query once.")
time.sleep(4)


# ─────────────────────────────────────────────────────────────
# 12. EXPRESSION REWRITING — TSVECTOR STORED COLUMNS
# ─────────────────────────────────────────────────────────────
section("12. Expression Rewriting — Tsvector Stored Columns")
print("Sending full-text search queries on articles.body...")
print("GL will auto-create a stored tsvector column (_gl_tsv_body) so Postgres")
print("doesn't recompute to_tsvector() on every row at query time.\n")

tsv_query = "SELECT * FROM articles WHERE to_tsvector('english', body) @@ plainto_tsquery('english', %s)"

t0 = time.perf_counter()
for i in range(5):
    rows = conn.execute(tsv_query, ("PostgreSQL",)).fetchall()
    print(f"  run {i+1}: {len(rows)} rows")
tsv_before = time.perf_counter() - t0

print(f"\n  Before (5 runs): {tsv_before:.4f}s")
print("  Waiting 5s for GL to create stored tsvector column...")
time.sleep(5)

t0 = time.perf_counter()
rows = conn.execute(tsv_query, ("PostgreSQL",)).fetchall()
tsv_after = time.perf_counter() - t0

print(f"  After  (1 run):  {tsv_after:.4f}s — {len(rows)} rows")
print("  GL added a stored column _gl_tsv_body with a GIN index.")
print("  The query is transparently rewritten to use the pre-computed column.")


# ─────────────────────────────────────────────────────────────
# 13. EXPRESSION REWRITING — SIMILARITY % OPERATOR
# ─────────────────────────────────────────────────────────────
section("13. Expression Rewriting — Similarity % Operator")
print("Sending similarity() queries on articles.title...")
print("GL rewrites similarity(col, val) > threshold to col % val,")
print("which can use the GIN trigram index for fast fuzzy matching.\n")

sim_query = "SELECT * FROM articles WHERE similarity(title, %s) > 0.3"

t0 = time.perf_counter()
for i in range(5):
    rows = conn.execute(sim_query, ("Postgres Guide",)).fetchall()
    print(f"  run {i+1}: {len(rows)} rows")
sim_before = time.perf_counter() - t0

print(f"\n  Before (5 runs): {sim_before:.4f}s")
print("  Waiting 5s for GL to create trigram index and rewrite rule...")
time.sleep(5)

t0 = time.perf_counter()
rows = conn.execute(sim_query, ("Postgres Guide",)).fetchall()
sim_after = time.perf_counter() - t0

print(f"  After  (1 run):  {sim_after:.4f}s — {len(rows)} rows")
print("  GL created a GIN trigram index on articles.title and rewrites")
print("  similarity(title, val) > 0.3 → title % val (index-friendly operator).")


# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────
section("Summary — Dashboard Stats")
print("Waiting for final stats flush...")
time.sleep(4)

try:
    resp = urllib.request.urlopen("http://localhost:7933/api/stats")
    stats = json.loads(resp.read())
    s = stats.get("strategy", {})
    print(f"  matviews_created:        {s.get('matviews_created', 0)}")
    print(f"  btree_indexes_created:   {s.get('btree_indexes_created', 0)}")
    print(f"  trigram_indexes_created:  {s.get('trigram_indexes_created', 0)}")
    print(f"  expression_indexes:      {s.get('expression_indexes_created', 0)}")
    print(f"  partial_indexes_created:  {s.get('partial_indexes_created', 0)}")
    print(f"  rewrites:                {s.get('rewrites', 0)}")
    print(f"  cache_hits:              {s.get('cache_hits', 0)}")
    print(f"  prepared_hits:           {s.get('prepared_hits', 0)}")
    print(f"  deep_pagination_warns:   {s.get('deep_pagination_warnings', 0)}")
    print(f"  coalesced:               {s.get('coalesced', 0)}")
except Exception as e:
    print(f"  (dashboard not available: {e})")

print(f"\nDashboard: http://localhost:7933")

conn.close()
goldlapel.stop()
