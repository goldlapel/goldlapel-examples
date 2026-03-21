# Gold Lapel — Materialized View Auto-Creation

GL watches for repeated query patterns and transparently creates materialized views to accelerate them — no schema changes or application code needed.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the demo:
   ```bash
   python app.py
   ```

## What to look for

The app sends the same join query (customers + orders) 5 times. After GL sees the pattern repeat past the `min_pattern_count` threshold, it creates a materialized view behind the scenes.

After a short wait, the app sends the query again. This time GL rewrites it to read from the matview instead of re-executing the join — same results, faster execution.

Check the dashboard at http://localhost:7933 to see the matview GL created, including its name, the original query pattern, and refresh schedule.
