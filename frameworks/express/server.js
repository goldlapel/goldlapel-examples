import express from 'express';
import { getPool } from './db.js';

const app = express();
app.use(express.json());

// Seed
app.post('/seed', async (req, res) => {
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
  res.json({ ok: true });
});

// List
app.get('/todos', async (req, res) => {
  const pool = await getPool();
  const { rows } = await pool.query('SELECT * FROM todos ORDER BY id');
  res.json(rows);
});

// Create
app.post('/todos', async (req, res) => {
  const pool = await getPool();
  const { rows } = await pool.query(
    'INSERT INTO todos (title, done) VALUES ($1, false) RETURNING *',
    [req.body.title]
  );
  res.status(201).json(rows[0]);
});

app.listen(3000, () => console.log('Listening on http://localhost:3000'));
