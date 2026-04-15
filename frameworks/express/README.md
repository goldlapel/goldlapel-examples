# Gold Lapel — Express

Minimal Express example with Gold Lapel optimizing Postgres queries.

## Setup

1. Start Postgres: `docker compose up -d`
2. Install deps: `npm install`
3. Start the server: `npm start`
4. Seed the database: `curl -X POST http://localhost:3000/seed`
5. Try it: `curl http://localhost:3000/todos`

## What to look for

Gold Lapel starts automatically when `db.js` is first imported — no configuration needed. Your app connects through GL's optimizing proxy instead of directly to Postgres. Check the dashboard at http://localhost:7933 to see what GL found.

## How it works

The only GL-specific code is `db.js`:

```js
import { GoldLapel } from '@goldlapel/goldlapel';
import pg from 'pg';

const gl = new GoldLapel(process.env.DATABASE_URL);
await gl.start();
export const pool = new pg.Pool({ connectionString: gl.proxyUrl() });
```

Routes import the pool and query normally. That's it — everything else is standard Express.

If you use Prisma or Drizzle, see the dedicated adapters: `@goldlapel/prisma` and `@goldlapel/drizzle`.
