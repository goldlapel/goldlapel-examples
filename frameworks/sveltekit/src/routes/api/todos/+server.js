import { json } from '@sveltejs/kit';
import { pool } from '$lib/server/db.js';

export async function GET() {
  const { rows } = await pool.query('SELECT * FROM todos ORDER BY id');
  return json(rows);
}

export async function POST({ request }) {
  const { title } = await request.json();
  const { rows } = await pool.query(
    'INSERT INTO todos (title, done) VALUES ($1, false) RETURNING *',
    [title]
  );
  return json(rows[0], { status: 201 });
}
