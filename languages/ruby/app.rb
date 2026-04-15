require "goldlapel"

gl = GoldLapel.new("postgres://gl:gl@localhost:5432/todos")
conn = gl.start

conn.exec("CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)")
conn.exec_params("INSERT INTO todos (title) VALUES ($1)", ["Try Gold Lapel"])
conn.exec_params("INSERT INTO todos (title, done) VALUES ($1, $2)", ["Read the docs", true])

conn.exec("SELECT id, title, done FROM todos ORDER BY id") do |result|
  result.each { |row| puts row.inspect }
end

conn.close
gl.stop
