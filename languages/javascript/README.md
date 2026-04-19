# Gold Lapel — JavaScript Wrapper

Minimal todo app showing Gold Lapel's Node.js wrapper with the `pg` driver.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the app:
   ```bash
   node app.js
   ```

## What to look for

The app calls `await goldlapel.start(upstream)`, which spawns the proxy and
returns a `GoldLapel` instance. `gl.url` is the proxy connection string —
pass it to any Postgres driver. The same instance exposes wrapper methods
(`gl.docInsert`, `gl.search`, etc.) directly.

On Node 22+ you can also write `await using gl = await goldlapel.start(...)`
to auto-stop the proxy at scope end. On older Node, call `await gl.stop()`
explicitly (shown in the example).

As GL observes queries, it creates optimizations (indexes, matviews, query
rewrites) in the background. Check the dashboard at http://localhost:7933
to see what it found.
