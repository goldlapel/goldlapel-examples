# Gold Lapel — .NET Wrapper

Minimal example showing Gold Lapel optimizing Postgres queries via the .NET wrapper.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Run the app:
   ```bash
   dotnet run
   ```

## What to look for

The app calls `await GoldLapel.StartAsync(upstream, opts => ...)`, which
spawns the proxy and returns a `GoldLapel` instance. `gl.Url` is a
Npgsql-ready connection string — pass it to `new NpgsqlConnection(...)`. The
same instance exposes wrapper methods (`gl.DocInsertAsync`, `gl.SearchAsync`,
etc.) directly.

`await using` auto-stops the proxy at scope end.

As GL observes queries, it creates optimizations (indexes, matviews, query
rewrites) in the background. Check the dashboard at http://localhost:7933 to
see what it found.
