import sys
import time
import goldlapel
import psycopg

mode = sys.argv[1] if len(sys.argv) > 1 else "transaction"
pool_size = int(sys.argv[2]) if len(sys.argv) > 2 else 20
print(f"Pool mode: {mode}, pool_size: {pool_size}")

url = goldlapel.start("postgres://gl:gl@localhost:5432/todos", config={
    "pool_mode": mode,
    "pool_size": pool_size,
})

pids = []
for i in range(10):
    with psycopg.connect(url) as conn:
        pid = conn.execute("SELECT pg_backend_pid()").fetchone()[0]
        pids.append(pid)
        print(f"  connection {i+1}: backend pid {pid}")
    time.sleep(0.1)

unique = len(set(pids))
print(f"\n{unique} unique backend PIDs across 10 sequential connections")
print(f"Pool mode: {mode} — {'connections reused between transactions' if mode == 'transaction' else 'each session pinned to its own backend'}")

goldlapel.stop()
