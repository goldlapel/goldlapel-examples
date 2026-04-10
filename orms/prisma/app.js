import { withGoldLapel, stop } from '@goldlapel/prisma'

const prisma = await withGoldLapel({ url: 'postgres://gl:gl@localhost:5432/todos' })

await prisma.todo.create({ data: { title: 'Try Gold Lapel' } })
await prisma.todo.create({ data: { title: 'Read the docs', done: true } })

const todos = await prisma.todo.findMany({ orderBy: { id: 'asc' } })
console.log(todos)

await prisma.$disconnect()
await stop()
