# LISTEN/NOTIFY Cache Invalidation

Gold Lapel automatically detects writes to your database and invalidates cached results. This works even for writes that bypass the proxy — GL uses PostgreSQL's logical decoding or trigger-based change detection to catch all mutations.

## How It Works

1. Application writes to table `orders` (through GL proxy or directly to PG)
2. GL detects the write via WAL monitoring or NOTIFY trigger
3. GL invalidates any cached matviews or result cache entries that depend on `orders`
4. Next read query for `orders` data fetches fresh results from PG

## Demo

```bash
# Terminal 1: Start GL with NOTIFY-based invalidation
goldlapel --upstream postgres://localhost:5432/mydb

# Terminal 2: Connect through GL and run a query (gets cached)
psql -h localhost -p 7932 -d mydb -c "SELECT count(*) FROM orders;"
# First run: hits PG
# Second run: served from cache (sub-ms)

# Terminal 3: Write DIRECTLY to PG (bypassing the proxy)
psql -h localhost -p 5432 -d mydb -c "INSERT INTO orders (data) VALUES ('{\"item\": \"test\"}');"

# Terminal 2: Query again through GL
psql -h localhost -p 7932 -d mydb -c "SELECT count(*) FROM orders;"
# GL detected the write and invalidated the cache — fetches fresh count
```

## Invalidation Methods

### NOTIFY (default)
GL installs lightweight triggers on monitored tables. Triggers fire `pg_notify()` on INSERT/UPDATE/DELETE. Zero configuration needed.

### Logical Decoding (advanced)
For high-write-volume tables where trigger overhead matters:

```bash
goldlapel --upstream postgres://localhost:5432/mydb --logical-decoding
```

Requires `wal_level = logical` in `postgresql.conf`. GL reads the WAL stream directly — no triggers needed, no per-row overhead.

## Cross-Instance Invalidation (Mesh)

When running multiple GL instances, a write detected by one instance propagates to all others via GL Mesh (P2P invalidation):

```bash
# Instance 1
goldlapel --upstream postgres://db:5432/mydb --mesh-peers instance2:7934

# Instance 2
goldlapel --upstream postgres://db:5432/mydb --mesh-peers instance1:7934
```

A write detected by Instance 1 invalidates caches on Instance 2 automatically.
