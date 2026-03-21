# Gold Lapel — Automatic Failover

Watch GL automatically failover from primary to standby when the primary goes down.

## Setup

1. Start Postgres primary and standby:

   ```bash
   docker compose up -d
   ```

   The standby may take a few seconds to start streaming.

2. Install deps:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python app.py
   ```

4. When prompted, stop the primary:

   ```bash
   docker compose stop primary
   ```

5. Press Enter in the app to see GL reconnect to the standby.

## What to look for

- The app writes to the primary, then after you stop it, GL automatically routes to the standby.
- The app shows which server it's connected to.
