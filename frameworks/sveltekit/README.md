# Gold Lapel — SvelteKit

Minimal SvelteKit example with Gold Lapel optimizing Postgres queries.

## Setup

1. Start Postgres: `docker compose up -d`
2. Install deps: `npm install`
3. Start the dev server: `npm run dev`
4. Seed the database: `curl -X POST http://localhost:5173/api/seed`
5. Try it: `curl http://localhost:5173/api/todos`

## What to look for

Gold Lapel starts automatically when `src/lib/server/db.js` is first imported — no configuration needed. Your app connects through GL's optimizing proxy instead of directly to Postgres. Check the dashboard at http://localhost:7933 to see what GL found.

## How it works

The only GL-specific code is `src/lib/server/db.js`:

```js
import goldlapel from '@goldlapel/goldlapel';
import pg from 'pg';

await goldlapel.start(process.env.DATABASE_URL);
export const pool = new pg.Pool({ connectionString: goldlapel.proxyUrl() });
```

The `server/` directory ensures this module is never bundled into client code. API routes import the pool and query normally. That's it — everything else is standard SvelteKit.

If you use Prisma or Drizzle, see the dedicated adapters: `@goldlapel/prisma` and `@goldlapel/drizzle`.
