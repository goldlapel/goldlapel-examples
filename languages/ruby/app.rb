require "goldlapel"
require "pg"

url = GoldLapel.start("postgres://gl:gl@localhost:5432/todos")
conn = PG.connect(url)

conn.exec("CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)")
conn.exec_params("INSERT INTO todos (title) VALUES ($1)", ["Try Gold Lapel"])
conn.exec_params("INSERT INTO todos (title, done) VALUES ($1, $2)", ["Read the docs", true])

conn.exec("SELECT id, title, done FROM todos ORDER BY id") do |result|
  result.each { |row| puts row.inspect }
end

conn.close
GoldLapel.stop
