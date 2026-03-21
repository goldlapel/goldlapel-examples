import time
import goldlapel
import psycopg

url = goldlapel.start("postgres://gl:gl@localhost:5432/todos", config={
    "min_pattern_count": 3,
    "report_interval_secs": 3,
})

conn = psycopg.connect(url)

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
print("Created customers and orders tables with seed data\n")

query = """
    SELECT c.name, o.total
    FROM customers c
    JOIN orders o ON o.customer_id = c.id
    WHERE c.region = 'us-east'
"""

print("=== Sending join query 5 times (building pattern) ===\n")
for i in range(1, 6):
    rows = conn.execute(query).fetchall()
    print(f"  run {i}: {len(rows)} rows returned")
    for row in rows:
        print(f"    {row[0]}: ${row[1]}")

print("\nWaiting 5 seconds for GL to create the matview...")
time.sleep(5)

print("\n=== Sending query again (should use matview now) ===\n")
rows = conn.execute(query).fetchall()
print(f"  {len(rows)} rows returned")
for row in rows:
    print(f"    {row[0]}: ${row[1]}")

print("\nQuery has now been optimized — check the dashboard for matview details.")
print("Dashboard: http://localhost:7933")

conn.close()
goldlapel.stop()
