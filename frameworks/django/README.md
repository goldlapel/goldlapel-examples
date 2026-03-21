# Gold Lapel — Django

One-line Django integration — swap the database ENGINE.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the app:
   ```bash
   python manage.py runserver
   ```

5. Try it:
   ```bash
   curl http://localhost:8000/todos/
   ```

## What to look for

GL starts automatically on first database connection. The only GL-specific change is in `settings.py` — the database `ENGINE` is set to `"django_goldlapel"` instead of `"django.db.backends.postgresql"`. Everything else is standard Django. Check the dashboard at http://localhost:7933 to see what GL found.
