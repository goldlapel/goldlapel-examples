import time
import goldlapel
import psycopg

url = goldlapel.start("postgres://gl:gl@localhost:5432/todos", config={
    "min_pattern_count": 3,
    "report_interval_secs": 3,
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
    region = "us-east" if i <= 5 else "us-west"
    conn.execute("INSERT INTO customers (name, region) VALUES (%s, %s)", (f"Customer {i}", region))
conn.commit()
print("Created customers table with 10 rows\n")

# --- Normal queries (GL tracks these) ---
print("=== Normal queries (tracked by GL) ===\n")
for i in range(1, 6):
    rows = conn.execute("SELECT name FROM customers WHERE region = 'us-east'").fetchall()
    print(f"  run {i}: {[row[0] for row in rows]}")

# --- Skipped queries (GL ignores these) ---
print("\n=== Annotated queries (invisible to GL) ===\n")
for i in range(1, 6):
    rows = conn.execute("/* goldlapel:skip */ SELECT name FROM customers WHERE region = 'us-east'").fetchall()
    print(f"  run {i}: {[row[0] for row in rows]}")

print("\nWaiting 5 seconds for stats to accumulate...")
time.sleep(5)

print("\nThe first query (without skip) was tracked by GL — check dashboard.")
print("The second query (with /* goldlapel:skip */) was completely invisible to GL.")
print("Dashboard: http://localhost:7933")

conn.close()
goldlapel.stop()
