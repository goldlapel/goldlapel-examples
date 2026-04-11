# Gold Lapel — SQLAlchemy

Drop-in SQLAlchemy integration — import from `goldlapel.sqlalchemy` instead of `sqlalchemy`.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

## What to look for

GL starts automatically when the engine connects. As it observes queries, it creates optimizations (indexes, rewrites) in the background. Check the dashboard at http://localhost:7933 to see what it found.
