# Gold Lapel — Next.js

Minimal Next.js App Router example with Gold Lapel optimizing Postgres queries.

## Setup

1. Start Postgres: `docker compose up -d`
2. Install deps: `npm install`
3. Start the dev server: `npm run dev`
4. Seed the database: `curl -X POST http://localhost:3000/api/seed`
5. Try it: `curl http://localhost:3000/api/todos`

## What to look for

Gold Lapel starts lazily on the first database request — no configuration needed. Your app connects through GL's optimizing proxy instead of directly to Postgres. Check the dashboard at http://localhost:7933 to see what GL found.

## How it works

The only GL-specific code is `lib/db.js`:

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

Route handlers call `await getPool()` inside the async function body — not at module load — so `next build`'s page-data collection doesn't have to wait for GL to spawn.

If you use Prisma or Drizzle, see the dedicated adapters: `@goldlapel/prisma` and `@goldlapel/drizzle`.
