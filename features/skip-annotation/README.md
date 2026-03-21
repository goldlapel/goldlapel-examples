# Gold Lapel — Skip Annotation

Opt specific queries out of GL optimization by adding a `/* goldlapel:skip */` comment to your SQL.

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

The app sends the same query 5 times normally (GL tracks it), then sends the same query 5 more times with the `/* goldlapel:skip */` annotation (GL ignores it completely).

Both return identical results from Postgres — the skip annotation is a SQL comment, so the database doesn't care. But GL treats annotated queries as invisible: no pattern tracking, no matview candidates, no stats.

Use skip annotations for:
- Admin or maintenance queries you don't want polluting pattern stats
- One-off reports or data exports
- Migration scripts
- Queries you've already hand-optimized and don't want GL touching

The annotation works as a block comment anywhere in the query: `/* goldlapel:skip */ SELECT ...` or `SELECT /* goldlapel:skip */ ...`.

Check the dashboard at http://localhost:7933 — you'll see the normal query tracked, but no trace of the skipped one.
