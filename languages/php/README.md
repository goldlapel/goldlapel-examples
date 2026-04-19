# Gold Lapel — PHP Wrapper

Minimal example showing Gold Lapel optimizing Postgres queries via the PHP wrapper.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Install dependencies:
   ```bash
   composer install
   ```

3. Run the app:
   ```bash
   php app.php
   ```

## What to look for

The app calls `GoldLapel::start($upstream, $options)`, which spawns the proxy
and returns a `GoldLapel` instance. `$gl->pdoDsn()` / `$gl->pdoCredentials()`
give you PDO-ready values; `$gl->url()` returns the raw `postgresql://...`
URL for libraries that want the URL form.

The same instance exposes wrapper methods (`$gl->docInsert`, `$gl->search`,
etc.) directly.

As GL observes queries, it creates optimizations (indexes, matviews, query
rewrites) in the background. Check the dashboard at http://localhost:7933 to
see what it found.
