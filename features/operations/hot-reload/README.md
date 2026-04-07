# Gold Lapel — Hot Reload

Change GL's configuration without restarting the proxy. GL polls its config file every 30 seconds and applies hot-reloadable settings on the fly.

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

The app starts GL with a config file set to `mode = "waiter"` and `min_pattern_count = 10`. After a couple of seconds, it overwrites the file with `mode = "bellhop"` and `min_pattern_count = 3`.

GL detects the change on its next poll cycle (up to 30 seconds) and applies the new values without dropping connections or restarting.

Watch the GL logs for:
- `hot-reloaded: mode: bellhop`
- `hot-reloaded: min-pattern-count: 10 -> 3`

After the reload completes, visit the dashboard at http://localhost:7933 to confirm the mode has changed to bellhop.

Hot-reloadable settings include mode, thresholds, and logging levels. Structural settings like port and upstream require a full restart.
