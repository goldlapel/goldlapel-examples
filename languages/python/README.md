# Gold Lapel — Python Wrapper

Minimal example showing Gold Lapel optimizing Postgres queries via the Python wrapper.

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

GL starts automatically when `gl.start()` is called on a `goldlapel.GoldLapel` instance. As it observes queries, it creates optimizations (indexes, rewrites) in the background. Check the dashboard at http://localhost:7933 to see what it found.
