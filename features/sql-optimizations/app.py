import json
import time
import urllib.request
import goldlapel
import psycopg

UPSTREAM = "postgres://gl:gl@localhost:5432/todos"

url = goldlapel.start(UPSTREAM, config={
    "min_pattern_count": 3,
    "report_interval_secs": 3,
    "n1_threshold": 5,
    "n1_window_ms": 2000,
    "enable_coalescing": True,
    "deep_pagination_threshold": 100,
})

conn = psycopg.connect(url)

# --- Schema setup ---

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

conn.commit()
print("Schema created: customers(50), products(20), orders(100), order_items(200)\n")


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
    print(f"  deep_pagination_warns:   {s.get('deep_pagination_warnings', 0)}")
    print(f"  coalesced:               {s.get('coalesced', 0)}")
except Exception as e:
    print(f"  (dashboard not available: {e})")

print(f"\nDashboard: http://localhost:7933")

conn.close()
goldlapel.stop()
