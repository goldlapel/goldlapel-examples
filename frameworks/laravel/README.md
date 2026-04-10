# Gold Lapel — Laravel

Auto-discovered Laravel integration — just install the package.

## Setup

1. Start Postgres:
   ```bash
   docker compose up -d
   ```

2. Install dependencies:
   ```bash
   composer install
   ```

3. Copy env file and generate key:
   ```bash
   cp .env.example .env && php artisan key:generate
   ```

4. Run migrations:
   ```bash
   php artisan migrate
   ```

5. Start the server:
   ```bash
   php artisan serve
   ```

6. Try it:
   ```bash
   curl http://localhost:8000/api/todos
   ```

## What to look for

GL starts automatically on first database connection. The only GL-specific step is `composer require goldlapel/goldlapel` — the service provider is auto-discovered by Laravel. An optional `goldlapel` config block in `config/database.php` lets you customize the port or pass extra args. Everything else is standard Laravel. Check the dashboard at http://localhost:7933 to see what GL found.
