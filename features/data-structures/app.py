import json
import time
import threading
import goldlapel

UPSTREAM = "postgres://gl:gl@localhost:5432/todos"

conn = goldlapel.start(UPSTREAM)


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


# ─────────────────────────────────────────────────────────────
# 1. COUNTERS
# ─────────────────────────────────────────────────────────────
section("1. Counters — incr / get_counter")

val = goldlapel.incr(conn, "page_views", "home")
print(f"  incr('page_views', 'home')     → {val}")
val = goldlapel.incr(conn, "page_views", "home")
print(f"  incr('page_views', 'home')     → {val}")
val = goldlapel.incr(conn, "page_views", "home", 10)
print(f"  incr('page_views', 'home', 10) → {val}")
val = goldlapel.get_counter(conn, "page_views", "home")
print(f"  get_counter('page_views', 'home') → {val}")


# ─────────────────────────────────────────────────────────────
# 2. HASHES
# ─────────────────────────────────────────────────────────────
section("2. Hashes — hset / hget / hgetall / hdel")

goldlapel.hset(conn, "user_prefs", "user:1", "theme", "dark")
goldlapel.hset(conn, "user_prefs", "user:1", "lang", "en")
goldlapel.hset(conn, "user_prefs", "user:1", "timezone", "US/Eastern")

theme = goldlapel.hget(conn, "user_prefs", "user:1", "theme")
print(f"  hget('user_prefs', 'user:1', 'theme') → {theme}")

all_prefs = goldlapel.hgetall(conn, "user_prefs", "user:1")
print(f"  hgetall('user_prefs', 'user:1') → {all_prefs}")

deleted = goldlapel.hdel(conn, "user_prefs", "user:1", "timezone")
print(f"  hdel('user_prefs', 'user:1', 'timezone') → {deleted}")

all_prefs = goldlapel.hgetall(conn, "user_prefs", "user:1")
print(f"  hgetall after hdel → {all_prefs}")


# ─────────────────────────────────────────────────────────────
# 3. SORTED SETS
# ─────────────────────────────────────────────────────────────
section("3. Sorted Sets — zadd / zincrby / zrange / zrank / zscore / zrem")

goldlapel.zadd(conn, "leaderboard", "alice", 100)
goldlapel.zadd(conn, "leaderboard", "bob", 85)
goldlapel.zadd(conn, "leaderboard", "carol", 92)

new_score = goldlapel.zincrby(conn, "leaderboard", "bob", 20)
print(f"  zincrby('leaderboard', 'bob', 20) → {new_score}")

top = goldlapel.zrange(conn, "leaderboard", 0, 3, desc=True)
print(f"  zrange (top 3 desc): {top}")

rank = goldlapel.zrank(conn, "leaderboard", "carol", desc=True)
print(f"  zrank('carol', desc=True) → {rank}")

score = goldlapel.zscore(conn, "leaderboard", "alice")
print(f"  zscore('alice') → {score}")

removed = goldlapel.zrem(conn, "leaderboard", "bob")
print(f"  zrem('bob') → {removed}")


# ─────────────────────────────────────────────────────────────
# 4. QUEUES
# ─────────────────────────────────────────────────────────────
section("4. Queues — enqueue / dequeue")

goldlapel.enqueue(conn, "jobs", {"type": "email", "to": "user@example.com", "subject": "Welcome"})
goldlapel.enqueue(conn, "jobs", {"type": "resize", "image_id": 42, "width": 800})
goldlapel.enqueue(conn, "jobs", {"type": "webhook", "url": "https://example.com/hook"})

job1 = goldlapel.dequeue(conn, "jobs")
print(f"  dequeue → {job1}")
job2 = goldlapel.dequeue(conn, "jobs")
print(f"  dequeue → {job2}")


# ─────────────────────────────────────────────────────────────
# 5. PUB/SUB
# ─────────────────────────────────────────────────────────────
section("5. Pub/Sub — publish / subscribe")

received = []

def on_message(channel, payload):
    received.append(payload)
    print(f"  subscriber received: channel={channel}, payload={payload}")

t = goldlapel.subscribe(conn, "notifications", on_message, blocking=False)
time.sleep(0.5)

goldlapel.publish(conn, "notifications", "Hello from Gold Lapel!")
goldlapel.publish(conn, "notifications", json.dumps({"event": "user_signup", "id": 42}))
time.sleep(1)

print(f"  total messages received: {len(received)}")


# ─────────────────────────────────────────────────────────────
# 6. GEOSPATIAL
# ─────────────────────────────────────────────────────────────
section("6. Geospatial — geoadd / georadius / geodist")

goldlapel.geoadd(conn, "locations", "name", "geom", "Empire State Building", -73.9857, 40.7484)
goldlapel.geoadd(conn, "locations", "name", "geom", "Times Square", -73.9855, 40.7580)
goldlapel.geoadd(conn, "locations", "name", "geom", "Central Park", -73.9654, 40.7829)
goldlapel.geoadd(conn, "locations", "name", "geom", "Brooklyn Bridge", -73.9969, 40.7061)

nearby = goldlapel.georadius(conn, "locations", "geom", -73.985, 40.750, 2000, limit=10)
print(f"  georadius (2km from midtown): {len(nearby)} results")
for loc in nearby:
    print(f"    {loc['name']}: {loc['distance_m']:.0f}m away")

dist = goldlapel.geodist(conn, "locations", "geom", "name", "Empire State Building", "Brooklyn Bridge")
print(f"  geodist(Empire State → Brooklyn Bridge): {dist:.0f}m")


# ─────────────────────────────────────────────────────────────
# 7. MISC
# ─────────────────────────────────────────────────────────────
section("7. Misc — count_distinct / script")

conn.execute("DROP TABLE IF EXISTS events")
conn.execute("CREATE TABLE events (id SERIAL, category TEXT, value INT)")
for cat in ["click", "view", "click", "purchase", "view", "view", "click"]:
    conn.execute("INSERT INTO events (category, value) VALUES (%s, %s)", (cat, 1))
conn.commit()

distinct = goldlapel.count_distinct(conn, "events", "category")
print(f"  count_distinct('events', 'category') → {distinct}")

print("\n  script() requires pllua extension — skipping in this example.")
print("  See docs/extensions for pllua installation instructions.")


# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────
section("Summary")
print("  21 data structure methods demonstrated:")
print("    Counters:    incr, get_counter")
print("    Hashes:      hset, hget, hgetall, hdel")
print("    Sorted Sets: zadd, zincrby, zrange, zrank, zscore, zrem")
print("    Queues:      enqueue, dequeue")
print("    Pub/Sub:     publish, subscribe")
print("    Geo:         geoadd, georadius, geodist")
print("    Misc:        count_distinct, script (requires pllua)")
print("\n  All backed by PostgreSQL. No additional infrastructure.")

conn.close()
goldlapel.stop()
