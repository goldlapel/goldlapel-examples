import time
import goldlapel

UPSTREAM = "postgres://gl:gl@localhost:5432/todos"

conn = goldlapel.start(UPSTREAM)


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


# ─────────────────────────────────────────────────────────────
# 1. STREAM ADD
# ─────────────────────────────────────────────────────────────
section("1. Stream Add — append messages to a stream")

for i in range(5):
    msg_id = goldlapel.stream_add(conn, "events", {
        "type": "page_view",
        "path": f"/products/{i+1}",
        "user_id": (i % 3) + 1,
    })
    print(f"  stream_add → id={msg_id}")


# ─────────────────────────────────────────────────────────────
# 2. CREATE CONSUMER GROUP
# ─────────────────────────────────────────────────────────────
section("2. Create Consumer Group")

goldlapel.stream_create_group(conn, "events", "analytics")
print("  created group 'analytics'")

goldlapel.stream_create_group(conn, "events", "notifications")
print("  created group 'notifications'")


# ─────────────────────────────────────────────────────────────
# 3. STREAM READ — consume messages
# ─────────────────────────────────────────────────────────────
section("3. Stream Read — consume messages from a group")

messages = goldlapel.stream_read(conn, "events", "analytics", "worker-1", count=3)
print(f"  worker-1 read {len(messages)} messages:")
for msg in messages:
    print(f"    id={msg['id']}, payload={msg['payload']}")


# ─────────────────────────────────────────────────────────────
# 4. STREAM ACK — acknowledge processing
# ─────────────────────────────────────────────────────────────
section("4. Stream Ack — acknowledge processed messages")

for msg in messages:
    goldlapel.stream_ack(conn, "events", "analytics", msg["id"])
    print(f"  acked message id={msg['id']}")


# ─────────────────────────────────────────────────────────────
# 5. STREAM CLAIM — recover abandoned messages
# ─────────────────────────────────────────────────────────────
section("5. Stream Claim — recover abandoned messages")

# Read without acking (simulating a crashed worker)
abandoned = goldlapel.stream_read(conn, "events", "analytics", "worker-2", count=2)
print(f"  worker-2 read {len(abandoned)} messages (then 'crashed' without acking)")

# Another worker claims the idle messages
time.sleep(0.1)
claimed = goldlapel.stream_claim(conn, "events", "analytics", "worker-3", min_idle_ms=50)
print(f"  worker-3 claimed {len(claimed)} idle messages:")
for msg in claimed:
    print(f"    id={msg['id']}, payload={msg['payload']}")

# Ack the claimed messages
for msg in claimed:
    goldlapel.stream_ack(conn, "events", "analytics", msg["id"])
    print(f"  worker-3 acked id={msg['id']}")


# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────
section("Summary")
print("  5 stream methods demonstrated:")
print("    stream_add          — append messages to a stream")
print("    stream_create_group — create consumer groups")
print("    stream_read         — consume messages (at-least-once)")
print("    stream_ack          — acknowledge processing")
print("    stream_claim        — recover abandoned messages")
print("\n  Consumer groups, acknowledgment, crash recovery.")
print("  No Redis Streams. Just PostgreSQL.")

conn.close()
goldlapel.stop()
