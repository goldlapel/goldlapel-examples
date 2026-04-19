import { getPool } from '../../../lib/db.js';

export async function POST() {
  const pool = await getPool();
  await pool.query(`
    CREATE TABLE IF NOT EXISTS todos (
      id SERIAL PRIMARY KEY,
      title TEXT NOT NULL,
      done BOOLEAN NOT NULL DEFAULT false
    )
  `);
  await pool.query(`
    INSERT INTO todos (title) VALUES ('Buy groceries'), ('Walk the dog'), ('Ship the feature')
    ON CONFLICT DO NOTHING
  `);
  return Response.json({ ok: true });
}
