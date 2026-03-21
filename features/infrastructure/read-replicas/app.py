import goldlapel
import psycopg
import time

url = goldlapel.start("postgres://gl:gl@localhost:5432/todos", config={
    "replica": "postgres://gl:gl@localhost:5433/todos",
})

# Give the replica a moment to start streaming
time.sleep(2)

print("=== Write (goes to primary) ===")
with psycopg.connect(url) as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)")
    conn.execute("INSERT INTO todos (title) VALUES (%s)", ("Try Gold Lapel",))
    conn.commit()

    recovery = conn.execute("SELECT pg_is_in_recovery()").fetchone()[0]
    print(f"  Read after write on same connection — replica? {recovery}")

print("\n=== Read on fresh connection (should route to replica) ===")
with psycopg.connect(url) as conn:
    recovery = conn.execute("SELECT pg_is_in_recovery()").fetchone()[0]
    print(f"  Fresh connection read — replica? {recovery}")
    for row in conn.execute("SELECT id, title, done FROM todos ORDER BY id"):
        print(f"  {row}")

goldlapel.stop()
