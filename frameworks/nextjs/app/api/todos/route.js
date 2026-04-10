import { pool } from '../../../lib/db.js';

export async function GET() {
  const { rows } = await pool.query('SELECT * FROM todos ORDER BY id');
  return Response.json(rows);
}

export async function POST(req) {
  const { title } = await req.json();
  const { rows } = await pool.query(
    'INSERT INTO todos (title, done) VALUES ($1, false) RETURNING *',
    [title]
  );
  return Response.json(rows[0], { status: 201 });
}
