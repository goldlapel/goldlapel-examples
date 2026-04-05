# Gold Lapel — macOS

Install GL via Homebrew and proxy a simple app through it.

## Setup

1. Install Gold Lapel:
   ```bash
   brew install goldlapel/tap/goldlapel
   ```

2. Start Postgres:
   ```bash
   docker compose up -d
   ```

3. Start Gold Lapel:
   ```bash
   goldlapel --upstream postgres://gl:gl@localhost:5432/todos --proxy-port 7932
   ```

4. Install Python deps (in another terminal):
   ```bash
   pip install -r requirements.txt
   ```

5. Run the app:
   ```bash
   python app.py
   ```

## What to look for

Check the dashboard at http://localhost:7933.
