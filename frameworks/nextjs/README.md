# Gold Lapel — Next.js

Minimal Next.js App Router example with Gold Lapel optimizing Postgres queries.

## Setup

1. Start Postgres: `docker compose up -d`
2. Install deps: `npm install`
3. Start the dev server: `npm run dev`
4. Seed the database: `curl -X POST http://localhost:3000/api/seed`
5. Try it: `curl http://localhost:3000/api/todos`

## What to look for

Gold Lapel starts automatically when `lib/db.js` is first imported — no configuration needed. Your app connects through GL's optimizing proxy instead of directly to Postgres. Check the dashboard at http://localhost:7933 to see what GL found.

## How it works

The only GL-specific code is `lib/db.js`:

```js
import { GoldLapel } from '@goldlapel/goldlapel';
import pg from 'pg';

const gl = new GoldLapel(process.env.DATABASE_URL);
await gl.start();
export const pool = new pg.Pool({ connectionString: gl.proxyUrl() });
```

API routes import the pool and query normally. That's it — everything else is standard Next.js.

If you use Prisma or Drizzle, see the dedicated adapters: `@goldlapel/prisma` and `@goldlapel/drizzle`.
