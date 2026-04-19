# pip install goldlapel psycopg[binary]
import goldlapel
import psycopg

with goldlapel.start("postgres://gl:gl@localhost:5432/todos") as gl:
    with psycopg.connect(gl.url) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS todos (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false)")
        conn.execute("INSERT INTO todos (title) VALUES (%s)", ("Try Gold Lapel",))
        conn.execute("INSERT INTO todos (title, done) VALUES (%s, %s)", ("Read the docs", True))
        for row in conn.execute("SELECT id, title, done FROM todos ORDER BY id"):
            print(row)

    # Wrapper methods also work directly on the GoldLapel instance.
    gl.doc_insert("events", {"type": "demo.ran"})
    print("events:", gl.doc_find("events", {"type": "demo.ran"}))
