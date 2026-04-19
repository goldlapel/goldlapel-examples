# Gold Lapel — Python Wrapper

Minimal example showing Gold Lapel optimizing Postgres queries via the Python wrapper.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

## What to look for

The app calls `goldlapel.start(upstream)`, which spawns the proxy and returns a
`GoldLapel` instance. `gl.url` is the proxy connection string — pass it to
`psycopg.connect(...)` (or any Postgres driver) for raw SQL. The same instance
also exposes wrapper methods like `gl.doc_insert` and `gl.search` directly.

The `with goldlapel.start(...)` context manager stops the proxy on exit. For
async code, use `from goldlapel.asyncio import start` and `async with start(...)`.

As GL observes queries, it creates optimizations (indexes, matviews, query
rewrites) in the background. Check the dashboard at http://localhost:7933 to
see what it found.
