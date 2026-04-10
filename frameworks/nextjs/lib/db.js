import goldlapel from '@goldlapel/goldlapel';
import pg from 'pg';

await goldlapel.start(process.env.DATABASE_URL);
export const pool = new pg.Pool({ connectionString: goldlapel.proxyUrl() });
