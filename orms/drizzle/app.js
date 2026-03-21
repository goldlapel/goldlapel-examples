import { drizzle } from 'goldlapel-drizzle'
import { todos } from './schema.js'
import { asc } from 'drizzle-orm'
import { sql } from 'drizzle-orm'

const db = drizzle({ url: 'postgres://gl:gl@localhost:5432/todos', schema: { todos } })

await db.execute(sql`CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)`)
await db.insert(todos).values({ title: 'Try Gold Lapel' })
await db.insert(todos).values({ title: 'Read the docs', done: true })

const rows = await db.select().from(todos).orderBy(asc(todos.id))
console.log(rows)

process.exit(0)
