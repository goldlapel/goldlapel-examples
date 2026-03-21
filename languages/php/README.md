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

GL starts automatically when `GoldLapel::start()` is called. As it observes queries, it creates optimizations (indexes, rewrites) in the background. Check the dashboard at http://localhost:7933 to see what it found.
