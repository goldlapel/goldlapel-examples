# Gold Lapel Example — Python Todo App

CRUD todo app using FastAPI + psycopg, proxied through Gold Lapel.

## Setup

### 1. Start Postgres

```bash
docker compose up -d
```

### 2. Start Gold Lapel

```bash
# From the goldlapel repo (after cargo build --release)
./target/release/goldlapel \
    --upstream postgres://gl:gl@localhost:5432/todos \
    --port 7932
```

### 3. Start the app

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

The app connects to `localhost:7932` (GL proxy) by default. To bypass GL and connect directly to Postgres:

```bash
DATABASE_URL=postgres://gl:gl@localhost:5432/todos uvicorn app:app --reload
```

### 4. Generate traffic

```bash
./generate_traffic.sh
```

Creates 20 todos, sends 260 read requests across 6 different query patterns, then completes some todos and reads again. This gives GL enough observations to start creating matviews.

### 5. Check what GL did

```bash
goldlapel status --upstream postgres://gl:gl@localhost:5432/todos
```

Or open the dashboard at http://localhost:7933.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/todos` | List all todos |
| GET | `/todos/pending` | List pending todos |
| GET | `/todos/completed` | List completed todos |
| GET | `/todos/search?q=term` | Search by title (ILIKE) |
| GET | `/todos/stats` | Aggregate stats |
| GET | `/todos/{id}` | Get single todo |
| POST | `/todos?title=...` | Create todo |
| PUT | `/todos/{id}?completed=true` | Update todo |
| DELETE | `/todos/{id}` | Delete todo |

## What GL optimizes

The 6 read endpoints generate repeating query patterns. After enough observations, GL will:

- Create **materialized views** for the most common patterns (list all, pending, completed, stats)
- Create **indexes** (btree on `completed`, trigram on `title` for ILIKE searches)
- **Rewrite** incoming queries to read from matviews instead of the base table
