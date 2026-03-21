# Gold Lapel — Prisma

One-line Prisma integration with `withGoldLapel()`.

## Setup

1. Start Postgres: `docker compose up -d`
2. Install deps: `npm install`
3. Generate Prisma client: `npx prisma generate`
4. Push schema: `npx prisma db push`
5. Run the app: `node app.js`

## What to look for

GL starts automatically when Prisma connects. Check the dashboard at http://localhost:7933.
