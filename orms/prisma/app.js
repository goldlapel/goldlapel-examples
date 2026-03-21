import { withGoldLapel } from 'goldlapel-prisma'

const prisma = withGoldLapel()

await prisma.todo.create({ data: { title: 'Try Gold Lapel' } })
await prisma.todo.create({ data: { title: 'Read the docs', done: true } })

const todos = await prisma.todo.findMany({ orderBy: { id: 'asc' } })
console.log(todos)

await prisma.$disconnect()
