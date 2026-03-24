import time
import json
import urllib.request
import goldlapel

conn = goldlapel.start("postgres://gl:gl@localhost:5432/todos")

conn.execute("DROP TABLE IF EXISTS orders")
conn.execute("DROP TABLE IF EXISTS customers")
conn.execute("""
    CREATE TABLE customers (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        region TEXT NOT NULL
    )
""")
conn.execute("""
    CREATE TABLE orders (
        id SERIAL PRIMARY KEY,
        customer_id INTEGER REFERENCES customers(id),
        total NUMERIC(10, 2) NOT NULL
    )
""")
for i in range(1, 11):
    region = "us-east" if i <= 5 else "us-west"
    conn.execute("INSERT INTO customers (name, region) VALUES (%s, %s)", (f"Customer {i}", region))
for i in range(1, 11):
    conn.execute("INSERT INTO orders (customer_id, total) VALUES (%s, %s)", (((i - 1) % 10) + 1, round(50 + i * 12.5, 2)))
conn.commit()
print("Created tables with seed data")

print("Sending join query 5 times to generate traffic...\n")
for i in range(5):
    conn.execute("""
        SELECT c.name, o.total
        FROM customers c
        JOIN orders o ON o.customer_id = c.id
        WHERE c.region = 'us-east'
    """).fetchall()

conn.close()

print("Waiting 5 seconds for stats to accumulate...\n")
time.sleep(5)

# --- /api/stats ---
print("=== GET /api/stats ===\n")
resp = urllib.request.urlopen("http://localhost:7933/api/stats")
stats = json.loads(resp.read())
print(f"  mode:              {stats.get('mode', 'n/a')}")
print(f"  version:           {stats.get('version', 'n/a')}")
print(f"  queries_observed:  {stats.get('queries_observed', 'n/a')}")
print(f"  queries_rewritten: {stats.get('queries_rewritten', 'n/a')}")

# --- /api/audit ---
print("\n=== GET /api/audit ===\n")
resp = urllib.request.urlopen("http://localhost:7933/api/audit")
audit = json.loads(resp.read())
events = audit if isinstance(audit, list) else audit.get("events", [])
for event in events[:5]:
    print(f"  [{event.get('timestamp', '')}] {event.get('category', '')}: {event.get('action', '')}")
if not events:
    print("  (no audit events yet)")

# --- /api/export ---
print("\n=== GET /api/export ===\n")
resp = urllib.request.urlopen("http://localhost:7933/api/export")
export = json.loads(resp.read())
print(f"  schema_version: {export.get('schema_version', 'n/a')}")
patterns = export.get("patterns", [])
matviews = export.get("matviews", [])
print(f"  patterns:       {len(patterns)}")
print(f"  matviews:       {len(matviews)}")

print("\nDashboard: http://localhost:7933")

goldlapel.stop()
