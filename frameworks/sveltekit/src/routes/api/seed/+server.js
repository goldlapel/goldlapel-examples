import { json } from '@sveltejs/kit';
import { pool } from '$lib/server/db.js';

export async function POST() {
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
  return json({ ok: true });
}
