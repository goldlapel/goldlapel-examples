# Gold Lapel — Rails

Zero-config Rails integration — just add the gem.

## Setup

1. Start Postgres: `docker compose up -d`
2. Install deps: `bundle install`
3. Create database and migrate: `rails db:create db:migrate`
4. Start the server: `rails server`
5. Try it: `curl http://localhost:3000/todos`

## What to look for

GL starts automatically on first database connection — no configuration needed.
Check the dashboard at http://localhost:7933.
