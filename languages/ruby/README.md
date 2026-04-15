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

GL starts automatically when `gl.start` is called on a `GoldLapel.new` instance. As it observes queries, it creates optimizations (indexes, rewrites) in the background. Check the dashboard at http://localhost:7933 to see what it found.
