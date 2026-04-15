# Gold Lapel — Java Wrapper

Minimal example showing Gold Lapel optimizing Postgres queries via the Java wrapper.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Build and run:
   ```bash
   mvn compile exec:java
   ```

## What to look for

GL starts automatically when `gl.start()` is called on a `new GoldLapel(...)` instance. As it observes queries, it creates optimizations (indexes, rewrites) in the background. Check the dashboard at http://localhost:7933 to see what it found.
