import goldlapel
import psycopg

url = goldlapel.start("postgres://gl:gl@localhost:5432/todos")

with psycopg.connect(url) as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)")
    conn.execute("INSERT INTO todos (title) VALUES (%s)", ("Try Gold Lapel",))
    conn.execute("INSERT INTO todos (title, done) VALUES (%s, %s)", ("Read the docs", True))
    conn.commit()
    for row in conn.execute("SELECT id, title, done FROM todos ORDER BY id"):
        print(row)

goldlapel.stop()
