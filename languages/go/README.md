# Gold Lapel — Go Wrapper

Minimal example showing Gold Lapel optimizing Postgres queries via the Go wrapper.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Fetch dependencies:
   ```bash
   go mod tidy
   ```

3. Run the app:
   ```bash
   go run .
   ```

## What to look for

The app calls `goldlapel.Start(ctx, upstream, opts...)`, which spawns the
proxy and returns a `*GoldLapel`. `gl.URL()` is the proxy connection string —
pass it to `pgx.Connect` (or any Postgres driver) for raw SQL. The same
instance also exposes wrapper methods (`gl.DocInsert`, `gl.Search`, etc.)
directly.

`defer gl.Close()` sends SIGTERM to the proxy and waits for it to exit.

As GL observes queries, it creates optimizations (indexes, matviews, query
rewrites) in the background. Check the dashboard at http://localhost:7933
to see what it found.
