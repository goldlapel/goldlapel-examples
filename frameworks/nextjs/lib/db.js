import { GoldLapel } from '@goldlapel/goldlapel';
import pg from 'pg';

const gl = new GoldLapel(process.env.DATABASE_URL);
await gl.start();
export const pool = new pg.Pool({ connectionString: gl.proxyUrl() });
