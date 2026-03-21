# Gold Lapel — Dashboard API

Access GL's stats, audit log, and configuration export programmatically through the REST API on port 7933.

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

The app generates some query traffic through GL, then hits three API endpoints:

- **`/api/stats`** — Live operational stats: mode, version, total queries observed, queries rewritten. Use this for monitoring dashboards and health checks.
- **`/api/audit`** — Chronological log of GL actions: matview creation, index suggestions, config reloads. Use this for alerting and compliance.
- **`/api/export`** — Full snapshot of GL's learned state: query patterns, matviews, indexes. Use this for CI integration, migration planning, or syncing config across environments.

All endpoints return JSON and require no authentication (they're bound to localhost by default).

You can also browse the dashboard UI at http://localhost:7933.
