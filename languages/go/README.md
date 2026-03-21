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

GL starts automatically when `goldlapel.Start()` is called. As it observes
queries, it creates optimizations (indexes, query rewrites) in the background.
Check the dashboard at http://localhost:7933 to see what GL is doing.
