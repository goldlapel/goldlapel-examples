# Gold Lapel — Express

Minimal Express example with Gold Lapel optimizing Postgres queries.

## Setup

1. Start Postgres: `docker compose up -d`
2. Install deps: `npm install`
3. Start the server: `npm start`
4. Seed the database: `curl -X POST http://localhost:3000/seed`
5. Try it: `curl http://localhost:3000/todos`

## What to look for

Gold Lapel starts lazily on the first database request — no configuration needed. Your app connects through GL's optimizing proxy instead of directly to Postgres. Check the dashboard at http://localhost:7933 to see what GL found.

## How it works

The only GL-specific code is `db.js`:

```js
import goldlapel from 'goldlapel';
import pg from 'pg';

let _instance = null;
let _pool = null;

export async function getGl() {
  if (!_instance) {
    _instance = await goldlapel.start(process.env.DATABASE_URL);
  }
  return _instance;
}

export async function getPool() {
  if (!_pool) {
    const gl = await getGl();
    _pool = new pg.Pool({ connectionString: gl.url });
  }
  return _pool;
}
```

Route handlers call `await getPool()` inside the async handler body — not at module load — so the server can bind its listener immediately and GL only spawns when a request actually hits the database.

If you use Prisma or Drizzle, see the dedicated adapters: `@goldlapel/prisma` and `@goldlapel/drizzle`.
