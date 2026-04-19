// npm install goldlapel pg
import * as goldlapel from 'goldlapel'
import pg from 'pg'

const gl = await goldlapel.start('postgres://gl:gl@localhost:5432/todos')

const client = new pg.Client({ connectionString: gl.url })
await client.connect()

await client.query('CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)')
await client.query('INSERT INTO todos (title) VALUES ($1)', ['Try Gold Lapel'])
await client.query('INSERT INTO todos (title, done) VALUES ($1, $2)', ['Read the docs', true])

const { rows } = await client.query('SELECT id, title, done FROM todos ORDER BY id')
console.log(rows)

await client.end()

// Wrapper methods also work directly on the instance.
await gl.docInsert('events', { type: 'demo.ran' })
console.log('events:', await gl.docFind('events', { type: 'demo.ran' }))

await gl.stop()
