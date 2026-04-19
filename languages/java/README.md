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

The app calls `GoldLapel.start(upstream, opts -> ...)`, which spawns the proxy
and returns a `GoldLapel` instance (try-with-resources auto-stops it). Because
the PostgreSQL JDBC driver doesn't accept inline userinfo, the example uses
`gl.getJdbcUrl()` + `gl.getJdbcUser()` / `gl.getJdbcPassword()` to hand a
clean URL and `Properties` to `DriverManager`.

The same instance exposes wrapper methods (`gl.docInsert`, `gl.search`, etc.)
directly.

As GL observes queries, it creates optimizations (indexes, matviews, query
rewrites) in the background. Check the dashboard at http://localhost:7933 to
see what it found.
