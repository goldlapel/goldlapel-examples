# Prepared Statement Cache

Gold Lapel caches prepared statements across query executions. When your application sends the same parameterized query multiple times (via the PostgreSQL extended protocol), GL suppresses redundant Parse messages and reuses the server-side prepared statement.

This eliminates ~0.5ms of parse+plan overhead per repeated query — significant for high-throughput applications.

## How It Works

```
First execution:  App → Parse(SQL) → GL → PG    (cache MISS, forwarded)
Second execution: App → Parse(SQL) → GL ✓        (cache HIT, suppressed)
                  App → Bind(params) → GL → PG   (forwarded with remapped name)
```

The client never knows — GL handles the statement name remapping transparently.

## Observing Cache Hits

Check the dashboard or CLI for `prepared_hits` and `prepared_misses`:

```bash
# Via CLI
goldlapel config --dashboard-port 7933

# Look for:
#   Prepared hits/misses    142/8
```

Or via Prometheus:
```
goldlapel_prepared_hits_total
goldlapel_prepared_misses_total
```

## Example

```python
import psycopg

# Connect through GL proxy
conn = psycopg.connect("host=localhost port=7932 dbname=mydb")

# This query template is parsed once, then cached
for user_id in range(100):
    conn.execute(
        "SELECT * FROM users WHERE id = %s",
        [user_id]
    )
    # First iteration: prepared_misses += 1 (Parse forwarded to PG)
    # Iterations 2-100: prepared_hits += 1 (Parse suppressed by GL)
```

## Describe Caching

GL also caches the ParameterDescription and RowDescription responses from Describe messages. Drivers that send Describe on every query (like psycopg3) benefit from an additional round-trip savings (~20-50us per query).

## Configuration

Prepared statement caching is enabled by default. To disable:

```bash
goldlapel --disable-prepared-cache
# or
GOLDLAPEL_DISABLE_PREPARED_CACHE=true
```

Cache size (max statements per connection):
```bash
goldlapel --prepared-cache-size 1024  # default
```
