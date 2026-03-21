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

GL starts automatically when the app calls `goldlapel.start()`. As it observes
queries, it creates optimizations (indexes, query rewrites) in the background.
Check the dashboard at http://localhost:7933 to see what GL is doing.
