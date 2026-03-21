# Gold Lapel — Windows

Install GL via PowerShell and proxy a simple app through it.

## Setup

1. Install Gold Lapel:
   ```powershell
   irm https://goldlapel.com/install.ps1 | iex
   ```

2. Start Postgres:
   ```powershell
   docker compose up -d
   ```

3. Start Gold Lapel:
   ```powershell
   goldlapel --upstream postgres://gl:gl@localhost:5432/todos --port 7932
   ```

4. Install Python deps (in another terminal):
   ```powershell
   pip install -r requirements.txt
   ```
   > **Note:** If using a venv, activate it with `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

5. Run the app:
   ```powershell
   python app.py
   ```

## What to look for

Check the Gold Lapel dashboard at [http://localhost:7933](http://localhost:7933).
