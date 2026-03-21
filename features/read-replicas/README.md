# Gold Lapel — Read Replicas

Automatic read routing to a replica with read-after-write protection.

## Setup

1. Start Postgres primary and replica:

   ```bash
   docker compose up -d
   ```

   The replica may take a few seconds to start streaming.

2. Install deps:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python app.py
   ```

## What to look for

- Writes go to the primary.
- Reads on the same connection immediately after a write stay on primary (read-after-write protection).
- Reads on a fresh connection route to the replica.
- The app prints which server each query hit.
