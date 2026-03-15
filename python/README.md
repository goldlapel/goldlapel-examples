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

By default GL starts in **bellhop mode**, which observes query patterns and suggests optimizations but does not modify your database. This is a safe way to see what GL would do before enabling active optimization.

### 3. Set up the app

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Then start the app:

```bash
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

Creates 20 todos, sends 260 read requests across 6 different query patterns, then completes some todos and reads again. This gives GL enough observations to start building suggestions.

### 5. Check what GL observed

```bash
goldlapel status --upstream postgres://gl:gl@localhost:5432/todos
```

Or open the dashboard at http://localhost:7933. You'll see the query patterns GL detected and what optimizations it recommends.

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

## What bellhop mode does

The 6 read endpoints generate repeating query patterns. In bellhop mode (the default), GL will:

- **Observe** query patterns and track frequency, latency, and row counts
- **Analyze** which queries would benefit from indexes, matviews, or rewrites
- **Suggest** optimizations via the dashboard and `goldlapel status` output

GL does not create indexes, materialized views, or rewrite queries in bellhop mode. It watches and reports.

## Try butler mode

To have GL **actively optimize** your database (create indexes, materialized views, and rewrite queries), start it in butler mode:

```bash
./target/release/goldlapel \
    --upstream postgres://gl:gl@localhost:5432/todos \
    --port 7932 \
    --mode butler
```

Butler mode requires a license or active trial. With butler mode enabled, GL will:

- Create **covering indexes** (btree on `completed`, `id`) so Postgres can do index-only scans
- Create a **trigram index** on `title` for the `ILIKE %...%` search pattern
- With enough data and latency, create **materialized views** for the heaviest patterns and **rewrite** queries to read from them
