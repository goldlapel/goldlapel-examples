# Bellhop vs Waiter Mode

Gold Lapel has two operating modes:

- **Waiter** (default) — full optimization: materialized views, query rewriting, caching, N+1 detection, write acceleration
- **Bellhop** — observe only: queries pass through unmodified, but GL still collects patterns and statistics

Bellhop mode is your kill switch. If something goes wrong, flip to Bellhop and GL becomes a transparent passthrough — zero impact on your queries.

## Usage

```bash
# Start in Waiter mode (default — full optimization)
goldlapel --upstream postgres://localhost:5432/mydb

# Start in Bellhop mode (observe only)
goldlapel --upstream postgres://localhost:5432/mydb --mode bellhop

# Or via environment variable
GOLDLAPEL_MODE=bellhop goldlapel --upstream postgres://localhost:5432/mydb
```

## Live Toggle

Switch modes without restarting — edit `goldlapel.toml`:

```toml
mode = "bellhop"   # switch to observe-only
```

GL detects the change and switches immediately. Switch back:

```toml
mode = "waiter"    # resume full optimization
```

## Dashboard Toggle

You can also toggle via the dashboard API:

```bash
# Switch to bellhop
curl -X POST http://localhost:7933/api/settings \
  -H "Content-Type: application/json" \
  -d '{"key": "mode", "value": "bellhop"}'

# Switch back to waiter
curl -X POST http://localhost:7933/api/settings \
  -H "Content-Type: application/json" \
  -d '{"key": "mode", "value": "waiter"}'
```

## When to Use Bellhop

- **Debugging** — suspect GL is causing an issue? Flip to Bellhop. If the issue disappears, report it.
- **Maintenance windows** — deploying schema changes? Bellhop prevents GL from creating matviews on transient patterns.
- **Gradual rollout** — start in Bellhop to observe patterns, then switch to Waiter when confident.

## What Bellhop Still Does

Even in Bellhop mode, GL continues to:
- Observe and log query patterns
- Track statistics (queries/sec, pattern frequency)
- Serve the dashboard
- Pool connections (if pooling is enabled)

It just doesn't create matviews, rewrite queries, or serve cached results.
