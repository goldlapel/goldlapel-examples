# Gold Lapel — Connection Pooling

See the difference between session and transaction pool modes.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```

3. Run in transaction mode:
   ```bash
   python app.py transaction
   ```

4. Run in session mode:
   ```bash
   python app.py session
   ```

5. Experiment with a custom pool_size:
   ```bash
   python app.py transaction 2
   ```

## What to look for

The app opens 10 sequential connections through GL and prints which backend PID each one gets.

In **transaction mode**, backend connections return to the pool after each transaction. Sequential clients reuse the same backends — you'll see very few unique PIDs (often just 1) because the pool recycles idle connections.

In **session mode**, each client session is pinned to its own dedicated backend for the session's lifetime. Since the app opens and closes connections sequentially (only 1 active at a time), you'll also see connection reuse — but if you add concurrency, session mode would pin each concurrent client to a separate backend.

The key difference shows up under concurrency: transaction mode multiplexes many clients over a small pool, while session mode dedicates a backend per client session.

Check the dashboard at http://localhost:7933.
