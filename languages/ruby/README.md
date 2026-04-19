# Gold Lapel — Ruby Wrapper

Minimal example showing Gold Lapel optimizing Postgres queries via the Ruby wrapper.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Install dependencies:
   ```bash
   bundle install
   ```

3. Run the app:
   ```bash
   ruby app.rb
   ```

## What to look for

The app calls `Goldlapel.start(upstream)`, which spawns the proxy and returns
a `Goldlapel::Instance`. `gl.url` is the proxy connection string — pass it to
`PG.connect(...)` for raw SQL. The same instance also exposes wrapper methods
(`gl.doc_insert`, `gl.search`, etc.) directly.

`gl.stop` shuts the proxy down; it also runs automatically on process exit.

As GL observes queries, it creates optimizations (indexes, matviews, query
rewrites) in the background. Check the dashboard at http://localhost:7933 to
see what it found.
