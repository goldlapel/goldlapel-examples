import goldlapel
import psycopg

url = goldlapel.start("postgres://gl:gl@localhost:5432/todos", config={
    "n1_threshold": 5,
    "n1_window_ms": 2000,
})

conn = psycopg.connect(url)

conn.execute("DROP TABLE IF EXISTS customers")
conn.execute("""
    CREATE TABLE customers (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        region TEXT NOT NULL
    )
""")
for i in range(1, 11):
    region = "us-east" if i % 2 == 0 else "us-west"
    conn.execute("INSERT INTO customers (name, region) VALUES (%s, %s)", (f"Customer {i}", region))
conn.commit()
print("Created customers table with 10 rows\n")

# --- The N+1 anti-pattern ---
print("=== N+1 anti-pattern ===")
print("Fetching all customer IDs, then querying each one individually...\n")

ids = [row[0] for row in conn.execute("SELECT id FROM customers").fetchall()]

for cid in ids:
    row = conn.execute("SELECT id, name, region FROM customers WHERE id = %s", (cid,)).fetchone()
    print(f"  customer {row[0]}: {row[1]} ({row[2]})")

print("\nThat was 1 + 10 = 11 queries. GL should flag this as an N+1 pattern.")
print("Check GL logs for 'N+1 query pattern detected' warning.\n")

# --- The fix ---
print("=== The fix: single query ===")
rows = conn.execute("SELECT id, name, region FROM customers ORDER BY id").fetchall()
for row in rows:
    print(f"  customer {row[0]}: {row[1]} ({row[2]})")

print(f"\nSame data, 1 query instead of 11.")

conn.close()
goldlapel.stop()
