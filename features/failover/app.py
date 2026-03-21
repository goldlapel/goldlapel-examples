import goldlapel
import psycopg
import time

url = goldlapel.start("postgres://gl:gl@localhost:5432/todos", config={
    "fallback": "postgres://gl:gl@localhost:5433/todos",
})

time.sleep(2)

print("=== Writing to primary ===")
with psycopg.connect(url) as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)")
    conn.execute("INSERT INTO todos (title) VALUES (%s)", ("Try Gold Lapel",))
    conn.commit()
    print("  Wrote 1 todo to primary")

print("\n>>> Now run: docker compose stop primary")
input(">>> Press Enter after stopping the primary...")

print("\n=== Reading after failover ===")
for attempt in range(5):
    try:
        with psycopg.connect(url) as conn:
            recovery = conn.execute("SELECT pg_is_in_recovery()").fetchone()[0]
            rows = conn.execute("SELECT id, title, done FROM todos ORDER BY id").fetchall()
            print(f"  Connected (recovery mode: {recovery}), {len(rows)} todo(s):")
            for row in rows:
                print(f"    {row}")
            break
    except Exception as e:
        print(f"  Attempt {attempt + 1}: {e}")
        time.sleep(1)

goldlapel.stop()
