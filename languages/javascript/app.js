import goldlapel from 'goldlapel'

const conn = await goldlapel.start('postgres://gl:gl@localhost:5432/todos')

await conn.query('CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)')
await conn.query('INSERT INTO todos (title) VALUES ($1)', ['Try Gold Lapel'])
await conn.query('INSERT INTO todos (title, done) VALUES ($1, $2)', ['Read the docs', true])

const { rows } = await conn.query('SELECT id, title, done FROM todos ORDER BY id')
console.log(rows)

await conn.end()
goldlapel.stop()
