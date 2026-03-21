# Gold Lapel — Docker

Run GL as a container alongside Postgres — no local install needed.

## Setup

1. Start everything:
   ```bash
   docker compose up -d
   ```

2. Install Python deps:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

## What to look for

GL is running as a container, proxying traffic between the app and Postgres. Check the dashboard at http://localhost:7933.
