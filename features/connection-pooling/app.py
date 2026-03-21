import sys
import threading
import goldlapel
import psycopg

mode = sys.argv[1] if len(sys.argv) > 1 else "transaction"
pool_size = int(sys.argv[2]) if len(sys.argv) > 2 else (2 if mode == "transaction" else None)
print(f"Pool mode: {mode}, pool_size: {pool_size or 'default'}")

config = {"pool_mode": mode}
if pool_size is not None:
    config["pool_size"] = pool_size

url = goldlapel.start("postgres://gl:gl@localhost:5432/todos", config=config)

results = []

def worker(name):
    with psycopg.connect(url) as conn:
        pid = conn.execute("SELECT pg_backend_pid()").fetchone()[0]
        conn.execute("SELECT pg_sleep(0.1)")
        results.append((name, pid))

threads = [threading.Thread(target=worker, args=(f"worker-{i}",)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

for name, pid in sorted(results):
    print(f"  {name}: backend pid {pid}")

unique_pids = len(set(pid for _, pid in results))
pool_label = f"pool_size={pool_size}" if pool_size else "default pool_size"
print(f"\n{unique_pids} unique backend connections used by 5 workers ({pool_label})")

goldlapel.stop()
