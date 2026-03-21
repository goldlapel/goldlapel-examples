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

3. Run in transaction mode (defaults to pool_size=2):
   ```bash
   python app.py transaction
   ```

4. Run in session mode (uses GL default pool_size — one connection per client session):
   ```bash
   python app.py session
   ```

5. Experiment with a custom pool_size:
   ```bash
   python app.py transaction 4
   ```

## What to look for

In **transaction mode** with pool_size=2, all 5 workers share just 2 backend connections — you'll see only 2 unique PIDs because GL multiplexes transactions over a small pool. In **session mode**, each worker gets its own dedicated backend connection (5 unique PIDs) because GL pins a backend to each client session. Check the dashboard at http://localhost:7933.
